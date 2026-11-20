"""Step 06: measure quality and test functionality of every quant.

1. Accuracy vs the BF16 original on held-out wikitext-2 test text:
   perplexity, KL divergence (mean / 99.9th pct / max), RMS delta-p, same-top-token %.
2. Functional tests through llama-server (with the vision projector loaded):
   thinking on, thinking off, tool calling, image understanding. Also records speed.

    python pipeline/06_evaluate.py [--only Q4_K_M ...] [--skip-kld] [--skip-functional] [--force]
"""
import argparse
import base64
import json
import re
import socket
import struct
import subprocess
import time
import urllib.request
import zlib

from common import (BF16, CFG, DATA, EVAL_TEXT, KLD_BASE, LOGS, MMPROJ, RESULTS, file_id, gguf,
                    load_json, log, require, run, save_json, tool)

ap = argparse.ArgumentParser()
ap.add_argument("--only", nargs="*")
ap.add_argument("--skip-kld", action="store_true")
ap.add_argument("--skip-functional", action="store_true")
ap.add_argument("--force", action="store_true", help="re-run tests that already have results")
args = ap.parse_args()

ev = CFG["eval"]
types = args.only or CFG["quantize"]["types"]
RES_FILE = RESULTS / "eval.json"
res = load_json(RES_FILE, {"base": {}, "quants": {}})

NUM = r"([-\d.]+)"
PATTERNS = {
    "ppl": rf"Mean PPL\(Q\)\s*:\s*{NUM}\s*±\s*{NUM}",
    "kld_mean": rf"Mean\s+KLD:\s*{NUM}\s*±\s*{NUM}",
    "kld_max": rf"Maximum KLD:\s*{NUM}",
    "kld_p999": rf"99\.9%\s+KLD:\s*{NUM}",
    "kld_p99": rf"99\.0%\s+KLD:\s*{NUM}",
    "rms_dp": rf"RMS Δp\s*:\s*{NUM}\s*±\s*{NUM}",
    "same_top": rf"Same top p:\s*{NUM}\s*±\s*{NUM}",
}


def is_current(entry: dict, f) -> bool:
    """True if the stored results belong to the file as it is now. Results saved before
    file tracking existed are adopted for the current file (they were measured on it)."""
    if not f.exists():
        return False
    if "file" not in entry:
        entry["file"] = file_id(f)
        return True
    return entry["file"] == file_id(f)


def parse(output: str) -> dict:
    out = {}
    for key, pat in PATTERNS.items():
        m = re.findall(pat, output)
        if m:
            g = m[-1] if isinstance(m[-1], tuple) else (m[-1],)
            out[key] = float(g[0])
            if len(g) > 1:
                out[key + "_err"] = float(g[1])
        else:
            log(f"  warning: could not parse {key}")
    return out


# ---------- 1. KL divergence + perplexity ----------
if not args.skip_kld:
    require(EVAL_TEXT, "Run step 03 first.")
    common_args = ["-c", ev["ctx"], "--chunks", ev["chunks"]]
    # A rebuilt BF16 invalidates every comparison. If BF16 was deleted to free disk space,
    # the saved reference is kept as it is.
    base_changed = BF16.exists() and not is_current(res["base"], BF16)
    if not KLD_BASE.exists() or "ppl" not in res["base"] or base_changed:
        require(BF16, "Run step 02 first.")
        log("Computing BF16 reference logits (one-time, partially on CPU because BF16 > 48 GB)")
        out = run([tool("llama-perplexity"), "-m", BF16, "-f", EVAL_TEXT, "-ngl", ev["base_ngl"],
                   "--kl-divergence-base", KLD_BASE, *common_args], "06_kld_base_BF16")
        m = re.findall(rf"Final estimate: PPL = {NUM} \+/- {NUM}", out)
        res["base"] = {"type": "BF16", "ppl": float(m[-1][0]), "ppl_err": float(m[-1][1])} if m else {"type": "BF16"}
        res["base"]["file"] = file_id(BF16)
        save_json(RES_FILE, res)
    for t in types:
        q = res["quants"].setdefault(t, {})
        unchanged = not gguf(t).exists() or is_current(q, gguf(t))
        if "kld_mean" in q and unchanged and not base_changed and not args.force:
            log(f"skip KLD: {t} already measured")
            continue
        require(gguf(t), "Run step 05 first.")
        if "kld_mean" in q:
            log(f"  {t}: file or reference changed since the last measurement, re-measuring")
            for k in [k for k in q if k not in ("functional", "file")]:
                del q[k]  # drop old numbers so none of them survive a partial parse
        out = run([tool("llama-perplexity"), "-m", gguf(t), "-ngl", ev["ngl"],
                   "--kl-divergence-base", KLD_BASE, "--kl-divergence", *common_args], f"06_kld_{t}")
        q.update(parse(out))
        q["file"] = file_id(gguf(t))
        save_json(RES_FILE, res)
        log(f"  {t}: PPL {q.get('ppl')}  mean KLD {q.get('kld_mean')}  same-top {q.get('same_top')}%")


# ---------- 2. Functional tests ----------
def make_png(p):
    """256x256 white image with a red square in the middle (no extra libraries)."""
    w = h = 256
    rows = b"".join(
        b"\x00" + b"".join(b"\xdc\x1e\x1e" if 64 <= x < 192 and 64 <= y < 192 else b"\xff\xff\xff"
                           for x in range(w)) for y in range(h))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    p.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                  + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def post(port, body, timeout=900):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/chat/completions",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def wait_ready(port, proc, limit=900):
    t0 = time.time()
    while time.time() - t0 < limit:
        if proc.poll() is not None:
            raise RuntimeError("llama-server exited early; see the server log")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=5) as r:
                if r.status == 200:
                    return
        except Exception:
            pass
        time.sleep(3)
    raise RuntimeError("llama-server did not become ready")


TOOLS = [{"type": "function", "function": {
    "name": "get_weather", "description": "Get the current weather for a city",
    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]


def port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def functional(t: str) -> dict:
    port = ev["server_port"]
    if port_in_use(port):
        # Otherwise the health check could reach an old server and test the wrong model
        return {"error": f"port {port} is already in use; stop the other llama-server or change eval.server_port"}
    img = DATA / "test_red_square.png"
    if not img.exists():
        make_png(img)
    data_url = "data:image/png;base64," + base64.b64encode(img.read_bytes()).decode()
    log_f = open(LOGS / f"06_server_{t}.log", "w", encoding="utf-8", errors="replace")
    proc = subprocess.Popen([tool("llama-server"), "-m", str(gguf(t)), "--mmproj", str(MMPROJ),
                             "-ngl", str(ev["ngl"]), "-c", str(ev["server_ctx"]), "-np", "1",
                             "--host", "127.0.0.1", "--port", str(port), "--jinja"],
                            stdout=log_f, stderr=subprocess.STDOUT)
    results = {}
    try:
        wait_ready(port, proc)
        base = {"temperature": 0, "max_tokens": 6000}

        def msg_of(r):
            return r["choices"][0]["message"]

        # Thinking ON: classic trick question; needs reasoning to avoid the intuitive wrong answer
        r = post(port, {**base, "chat_template_kwargs": {"enable_thinking": True}, "messages": [{
            "role": "user", "content": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more "
                                       "than the ball. How much does the ball cost?"}]})
        m = msg_of(r)
        content, reasoning = (m.get("content") or ""), (m.get("reasoning_content") or "")
        results["thinking_on"] = {
            "pass": bool(reasoning.strip()) and any(s in content.lower() for s in ("0.05", "5 cents", "five cents")),
            "reasoning_chars": len(reasoning), "answer": content[-200:]}
        results["tokens_per_sec"] = round(r.get("timings", {}).get("predicted_per_second", 0), 1)

        # Thinking OFF: direct answer, no reasoning block
        m = msg_of(post(port, {**base, "chat_template_kwargs": {"enable_thinking": False}, "messages": [{
            "role": "user", "content": "What is 17 multiplied by 23? Reply with just the number."}]}))
        content, reasoning = (m.get("content") or ""), (m.get("reasoning_content") or "")
        results["thinking_off"] = {"pass": "391" in content and not reasoning.strip(), "answer": content[:200]}

        # Tool calling
        m = msg_of(post(port, {**base, "tools": TOOLS, "chat_template_kwargs": {"enable_thinking": False},
                               "messages": [{"role": "user", "content": "What's the weather in Paris right now?"}]}))
        calls = m.get("tool_calls") or []
        ok = any(c["function"]["name"] == "get_weather" and "paris" in c["function"]["arguments"].lower()
                 for c in calls)
        results["tool_call"] = {"pass": ok, "calls": [c["function"] for c in calls]}

        # Vision
        m = msg_of(post(port, {**base, "chat_template_kwargs": {"enable_thinking": False}, "messages": [{
            "role": "user", "content": [
                {"type": "text", "text": "What color is the square in this image? Answer with one word."},
                {"type": "image_url", "image_url": {"url": data_url}}]}]}))
        content = m.get("content") or ""
        results["vision"] = {"pass": "red" in content.lower(), "answer": content[:200]}
    except Exception as e:  # record the failure instead of crashing the whole run
        results["error"] = str(e)
    finally:
        proc.terminate()
        try:
            proc.wait(30)
        except subprocess.TimeoutExpired:
            proc.kill()
        log_f.close()
    return results


if not args.skip_functional:
    require(MMPROJ, "Run step 02 first.")
    for t in types:
        q = res["quants"].setdefault(t, {})
        fn = q.get("functional")
        # A run that ended in an error (server crash, busy port) is retried, not kept
        unchanged = fn is not None and "error" not in fn and (not gguf(t).exists() or is_current(fn, gguf(t)))
        if unchanged and not args.force:
            log(f"skip functional: {t} already tested")
            continue
        require(gguf(t), "Run step 05 first.")
        if fn is not None:
            log(f"  {t}: file changed since the last test, re-testing")
        log(f"functional tests: {t}")
        q["functional"] = functional(t)
        if "error" not in q["functional"]:
            q["functional"]["file"] = file_id(gguf(t))
        save_json(RES_FILE, res)
        f = q["functional"]
        log("  " + "  ".join(f"{k}={'PASS' if v.get('pass') else 'FAIL'}"
                             for k, v in f.items() if isinstance(v, dict) and k != "file")
            + f"  {f.get('tokens_per_sec')} tok/s"
            + (f"  ERROR: {f['error']}" if "error" in f else ""))

save_json(RES_FILE, res)  # also stores file identities adopted for older results
log(f"results saved to {RES_FILE}")
