"""Step 03: build the calibration text (for the imatrix) and the evaluation text.

Calibration mixes general text, multi-turn chat, math, code, reasoning traces with
<think> blocks, and multilingual data, all rendered with the model's own chat template,
so the importance matrix protects every skill (including thinking mode).

Evaluation uses the held-out wikitext-2 TEST split (calibration uses TRAIN).

    python pipeline/03_calibration.py [--force]
"""
import argparse
import random

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer

from common import CALIB, CFG, DATA, EVAL_TEXT, MODEL_DIR, RESULTS, log, save_json

ap = argparse.ArgumentParser()
ap.add_argument("--force", action="store_true")
args = ap.parse_args()

cc = CFG["calibration"]
rng = random.Random(cc["seed"])
max_chars = cc["max_chars_per_sample"]
tok = AutoTokenizer.from_pretrained(MODEL_DIR)
if not tok.chat_template:
    raise SystemExit("Tokenizer has no chat template; cannot format chat samples.")


def fetch(repo: str, file: str) -> list[dict]:
    p = hf_hub_download(repo, file, repo_type="dataset", cache_dir=DATA / "hf_cache")
    return pq.read_table(p).to_pylist()


def clip(s: str, limit: int = max_chars) -> str:
    # Keep the start and the end of long samples, so reasoning traces still contain
    # both the opening <think> and the closing </think> + final answer.
    if len(s) <= limit:
        return s
    head = int(limit * 0.6)
    return s[:head] + "\n...\n" + s[-(limit - head):]


def chat(messages: list[dict], thinking: bool) -> str:
    # Match real usage: samples with reasoning traces use thinking mode (with a random
    # reasoning-effort level, as users would set it); plain answers use thinking off.
    kwargs = {"enable_thinking": thinking}
    if thinking:
        kwargs["reasoning_effort"] = rng.choice(["xhigh", "medium", "low"])
    return tok.apply_chat_template(messages, tokenize=False, **kwargs)


def samples(src: dict, rows: list[dict]):
    kind = src["kind"]
    limit = src.get("max_chars", max_chars)
    if kind == "plain":
        # wikitext rows are lines; join consecutive lines into ~2000-char passages
        buf = ""
        for r in rows:
            buf += r[src["text"]]
            if len(buf) >= 2000:
                yield buf.strip()
                buf = ""
        return
    rng.shuffle(rows)
    for r in rows:
        if kind == "messages":
            msgs = [{"role": m["role"], "content": clip(m["content"], limit)} for m in r[src["messages"]]]
            if msgs and all(m["content"] for m in msgs):
                yield chat(msgs, thinking=False)
        elif kind == "qa":
            q, a = r.get(src["prompt"]), r.get(src["response"])
            if not (q and a) or q.strip() in ("-", ""):
                continue
            assistant = {"role": "assistant", "content": clip(a, limit)}
            if "<think>" in a and "</think>" in a:
                # The chat template renders reasoning from a separate field
                reasoning, answer = a.split("</think>", 1)
                assistant = {"role": "assistant",
                             "reasoning_content": clip(reasoning.replace("<think>", "", 1).strip(), limit),
                             "content": clip(answer.strip(), limit // 2)}
            yield chat([{"role": "user", "content": clip(q, limit)}, assistant],
                       thinking="reasoning_content" in assistant)
        else:
            raise SystemExit(f"Unknown calibration kind: {kind}")


if CALIB.exists() and not args.force:
    log(f"skip: {CALIB.name} exists")
else:
    target = cc["target_tokens"]
    picked, stats = [], {}
    for src in cc["sources"]:
        budget = int(target * src["share"])
        rows = fetch(src["repo"], src["file"])
        n_tok = n = 0
        think = 0
        for text in samples(src, rows):
            t = len(tok(text, add_special_tokens=False)["input_ids"])
            picked.append(text)
            n_tok += t
            n += 1
            think += "<think>\n" in text and "<think>\n\n</think>" not in text  # real reasoning trace
            if n_tok >= budget:
                break
        stats[src["name"]] = {"repo": src["repo"], "samples": n, "tokens": n_tok, "with_think": think}
        log(f"  {src['name']:<13} {n:>5} samples  {n_tok:>7} tokens  ({src['repo']})")
    rng.shuffle(picked)  # interleave sources so every imatrix chunk sees a mix
    CALIB.write_text("\n\n".join(picked), encoding="utf-8", newline="\n")  # no CRLF on Windows
    total = sum(s["tokens"] for s in stats.values())
    save_json(RESULTS / "calibration_stats.json", {"total_tokens": total, "seed": cc["seed"], "sources": stats})
    log(f"wrote {CALIB.name}: {total} tokens from {len(stats)} sources")

if EVAL_TEXT.exists() and not args.force:
    log(f"skip: {EVAL_TEXT.name} exists")
else:
    ev = CFG["eval"]
    EVAL_TEXT.write_text("".join(r["text"] for r in fetch(ev["repo"], ev["file"])),
                         encoding="utf-8", newline="\n")
    log(f"wrote {EVAL_TEXT.name} ({EVAL_TEXT.stat().st_size // 1024} KB)")
