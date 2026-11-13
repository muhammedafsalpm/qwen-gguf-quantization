"""Live progress bar for the Hugging Face model download.

Usage (in the mycuda env, from the quantization folder):
    python tools/progress.py            # live bar, refreshes every 2 s (Ctrl+C to stop)
    python tools/progress.py --once     # print one line and exit
"""
import sys
import time
from pathlib import Path

from huggingface_hub import HfApi

REPO = "Qwen/Qwen3.8-27B"
LOCAL = Path(__file__).resolve().parent.parent / "models" / "Qwen3.8-27B"
WIDTH = 40


REMOTE: dict[str, int] = {}


def remote_total() -> int:
    info = HfApi().model_info(REPO, files_metadata=True)
    REMOTE.update({s.rfilename: s.size or 0 for s in info.siblings})
    return sum(REMOTE.values())


def local_bytes() -> int:
    # Only finished files whose size matches the repo. Temporary *.incomplete
    # files can be pre-allocated at full size, so counting them overstates progress.
    done = 0
    for name, size in REMOTE.items():
        p = LOCAL / name
        if p.is_file() and p.stat().st_size == size:
            done += size
    return done


def files_done() -> str:
    n = sum(1 for name, size in REMOTE.items()
            if (LOCAL / name).is_file() and (LOCAL / name).stat().st_size == size)
    return f"{n}/{len(REMOTE)} files"


def bar(done: int, total: int, speed: float) -> str:
    frac = min(done / total, 1.0) if total else 0.0
    filled = int(WIDTH * frac)
    eta = (total - done) / speed if speed > 0 else 0
    eta_txt = time.strftime("%H:%M:%S", time.gmtime(eta)) if speed > 0 else "--:--:--"
    return (f"[{'#' * filled}{'.' * (WIDTH - filled)}] {frac * 100:5.1f}%  "
            f"{done / 1e9:6.1f} / {total / 1e9:.1f} GB  {files_done()}  "
            f"{speed / 1e6:7.1f} MB/s  ETA {eta_txt}")


def main() -> None:
    total = remote_total()
    if "--once" in sys.argv:
        print(bar(local_bytes(), total, 0.0))
        return
    prev, prev_t, speed = local_bytes(), time.time(), 0.0
    try:
        while True:
            time.sleep(2)
            now, t = local_bytes(), time.time()
            inst = max(now - prev, 0) / (t - prev_t)
            speed = inst if speed == 0 else 0.7 * speed + 0.3 * inst  # smoothed
            prev, prev_t = now, t
            print("\r" + bar(now, total, speed), end="", flush=True)
            if now >= total:
                print("\nDownload complete.")
                break
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
