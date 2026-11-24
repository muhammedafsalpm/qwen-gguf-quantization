"""Throughput and latency of every quant under concurrent load (llama-server, continuous batching).

For each quant, llama-server is started with one slot per concurrent user. At each concurrency level
N, N requests are sent at the same time (two waves per level); each has a different ~500-token prompt
and generates exactly 256 tokens (thinking off, temperature 0, end-of-text ignored), so every quant does
the same work.

    python tools/concurrency_bench.py                         # all quants, 1 2 4 8 16 users
    python tools/concurrency_bench.py --only Q4_K_M Q8_0 --levels 1 4 16

Measured per level: total throughput (generated tokens/s, all users), generation speed per user,
time to first token (p50/p95), request latency (p50/p95) and GPU memory in use.
Output: results/concurrency/<date-time>/report.md and results.json
"""
import argparse
import json
import socket
import statistics
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
from common import CFG, EVAL_TEXT, LOGS, RESULTS, gguf, log, require, save_json, tool  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--only", nargs="*", help="quant types (default: all in config.yaml)")
ap.add_argument("--levels", nargs="*", type=int, default=[1, 2, 4, 8, 16])
ap.add_argument("--gen", type=int, default=256, help="tokens generated per request")
ap.add_argument("--prompt-chars", type=int, default=2000, help="prompt length (~500 tokens of English text)")
ap.add_argument("--ctx-per-slot", type=int, default=4096)
ap.add_argument("--waves", type=int, default=2, help="repeats per concurrency level")
ap.add_argument("--port", type=int, default=8091)
args = ap.parse_args()

types = args.only or CFG["quantize"]["types"]
slots = max(args.levels)
for t in types:
    require(gguf(t), "Build the quants first (run_all.py).")
require(EVAL_TEXT, "Run step 03 first (held-out text is used for prompts).")
TEXT = EVAL_TEXT.read_text(encoding="utf-8")
OUT_DIR = RESULTS / "concurrency" / time.strftime("%Y%m%d-%H%M%S")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def gpu_mem_mb() -> int:
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=10).stdout
        return int(out.strip().splitlines()[0])
    except Exception:
        return -1


def port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_server(t: str):
    if port_in_use(args.port):
        sys.exit(f"Port {args.port} is already in use. Stop the other server or pass --port.")
    log_f = open(LOGS / f"concurrency_server_{t}.log", "w", encoding="utf-8", errors="replace")
    proc = subprocess.Popen([tool("llama-server"), "-m", str(gguf(t)), "-ngl", "99", "--jinja",
                             "-np", str(slots), "-c", str(slots * args.ctx_per_slot),
                             "--host", "127.0.0.1", "--port", str(args.port)],
                            stdout=log_f, stderr=subprocess.STDOUT)
    t0 = time.time()
    try:
        while time.time() - t0 < 900:
            if proc.poll() is not None:
                sys.exit(f"llama-server stopped while loading {t}; see logs/concurrency_server_{t}.log")
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{args.port}/health", timeout=5) as r:
                    if r.status == 200:
                        return proc, log_f
            except Exception:
                pass
            time.sleep(2)
    except BaseException:
        proc.kill()  # do not leave a server holding GPU memory on Ctrl+C
        raise
    proc.kill()
    sys.exit(f"llama-server did not become ready for {t}")


def stop_server(proc, log_f):
    proc.terminate()
    try:
        proc.wait(30)
    except subprocess.TimeoutExpired:
        proc.kill()
    log_f.close()


def one_request(idx: int, out: list):
    """Streamed request; records time to first token, total time and generated tokens."""
    start = (idx * 7919) % (len(TEXT) - args.prompt_chars)  # a different slice per request (no prompt cache reuse)
    body = {"messages": [{"role": "user", "content": "Continue this text:\n\n" + TEXT[start:start + args.prompt_chars]}],
            "max_tokens": args.gen, "temperature": 0, "ignore_eos": True, "stream": True,
            "chat_template_kwargs": {"enable_thinking": False}}
    req = urllib.request.Request(f"http://127.0.0.1:{args.port}/v1/chat/completions",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    first, n, timings = None, 0, {}
    try:
        with urllib.request.urlopen(req, timeout=1800) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:") or line == "data: [DONE]":
                    continue
                ev = json.loads(line[5:])
                if ev.get("timings"):
                    timings = ev["timings"]
                delta = (ev.get("choices") or [{}])[0].get("delta", {})
                if delta.get("content") or delta.get("reasoning_content"):
                    n += 1
                    if first is None:
                        first = time.perf_counter()
        end = time.perf_counter()
        gen = timings.get("predicted_n") or n
        out.append({"ttft_s": (first or end) - t0, "latency_s": end - t0, "gen_tokens": gen,
                    "user_tok_s": gen / max(end - (first or t0), 1e-6), "error": None})
    except Exception as e:  # recorded, not fatal: one failed request should not end the benchmark
        out.append({"error": repr(e)})


def pct(vals, p):
    vals = sorted(vals)
    return vals[min(len(vals) - 1, max(0, round(p / 100 * (len(vals) - 1))))] if vals else None


results = {"settings": {"levels": args.levels, "gen": args.gen, "prompt_chars": args.prompt_chars,
                        "ctx_per_slot": args.ctx_per_slot, "waves": args.waves, "slots": slots,
                        "llama_cpp": CFG["llama_cpp"]["build"]}, "quants": {}}
for t in types:
    log(f"=== {t}: loading ({slots} slots)")
    proc, log_f = start_server(t)
    q = results["quants"][t] = {"gpu_mem_loaded_mb": gpu_mem_mb(), "levels": {}}
    try:
        warm = []
        one_request(0, warm)  # warm-up, not counted
        counter = 1
        for n in args.levels:
            reqs, walls, peak = [], [], 0
            for _ in range(args.waves):
                wave, threads = [], []
                for i in range(n):
                    threads.append(threading.Thread(target=one_request, args=(counter, wave)))
                    counter += 1
                w0 = time.perf_counter()
                for th in threads:
                    th.start()
                while any(th.is_alive() for th in threads):
                    peak = max(peak, gpu_mem_mb())
                    time.sleep(1)
                walls.append(time.perf_counter() - w0)
                reqs += wave
            ok = [r for r in reqs if not r["error"]]
            total_tokens = sum(r["gen_tokens"] for r in ok)
            lv = q["levels"][str(n)] = {
                "requests": len(reqs), "errors": len(reqs) - len(ok),
                "throughput_tok_s": round(total_tokens / sum(walls), 1) if ok else None,
                "user_tok_s": round(statistics.mean(r["user_tok_s"] for r in ok), 1) if ok else None,
                "ttft_p50_s": round(pct([r["ttft_s"] for r in ok], 50), 2) if ok else None,
                "ttft_p95_s": round(pct([r["ttft_s"] for r in ok], 95), 2) if ok else None,
                "latency_p50_s": round(pct([r["latency_s"] for r in ok], 50), 2) if ok else None,
                "latency_p95_s": round(pct([r["latency_s"] for r in ok], 95), 2) if ok else None,
                "gpu_mem_peak_mb": peak}
            log(f"  {n:>2} users: {lv['throughput_tok_s']} tok/s total, {lv['user_tok_s']} tok/s per user, "
                f"first token p95 {lv['ttft_p95_s']} s, errors {lv['errors']}")
    finally:
        stop_server(proc, log_f)
    save_json(OUT_DIR / "results.json", results)

# ---------- report ----------
lv_cols = [str(n) for n in args.levels]
L = [f"# Concurrent load: {CFG['model']['name']}", "",
     f"llama-server (llama.cpp {CFG['llama_cpp']['build']}), {slots} slots × {args.ctx_per_slot} tokens, continuous batching. "
     f"Each request: ~{args.prompt_chars // 4}-token prompt, exactly {args.gen} generated tokens, thinking off, "
     f"{args.waves} waves per level. Text only (no vision projector).", "",
     "## Total throughput (generated tokens/s, all users combined)", "",
     "| Type | " + " | ".join(f"{n} user{'s' if n != '1' else ''}" for n in lv_cols) + " |",
     "|---|" + "---|" * len(lv_cols)]
for t in types:
    L.append(f"| {t} | " + " | ".join(str(results['quants'][t]['levels'][n]['throughput_tok_s']) for n in lv_cols) + " |")
L += ["", "## Generation speed per user (tokens/s)", "",
      "| Type | " + " | ".join(lv_cols) + " |", "|---|" + "---|" * len(lv_cols)]
for t in types:
    L.append(f"| {t} | " + " | ".join(str(results['quants'][t]['levels'][n]['user_tok_s']) for n in lv_cols) + " |")
L += ["", "## Time to first token, p95 (s)", "",
      "| Type | " + " | ".join(lv_cols) + " |", "|---|" + "---|" * len(lv_cols)]
for t in types:
    L.append(f"| {t} | " + " | ".join(str(results['quants'][t]['levels'][n]['ttft_p95_s']) for n in lv_cols) + " |")
L += ["", "## GPU memory (GB): after loading / peak at the highest level", "", "| Type | Loaded | Peak | Errors |", "|---|---|---|---|"]
for t in types:
    q = results["quants"][t]
    errs = sum(v["errors"] for v in q["levels"].values())
    L.append(f"| {t} | {q['gpu_mem_loaded_mb'] / 1024:.1f} | {q['levels'][lv_cols[-1]]['gpu_mem_peak_mb'] / 1024:.1f} | {errs} |")
(OUT_DIR / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
log(f"report: {OUT_DIR / 'report.md'}")
