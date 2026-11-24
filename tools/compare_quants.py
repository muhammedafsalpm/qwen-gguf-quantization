"""Ask every quantized version the same questions and compare answers and latency.

Each quant is loaded in llama-server on its own (with the vision projector), warmed up,
then asked every prompt in tools/prompts.yaml with the same settings (temperature 0,
fixed seed). Answers are graded automatically where the prompt has a known answer, and
compared with the Q8_0 answer (the reference, practically identical to BF16).

    python tools/compare_quants.py                         # all quants, all prompts
    python tools/compare_quants.py --only Q4_K_M IQ3_M     # some quants
    python tools/compare_quants.py --prompts-only bat-ball multiply --repeats 1

Output: results/compare/<date-time>/report.md, results.csv, results.json
"""
import argparse
import base64
import csv
import difflib
import json
import re
import socket
import statistics
import struct
import subprocess
import sys
import time
import urllib.request
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
from common import CFG, EVAL_TEXT, LOGS, MMPROJ, RESULTS, gguf, log, require, tool  # noqa: E402

PROMPTS_FILE = Path(__file__).resolve().parent / "prompts.yaml"
REFERENCE = CFG["quantize"]["reference"]  # Q8_0

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--only", nargs="*", help="quant types to test (default: all in config.yaml)")
ap.add_argument("--prompts-only", nargs="*", help="prompt ids to run (default: all)")
ap.add_argument("--repeats", type=int, help="timing runs per prompt (default: from prompts.yaml)")
ap.add_argument("--prompts", type=Path, default=PROMPTS_FILE, help="prompt file to use")
ap.add_argument("--port", type=int, default=8090)
args = ap.parse_args()

import yaml  # noqa: E402

spec = yaml.safe_load(args.prompts.read_text(encoding="utf-8"))
settings = spec.get("settings", {})
repeats = args.repeats or settings.get("repeats", 2)
ctx, seed = settings.get("ctx", 16384), settings.get("seed", 42)
prompts = [p for p in spec["prompts"] if not args.prompts_only or p["id"] in args.prompts_only]
types = args.only or CFG["quantize"]["types"]
if not prompts:
    sys.exit("No prompts selected.")
for t in types:
    require(gguf(t), "Build the quants first (run_all.py).")
require(MMPROJ, "The vision projector is missing (run step 02).")

OUT_DIR = RESULTS / "compare" / time.strftime("%Y%m%d-%H%M%S")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------- inputs that are generated, not typed ----------
def bar_chart_png() -> bytes:
    """320x240 white image with red, green (tallest) and blue bars. No extra libraries."""
    w, h = 320, 240
    bars = [(40, 110, 140, (220, 40, 40)), (130, 200, 40, (40, 170, 60)), (220, 290, 100, (40, 80, 220))]
    rows = []
    for y in range(h):
        row = bytearray(b"\x00")
        for x in range(w):
            px = (255, 255, 255)
            for x0, x1, top_y, color in bars:
                if x0 <= x < x1 and top_y <= y < 220:
                    px = color
            if y == 220:
                px = (0, 0, 0)
            row += bytes(px)
        rows.append(bytes(row))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))


def long_text() -> str:
    """About 7K tokens of held-out Wikipedia text with one fact hidden in the middle."""
    base = EVAL_TEXT.read_text(encoding="utf-8")[:28000] if EVAL_TEXT.exists() else ("Filler sentence. " * 1800)
    mid = len(base) // 2
    return base[:mid] + "\nThe access code for the vault is 7341.\n" + base[mid:]


IMAGES = {"bars": "data:image/png;base64," + base64.b64encode(bar_chart_png()).decode()}
LONG = long_text()
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def image_url(name: str) -> str:
    """'bars' is generated; anything else is an image file path relative to the prompts file."""
    if name in IMAGES:
        return IMAGES[name]
    f = (args.prompts.resolve().parent / name)
    require(f, f"Image for a prompt is missing: {name}")
    return f"data:{MIME.get(f.suffix.lower(), 'image/png')};base64," + base64.b64encode(f.read_bytes()).decode()


def build_messages(p: dict) -> list:
    text = p["prompt"]
    if p.get("long_text"):
        text = LONG + "\n\n" + text
    if p.get("image"):
        return [{"role": "user", "content": [{"type": "text", "text": text},
                                             {"type": "image_url", "image_url": {"url": image_url(p["image"])}}]}]
    return [{"role": "user", "content": text}]


# ---------- grading ----------
def last_number(s: str):
    nums = re.findall(r"-?\d+(?:\.\d+)?", s.replace(",", ""))
    return float(nums[-1]) if nums else None


def run_python(answer: str, tests: str) -> bool:
    # Answers may quote the original code or put tests in a separate block, so every code block is
    # tried on its own; the answer passes if any block passes the tests.
    blocks = re.findall(r"```(?:python|py)?[ \t]*\n(.*?)```", answer, re.S) or [answer]
    for code in blocks:
        try:
            r = subprocess.run([sys.executable, "-I", "-c", code + "\n" + tests],
                               capture_output=True, text=True, timeout=10)
            if r.returncode == 0:
                return True
        except subprocess.TimeoutExpired:
            pass
    return False


def norm(s: str) -> str:
    """Lower case without thousands separators or markdown emphasis, so '₹11,280' and '**11280**' match."""
    return s.lower().replace(",", "").replace("*", "")


def grade(p: dict, content: str, calls: list):
    c = p.get("check", {"type": "manual"})
    kind = c["type"]
    if kind == "contains":
        text = norm(content)
        if "all" in c and not all(norm(s) in text for s in c["all"]):
            return False
        return any(norm(s) in text for s in c["any"]) if "any" in c else True
    if kind == "regex":  # every pattern must match (case-insensitive)
        text = norm(content)
        return all(re.search(pat, text, re.I | re.S) for pat in c["all"])
    if kind == "number":
        return last_number(content) == float(c["value"])
    if kind == "bullets":
        n = sum(1 for line in content.splitlines() if re.match(r"\s*([-*•]|\d+[.)])\s+\S", line))
        return n == c["count"]
    if kind == "tool_call":
        return any(x.get("name") == c["name"] and c["arg_contains"].lower() in str(x.get("arguments", "")).lower()
                   for x in calls)  # calls = the "function" part of each tool call (see ask())
    if kind == "python":
        return run_python(content, c["tests"])
    return None  # manual: not graded


# ---------- llama-server ----------
def port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", port)) == 0


def post(body: dict, timeout=1200) -> dict:
    req = urllib.request.Request(f"http://127.0.0.1:{args.port}/v1/chat/completions",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def start_server(t: str):
    if port_in_use(args.port):
        sys.exit(f"Port {args.port} is already in use. Stop the other server or pass --port.")
    log_f = open(LOGS / f"compare_server_{t}.log", "w", encoding="utf-8", errors="replace")
    proc = subprocess.Popen([tool("llama-server"), "-m", str(gguf(t)), "--mmproj", str(MMPROJ),
                             "-ngl", "99", "-c", str(ctx), "-np", "1", "--host", "127.0.0.1",
                             "--port", str(args.port), "--jinja"], stdout=log_f, stderr=subprocess.STDOUT)
    t0 = time.time()
    while time.time() - t0 < 900:
        if proc.poll() is not None:
            log_f.close()
            sys.exit(f"llama-server stopped while loading {t}; see logs/compare_server_{t}.log")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{args.port}/health", timeout=5) as r:
                if r.status == 200:
                    return proc, log_f, time.time() - t0
        except Exception:
            pass
        time.sleep(2)
    proc.kill()
    sys.exit(f"llama-server did not become ready for {t}")


def stop_server(proc, log_f):
    proc.terminate()
    try:
        proc.wait(30)
    except subprocess.TimeoutExpired:
        proc.kill()
    log_f.close()


def ask(p: dict) -> dict:
    body = {"messages": build_messages(p), "temperature": 0, "seed": seed,
            "max_tokens": p.get("max_tokens", 1024),
            "chat_template_kwargs": {"enable_thinking": bool(p.get("thinking"))}}
    if p.get("tools"):
        body["tools"] = p["tools"]
    t0 = time.perf_counter()
    r = post(body)
    wall = time.perf_counter() - t0
    m, tm = r["choices"][0]["message"], r.get("timings", {})
    return {"content": m.get("content") or "", "reasoning": m.get("reasoning_content") or "",
            "calls": [c["function"] for c in (m.get("tool_calls") or [])],
            "finish": r["choices"][0].get("finish_reason"), "wall_s": wall,
            "prefill_ms": tm.get("prompt_ms"), "prompt_tokens": tm.get("prompt_n"),
            "gen_tokens": tm.get("predicted_n"), "tok_s": tm.get("predicted_per_second")}


# ---------- run ----------
results = {"settings": {"repeats": repeats, "ctx": ctx, "seed": seed, "temperature": 0,
                        "llama_cpp": CFG["llama_cpp"]["build"], "prompts_file": str(args.prompts)},
           "quants": {}}
order = sorted(types, key=lambda t: t != REFERENCE)  # reference first, so similarity can be computed as we go
for t in order:
    log(f"=== {t}: loading")
    proc, log_f, load_s = start_server(t)
    q = results["quants"][t] = {"load_s": round(load_s, 1), "answers": {}}
    try:
        ask({"prompt": "Say OK.", "max_tokens": 8})  # warm-up, not counted
        for p in prompts:
            runs = [ask(p) for _ in range(repeats)]
            first = runs[0]
            avg = lambda k: round(statistics.mean(x[k] for x in runs if x[k] is not None), 2) \
                if any(x[k] is not None for x in runs) else None
            entry = {
                "category": p.get("category", ""), "thinking": bool(p.get("thinking")),
                "content": first["content"], "reasoning_chars": len(first["reasoning"]),
                "calls": first["calls"], "finish": first["finish"],
                "correct": grade(p, first["content"], first["calls"]),
                "wall_s": avg("wall_s"), "prefill_ms": avg("prefill_ms"), "tok_s": avg("tok_s"),
                "gen_tokens": avg("gen_tokens"), "prompt_tokens": first["prompt_tokens"],
            }
            ref = results["quants"].get(REFERENCE, {}).get("answers", {}).get(p["id"])
            entry["similarity_to_ref"] = round(difflib.SequenceMatcher(
                None, ref["content"], entry["content"]).ratio(), 3) if ref else None
            q["answers"][p["id"]] = entry
            mark = {True: "PASS", False: "FAIL", None: "manual"}[entry["correct"]]
            log(f"  {p['id']:<16} {mark:<6} {entry['wall_s']:>6} s  {entry['tok_s']} tok/s"
                + ("  (hit max_tokens)" if entry["finish"] == "length" else ""))
    finally:
        stop_server(proc, log_f)
    (OUT_DIR / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False),
                                          encoding="utf-8", newline="\n")


# ---------- report ----------
def mean_of(t, key):
    vals = [a[key] for a in results["quants"][t]["answers"].values() if a[key] is not None]
    return round(statistics.mean(vals), 2) if vals else None


graded = [p["id"] for p in prompts if p.get("check", {}).get("type", "manual") != "manual"]
with open(OUT_DIR / "results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["quant", "prompt", "category", "thinking", "correct", "wall_s", "prefill_ms", "tok_s",
                "gen_tokens", "prompt_tokens", "reasoning_chars", "similarity_to_q8_0", "answer"])
    for t in types:
        for pid, a in results["quants"][t]["answers"].items():
            w.writerow([t, pid, a["category"], a["thinking"], a["correct"], a["wall_s"], a["prefill_ms"],
                        a["tok_s"], a["gen_tokens"], a["prompt_tokens"], a["reasoning_chars"],
                        a["similarity_to_ref"], a["content"]])

L = [f"# Quant comparison: {CFG['model']['name']}", "",
     f"{len(prompts)} prompts × {len(types)} quants, temperature 0, seed {seed}, context {ctx}, "
     f"{repeats} timing run(s) per prompt, llama.cpp {CFG['llama_cpp']['build']}. "
     f"Similarity is measured against the {REFERENCE} answer (1.0 = identical text).", "",
     "## Summary", "",
     "| Quant | Correct | Avg total time (s) | Avg first-token / prefill (ms) | Avg generation (tok/s) | Avg similarity to Q8_0 | Load time (s) |",
     "|---|---|---|---|---|---|---|"]
for t in types:
    ans = results["quants"][t]["answers"]
    ok = sum(1 for pid in graded if ans.get(pid, {}).get("correct"))
    sims = [a["similarity_to_ref"] for a in ans.values() if a["similarity_to_ref"] is not None]
    L.append(f"| {t} | {ok}/{len(graded)} | {mean_of(t, 'wall_s')} | {mean_of(t, 'prefill_ms')} | "
             f"{mean_of(t, 'tok_s')} | {round(statistics.mean(sims), 3) if sims else '—'} | {results['quants'][t]['load_s']} |")

L += ["", "## Per prompt: correct and total time (s)", "",
      "| Prompt | Category | " + " | ".join(types) + " |", "|---|---|" + "---|" * len(types)]
for p in prompts:
    cells = []
    for t in types:
        a = results["quants"][t]["answers"][p["id"]]
        mark = {True: "✅", False: "❌", None: "·"}[a["correct"]]
        cells.append(f"{mark} {a['wall_s']}")
    L.append(f"| {p['id']} | {p.get('category', '')} | " + " | ".join(cells) + " |")
L += ["", "✅ correct · ❌ wrong · · not graded (compare by reading)", "", "## Answers side by side", ""]
for p in prompts:
    L += [f"### {p['id']} ({p.get('category', '')})", "", f"> {p['prompt'][:300]}", ""]
    for t in types:
        a = results["quants"][t]["answers"][p["id"]]
        shown = a["content"].strip() or json.dumps(a["calls"], ensure_ascii=False)
        sim = f", similarity {a['similarity_to_ref']}" if a["similarity_to_ref"] is not None and t != REFERENCE else ""
        L += [f"<details><summary><b>{t}</b> — {a['wall_s']} s, {a['gen_tokens']} tokens{sim}</summary>", "",
              "```text", shown[:2000], "```", "", "</details>", ""]
(OUT_DIR / "report.md").write_text("\n".join(L), encoding="utf-8", newline="\n")
log(f"report: {OUT_DIR / 'report.md'}")
