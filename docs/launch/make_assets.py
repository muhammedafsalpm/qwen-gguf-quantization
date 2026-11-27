"""Build the launch assets (CSV tables and charts) from the measured results.

Every number comes from results/ (eval.json, kld_by_language.json) or from the verified
question-test tables in the model cards. Nothing is typed in by hand except those verified scores.

    python docs/launch/make_assets.py

Output: docs/launch/data/*.csv and docs/launch/images/*.png
"""
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
(OUT / "data").mkdir(exist_ok=True)
(OUT / "images").mkdir(exist_ok=True)

TYPES = ["Q8_0", "Q6_K", "Q5_K_M", "Q4_K_M", "IQ4_XS", "Q3_K_M", "IQ3_M"]
MODELS = {  # name: (results folder, out folder, HF repo)
    "Qwen3.8-27B": (ROOT / "results", ROOT / "out", "muhammed-afsal-p-m/Qwen3.8-27B-GGUF"),
    "Qwen3-14B": (ROOT / "results/Qwen3-14B", ROOT / "out/Qwen3-14B", "muhammed-afsal-p-m/Qwen3-14B-GGUF"),
    "Qwen3-8B": (ROOT / "results/Qwen3-8B", ROOT / "out/Qwen3-8B", "muhammed-afsal-p-m/Qwen3-8B-GGUF"),
}
# Verified by reading the answers (same tables as the Hugging Face model cards)
TESTS = {
    "Qwen3.8-27B": {"total": (13, 19, 14), **{t: (13, 19, 14) for t in TYPES}},
    "Qwen3-14B": {"total": (12, 17, 14), "Q8_0": (12, 17, 14), "Q6_K": (12, 17, 14), "Q5_K_M": (12, 17, 14),
                  "Q4_K_M": (12, 17, 14), "IQ4_XS": (11, 17, 14), "Q3_K_M": (11, 17, 14), "IQ3_M": (11, 17, 13)},
    "Qwen3-8B": {"total": (12, 17, 14), "Q8_0": (11, 15, 14), "Q6_K": (12, 16, 14), "Q5_K_M": (12, 16, 14),
                 "Q4_K_M": (12, 17, 13), "IQ4_XS": (12, 16, 14), "Q3_K_M": (11, 16, 14), "IQ3_M": (12, 17, 12)},
}

rows, lang_rows, test_rows = [], [], []
for name, (res, out, repo) in MODELS.items():
    ev = json.loads((res / "eval.json").read_text(encoding="utf-8"))
    lang = json.loads((res / "kld_by_language.json").read_text(encoding="utf-8"))["langs"]
    params = (out / f"{name}-BF16.gguf").stat().st_size * 8 / 16
    for t in TYPES:
        q = ev["quants"][t]
        size = (out / f"{name}-{t}.gguf").stat().st_size
        fn = q.get("functional", {})
        rows.append({
            "model": name, "quant": t, "file": f"{name}-{t}.gguf", "hf_repo": repo,
            "size_gb": round(size / 1e9, 2), "bits_per_weight": round(size * 8 / params, 2),
            "perplexity": round(q["ppl"], 4), "bf16_perplexity": ev["base"]["ppl"],
            "mean_kld": round(q["kld_mean"], 6), "kld_p99_9": round(q["kld_p999"], 4),
            "same_top_token_pct": round(q["same_top"], 2), "gen_tokens_per_sec": fn.get("tokens_per_sec"),
            "thinking_on": fn.get("thinking_on", {}).get("pass"), "thinking_off": fn.get("thinking_off", {}).get("pass"),
            "tool_call": fn.get("tool_call", {}).get("pass"), "vision": fn.get("vision", {}).get("pass"),
        })
        lang_rows.append({"model": name, "quant": t, "english": round(q["kld_mean"], 6),
                          **{v["name"].lower().replace(" ", "_"): round(v["quants"][t]["kld_mean"], 6)
                             for v in lang.values()}})
        b, e, m = TESTS[name][t]
        tb, te, tm = TESTS[name]["total"]
        test_rows.append({"model": name, "quant": t, "basic": b, "basic_total": tb, "extended": e,
                          "extended_total": te, "multilingual": m, "multilingual_total": tm})


def write_csv(path, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]))
        w.writeheader()
        w.writerows(data)


write_csv(OUT / "data/quant_results.csv", rows)
write_csv(OUT / "data/kld_by_language.csv", lang_rows)
write_csv(OUT / "data/question_tests.csv", test_rows)

# ---------- charts: plain matplotlib, one consistent style ----------
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 150})
COLORS = {"Qwen3.8-27B": "#1f77b4", "Qwen3-14B": "#ff7f0e", "Qwen3-8B": "#2ca02c"}
NOTE = "Measured with llama.cpp b12345 against each model's BF16 weights (wikitext-2 test, 150 x 512 tokens)."

# 1. accuracy loss vs file size
fig, ax = plt.subplots(figsize=(8, 5))
for name in MODELS:
    pts = [r for r in rows if r["model"] == name]
    ax.plot([r["size_gb"] for r in pts], [r["mean_kld"] for r in pts], "o-", color=COLORS[name], label=name)
    for r in pts:
        if r["quant"] in ("Q8_0", "Q4_K_M", "IQ3_M"):
            ax.annotate(r["quant"], (r["size_gb"], r["mean_kld"]), textcoords="offset points",
                        xytext=(5, 5), fontsize=8, color="#444")
ax.set_yscale("log")
ax.set_xlabel("File size (GB)")
ax.set_ylabel("Mean KL divergence vs BF16 (log scale, lower is better)")
ax.set_title("How much each GGUF file drifts from the original model")
ax.legend(frameon=False)
fig.text(0.01, 0.01, NOTE, fontsize=7, color="#666")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(OUT / "images/kld_vs_size.png")
plt.close(fig)

# 2. same top token per quant
fig, ax = plt.subplots(figsize=(8, 5))
x = range(len(TYPES))
w = 0.27
for i, name in enumerate(MODELS):
    vals = [next(r["same_top_token_pct"] for r in rows if r["model"] == name and r["quant"] == t) for t in TYPES]
    ax.bar([k + (i - 1) * w for k in x], vals, w, color=COLORS[name], label=name)
ax.set_xticks(list(x), TYPES)
ax.set_ylim(80, 100)
ax.set_ylabel("Same top token as BF16 (%)")
ax.set_title("How often each quant picks the same next token as the original")
ax.legend(frameon=False, loc="upper right")
fig.text(0.01, 0.01, NOTE, fontsize=7, color="#666")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(OUT / "images/same_top_token.png")
plt.close(fig)

# 3. languages at Q4_K_M
langs = [("english", "English"), ("malayalam", "Malayalam"), ("hindi", "Hindi"), ("python_code", "Python code")]
fig, ax = plt.subplots(figsize=(8, 5))
for i, name in enumerate(MODELS):
    r = next(r for r in lang_rows if r["model"] == name and r["quant"] == "Q4_K_M")
    ax.bar([k + (i - 1) * w for k in range(len(langs))], [r[k] for k, _ in langs], w, color=COLORS[name], label=name)
ax.set_xticks(range(len(langs)), [n for _, n in langs])
ax.set_ylabel("Mean KL divergence vs BF16 (lower is better)")
ax.set_title("Q4_K_M accuracy loss by language")
ax.legend(frameon=False)
fig.text(0.01, 0.01, "English: wikitext-2 test (150 x 512 tokens). Malayalam, Hindi: Wikipedia; code: llama.cpp scripts (80 x 512 tokens each). "
         "None of these texts is in the calibration data.", fontsize=7, color="#666")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(OUT / "images/kld_by_language_q4.png")
plt.close(fig)

# 4. speed vs size
fig, ax = plt.subplots(figsize=(8, 5))
for name in MODELS:
    pts = [r for r in rows if r["model"] == name]
    ax.plot([r["size_gb"] for r in pts], [r["gen_tokens_per_sec"] for r in pts], "o-", color=COLORS[name], label=name)
ax.set_xlabel("File size (GB)")
ax.set_ylabel("Generation speed (tokens/s)")
ax.set_title("Generation speed on one RTX 6000 Ada (48 GB)")
ax.legend(frameon=False)
fig.text(0.01, 0.01, "llama-server, temperature 0, all layers on GPU. Speeds on other GPUs will differ.",
         fontsize=7, color="#666")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(OUT / "images/speed_vs_size.png")
plt.close(fig)

print(f"{len(rows)} rows -> {OUT / 'data'}; 4 charts -> {OUT / 'images'}")
