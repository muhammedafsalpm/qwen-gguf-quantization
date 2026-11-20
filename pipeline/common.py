"""Shared helpers for the quantization pipeline (paths, config, running tools, hashing)."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

with open(ROOT / "config.yaml", encoding="utf-8") as _f:
    CFG: dict = yaml.safe_load(_f)

NAME: str = CFG["model"]["name"]


def path(rel: str) -> Path:
    return ROOT / rel


MODEL_DIR = path(CFG["model"]["local_dir"])
OUT = path(CFG["paths"]["out"])
DATA = path(CFG["paths"]["data"])
LOGS = path(CFG["paths"]["logs"])
RESULTS = path(CFG["paths"]["results"])
RELEASE = path(CFG["paths"]["release"])
for _d in (OUT, DATA, LOGS, RESULTS):
    _d.mkdir(parents=True, exist_ok=True)

LLAMA_SRC = path(CFG["llama_cpp"]["src"])
LLAMA_BIN = path(CFG["llama_cpp"]["bin"])


def gguf(quant: str) -> Path:
    return OUT / f"{NAME}-{quant}.gguf"


BF16 = gguf(CFG["convert"]["outtype"].upper())
MMPROJ = OUT / f"mmproj-{NAME}-{CFG['convert']['mmproj_outtype'].upper()}.gguf"
IMATRIX = OUT / f"{NAME}.imatrix.gguf"
CALIB = DATA / "calibration.txt"
EVAL_TEXT = DATA / "wiki.test.raw"
KLD_BASE = DATA / "kld_base_bf16.bin"


def tool(name: str) -> str:
    exe = LLAMA_BIN / (f"{name}.exe" if os.name == "nt" else name)
    if not exe.exists():
        sys.exit(f"Missing llama.cpp tool: {exe}")
    return str(exe)


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(cmd: list, log_name: str) -> str:
    """Run a command, stream its output to the console and logs/<log_name>.log.
    Exits the script if the command fails. Returns the full output."""
    cmd = [str(c) for c in cmd]
    log("$ " + " ".join(cmd))
    log_path = LOGS / f"{log_name}.log"
    out: list[str] = []
    t0 = time.time()
    with open(log_path, "w", encoding="utf-8", errors="replace") as lf:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding="utf-8", errors="replace", bufsize=1)
        assert proc.stdout is not None
        # Read in small chunks, not lines: progress bars redraw with "\r" and no newline
        for part in iter(lambda: proc.stdout.read(256), ""):
            sys.stdout.write(part)
            sys.stdout.flush()
            lf.write(part)
            lf.flush()
            out.append(part)
        rc = proc.wait()
    log(f"finished in {(time.time() - t0) / 60:.1f} min (exit {rc}) -> {log_path.name}")
    if rc != 0:
        sys.exit(f"Command failed with exit code {rc}. See {log_path}")
    return "".join(out)


def require(p: Path, hint: str) -> None:
    if not p.exists():
        sys.exit(f"Missing {p}. {hint}")


def sha256(p: Path, chunk: int = 16 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(chunk):
            h.update(b)
    return h.hexdigest()


def save_json(p: Path, data) -> None:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")


def file_id(p: Path) -> dict:
    """Cheap identity of a file (size + modification time) to detect rebuilt files."""
    st = p.stat()
    return {"size": st.st_size, "mtime": int(st.st_mtime)}


def single_instance(lock_path: Path, what: str):
    """Exit if another process already holds this lock. The operating system releases
    the lock when the process ends, even after a crash, so it never goes stale.
    Keep the returned file object alive for as long as the lock is needed."""
    f = open(lock_path, "a+")
    f.seek(0)
    try:
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        f.close()
        sys.exit(f"Another {what} is already running (lock: {lock_path}). Wait for it to finish.")
    return f


def load_json(p: Path, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def gb(n_bytes: int) -> float:
    return round(n_bytes / 1e9, 2)
