"""Measure how much each quant drifts from BF16 per language (KL divergence, same top token).

Same method as step 06 (llama-perplexity, BF16 reference logits, 512-token chunks), run on one
held-out text per language. English comes from step 06 (results/eval.json) and is not re-run.

    python tools/kld_by_language.py                       # all languages in TEXTS, all quants
    python tools/kld_by_language.py --langs ml --only Q4_K_M
    python tools/kld_by_language.py --keep-base           # keep the BF16 reference files (~10 GB each)

Texts (data/lang/, not in the calibration data):
    ml.txt    Malayalam Wikipedia articles (wikimedia/wikipedia 20231101.ml)
    hi.txt    Hindi Wikipedia articles (wikimedia/wikipedia 20231101.hi)
    code.txt  Python source from llama.cpp's own scripts (gguf-py, scripts/)

Output: results/kld_by_language.json and results/kld_by_language.md
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
from common import BF16, CFG, DATA, RESULTS, SHARED_DATA, gguf, load_json, log, require, run, save_json, tool  # noqa: E402

TEXTS = {"ml": ("Malayalam", SHARED_DATA / "lang" / "ml.txt"),  # shared by every model
         "hi": ("Hindi", SHARED_DATA / "lang" / "hi.txt"),
         "code": ("Python code", SHARED_DATA / "lang" / "code.txt")}

ap = argparse.ArgumentParser()
ap.add_argument("--langs", nargs="*", default=list(TEXTS))
ap.add_argument("--only", nargs="*", help="quant types (default: all in config.yaml)")
ap.add_argument("--chunks", type=int, default=80, help="512-token chunks per language (default 80)")
ap.add_argument("--keep-base", action="store_true", help="keep the BF16 reference logits after measuring")
ap.add_argument("--force", action="store_true", help="re-measure results that already exist")
args = ap.parse_args()

ev = CFG["eval"]
types = args.only or CFG["quantize"]["types"]
OUT = RESULTS / "kld_by_language.json"
res = load_json(OUT, {"settings": {}, "langs": {}})
res["settings"] = {"ctx": ev["ctx"], "chunks": args.chunks, "reference": "BF16",
                   "llama_cpp": CFG["llama_cpp"]["build"]}

NUM = r"([-\d.]+)"
PATTERNS = {  # same as pipeline/06_evaluate.py
    "ppl": rf"Mean PPL\(Q\)\s*:\s*{NUM}\s*±\s*{NUM}",
    "kld_mean": rf"Mean\s+KLD:\s*{NUM}\s*±\s*{NUM}",
    "kld_p999": rf"99\.9%\s+KLD:\s*{NUM}",
    "same_top": rf"Same top p:\s*{NUM}\s*±\s*{NUM}",
}


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


common_args = ["-c", ev["ctx"], "--chunks", args.chunks]
for lang in args.langs:
    name, text = TEXTS[lang]
    require(text, f"Missing test text for {name}.")
    entry = res["langs"].setdefault(lang, {"name": name, "base": {}, "quants": {}})
    todo = [t for t in types if args.force or "kld_mean" not in entry["quants"].get(t, {})]
    if not todo:
        log(f"skip {name}: all quants measured")
        continue
    base = DATA / f"kld_base_{lang}.bin"  # this model's BF16 reference logits (temporary)
    if not base.exists():
        require(BF16, "The BF16 GGUF is needed as the reference (step 02).")
        log(f"=== {name}: BF16 reference logits ({args.chunks} chunks)")
        out = run([tool("llama-perplexity"), "-m", BF16, "-f", text, "-ngl", ev["base_ngl"],
                   "--kl-divergence-base", base, *common_args], f"lang_kld_base_{lang}")
        m = re.findall(rf"Final estimate: PPL = {NUM} \+/- {NUM}", out)
        entry["base"] = {"ppl": float(m[-1][0]), "ppl_err": float(m[-1][1])} if m else {}
        save_json(OUT, res)
    for t in todo:
        require(gguf(t), "Run step 05 first.")
        out = run([tool("llama-perplexity"), "-m", gguf(t), "-ngl", ev["ngl"],
                   "--kl-divergence-base", base, "--kl-divergence", *common_args], f"lang_kld_{lang}_{t}")
        entry["quants"][t] = parse(out)
        save_json(OUT, res)
        q = entry["quants"][t]
        log(f"  {name:<11} {t:<7} mean KLD {q.get('kld_mean')}  same top {q.get('same_top')}%")
    if not args.keep_base:
        base.unlink(missing_ok=True)  # ~10 GB per language

# ---------- report ----------
eng = load_json(RESULTS / "eval.json", {"quants": {}})["quants"]
cols = [("English", {t: eng.get(t, {}) for t in types})] + \
       [(res["langs"][k]["name"], res["langs"][k]["quants"]) for k in TEXTS if k in res["langs"]]


def cell(q, key, pct=False):
    v = q.get(key)
    if v is None:
        return "—"
    return f"{100 - v:.2f}%" if pct else f"{v:.4f}"


L = [f"# Accuracy drop by language: {CFG['model']['name']}", "",
     f"KL divergence against BF16 per language, {ev['ctx']}-token chunks (English: {ev['chunks']} chunks of wikitext-2 "
     f"test, from step 06; other languages: {args.chunks} chunks). Lower is better in both tables.", "",
     "## Next token differs from BF16 (100% − same top token)", "",
     "| Type | " + " | ".join(c for c, _ in cols) + " |", "|---|" + "---|" * len(cols)]
L += [f"| {t} | " + " | ".join(cell(q.get(t, {}), "same_top", pct=True) for _, q in cols) + " |" for t in types]
L += ["", "## Mean KL divergence", "", "| Type | " + " | ".join(c for c, _ in cols) + " |", "|---|" + "---|" * len(cols)]
L += [f"| {t} | " + " | ".join(cell(q.get(t, {}), "kld_mean") for _, q in cols) + " |" for t in types]
L += ["", "Texts: English = wikitext-2 test; Malayalam and Hindi = Wikipedia articles (wikimedia/wikipedia, "
      "20231101); Python code = llama.cpp's own scripts. None of these texts is in the calibration data."]
(RESULTS / "kld_by_language.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
log(f"report: {RESULTS / 'kld_by_language.md'}")
