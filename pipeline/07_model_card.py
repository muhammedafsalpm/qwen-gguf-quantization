"""Step 07: assemble the release folder and write the Hugging Face model card.

release/ holds exactly what will be uploaded (hard links, so no extra disk space):
quants, mmproj, imatrix, SHA256SUMS.txt and README.md built from the measured results.
Review release/README.md before running step 08.

    python pipeline/07_model_card.py
"""
import os
import shutil

from common import (BF16, CFG, IMATRIX, MMPROJ, NAME, OUT, RELEASE, RESULTS, gb, gguf,
                    load_json, log, require)

qc, hf, mc = CFG["quantize"], CFG["hf"], CFG["model"]
ev = load_json(RESULTS / "eval.json", {"base": {}, "quants": {}})
cal = load_json(RESULTS / "calibration_stats.json", {})
src = load_json(RESULTS / "source_manifest.json", {})
require(RESULTS / "checksums.json", "Run step 05 first.")

# ---- release folder (hard links) ----
RELEASE.mkdir(exist_ok=True)
files = [gguf(t) for t in qc["types"] if gguf(t).exists()] + [MMPROJ, IMATRIX, OUT / "SHA256SUMS.txt"]
for f in files:
    require(f, "Run the earlier steps first.")
    dst = RELEASE / f.name
    if dst.exists() and dst.stat().st_size == f.stat().st_size:
        continue
    dst.unlink(missing_ok=True)
    try:
        os.link(f, dst)
    except OSError:
        shutil.copy2(f, dst)

# ---- numbers for the table ----
# Text-model parameter count from the BF16 GGUF (16 bits each). The safetensors total
# would also include the vision encoder, which lives in the separate mmproj file.
n_params = BF16.stat().st_size * 8 / 16 if BF16.exists() else 0
mmproj_gb = gb(MMPROJ.stat().st_size)

NOTES = {
    "Q8_0": "Near-lossless. Best accuracy",
    "Q6_K": "Excellent quality",
    "Q5_K_M": "Very high quality",
    "Q4_K_M": "**Recommended default.** Best balance",
    "IQ4_XS": "Best choice for 16 GB GPUs",
    "Q3_K_M": "16 GB GPUs with longer context",
    "IQ3_M": "12–16 GB GPUs",
    "IQ2_M": "Low VRAM; noticeable quality loss",
}


LICENSE_NAMES = {"apache-2.0": "Apache 2.0", "mit": "MIT"}


def fmt(v, nd=4):
    return "—" if v is None else f"{v:.{nd}f}"


rows = []
for t in qc["types"]:
    f = gguf(t)
    if not f.exists():
        continue
    q = ev["quants"].get(t, {})
    size = f.stat().st_size
    bpw = size * 8 / n_params if n_params else None
    vram = gb(size) + mmproj_gb + 2  # ~2 GB for 8K context (hybrid attention keeps the KV cache small)
    rows.append(f"| [{f.name}](./{f.name}) | {t} | {gb(size):.1f} GB | {fmt(bpw, 2)} | ~{vram:.0f} GB | "
                f"{fmt(q.get('ppl'))} | {fmt(q.get('kld_mean'))} | {fmt(q.get('same_top'), 2)}% | {NOTES.get(t, '')} |")

func_rows = []
for t in qc["types"]:
    fn = ev["quants"].get(t, {}).get("functional")
    if not fn:
        continue
    mark = lambda k: "✅" if fn.get(k, {}).get("pass") else "❌"
    func_rows.append(f"| {t} | {mark('thinking_on')} | {mark('thinking_off')} | {mark('tool_call')} | "
                     f"{mark('vision')} | {fn.get('tokens_per_sec', '—')} |")

base_ppl = ev["base"].get("ppl")
cal_rows = "\n".join(f"| {k} | `{v['repo']}` | {v['samples']} | {v['tokens']:,} |"
                     for k, v in cal.get("sources", {}).items())
repo = hf["repo_id"]
gh = f"\n**Pipeline code:** {hf['github_url']}\n" if hf.get("github_url") else ""

card = f"""---
base_model: {mc['repo_id']}
base_model_relation: quantized
license: {mc['license']}
pipeline_tag: image-text-to-text
library_name: gguf
quantized_by: {hf['username']}
tags:
- gguf
- qwen3.8
- quantized
- imatrix
- thinking
- vision
- llama.cpp
---

# {NAME} GGUF (imatrix)

Quantized GGUF versions of [{mc['repo_id']}](https://huggingface.co/{mc['repo_id']}), with **thinking mode,
vision (image input) and tool calling**. Every quant was **measured against the original BF16 model**
(perplexity + KL divergence) and **functionally tested** (thinking on/off, tool calls, vision).
{gh}
## Files

| File | Type | Size | Bits/weight | VRAM* | PPL ↓ | Mean KLD ↓ | Same top token ↑ | Notes |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

**Vision:** also download [`{MMPROJ.name}`](./{MMPROJ.name}) ({mmproj_gb:.1f} GB); it works with every quant above.

\\*VRAM is approximate: model + vision projector + ~8K context. Longer context needs more.

**How to read the accuracy columns** (all measured against the original BF16 model, perplexity **{fmt(base_ppl)}**):
- **Mean KLD** (KL divergence): how far the quant's word probabilities are from the original's. Lower is better; 0 means identical. This is the most reliable measure.
- **Same top token:** how often the quant picks the same most-likely next word as the original.
- **PPL** (perplexity): how well the model predicts held-out text. Lower is better. The measurement
  uncertainty is about ±{fmt(ev['base'].get('ppl_err'), 2)}, so differences smaller than that (for example Q6_K vs BF16) are noise.

## Which file should I use?

- **32 GB+ GPU:** Q8_0 (practically identical to the original)
- **24–32 GB GPU (RTX 3090/4090/5090):** Q6_K or Q5_K_M
- **20–24 GB:** Q4_K_M (the usual default)
- **16 GB:** IQ4_XS or Q3_K_M
- **12 GB:** IQ3_M

## How to run

**llama.cpp** (chat with image support):
```bash
llama-server -m {NAME}-Q4_K_M.gguf --mmproj {MMPROJ.name} -ngl 99 -c 16384 --jinja
```

**Ollama:**
```bash
ollama run hf.co/{repo}:Q4_K_M
```

**LM Studio:** search for `{repo}` and pick a quant.

**Thinking mode** is on by default (reasoning effort `xhigh`). Per request, with llama-server or any
OpenAI-compatible API:
- turn thinking off: `"chat_template_kwargs": {{"enable_thinking": false}}`
- shorter thinking: `"chat_template_kwargs": {{"reasoning_effort": "low"}}` (`xhigh`, `medium` or `low`)

## Functional tests

Run through `llama-server` with the vision projector loaded (temperature 0):

| Quant | Thinking on | Thinking off | Tool call | Vision | Generation speed (tok/s, RTX 6000 Ada) |
|---|---|---|---|---|---|
{chr(10).join(func_rows) if func_rows else "| — | | | | | |"}

## How these quants were made

1. Original weights: `{mc['repo_id']}` at commit `{src.get('commit', 'unknown')}` (SHA256-verified).
2. Converted to BF16 GGUF with llama.cpp `{CFG['llama_cpp']['build']}`; vision projector exported as {CFG['convert']['mmproj_outtype'].upper()}.
3. Importance matrix computed on the Q8_0 quant using **{cal.get('total_tokens', 0):,} tokens** of calibration data,
   rendered with the model's own chat template (including `<think>` reasoning traces):

| Source | Dataset | Samples | Tokens |
|---|---|---|---|
{cal_rows}

4. All quants except Q8_0 use the importance matrix. The file [`{IMATRIX.name}`](./{IMATRIX.name}) is included.
5. Evaluated on the held-out **wikitext-2 test** split ({CFG['eval']['chunks']} chunks × {CFG['eval']['ctx']} tokens),
   with KL divergence against BF16 logits. Calibration used the train split only.

Checksums: [`SHA256SUMS.txt`](./SHA256SUMS.txt).

## License and credits

The model weights are licensed under **{LICENSE_NAMES.get(mc['license'], mc['license'])}**, the same as the original
[{mc['repo_id']}](https://huggingface.co/{mc['repo_id']}). All credit for the model goes to the Qwen team.
Quantized with [llama.cpp](https://github.com/ggml-org/llama.cpp).
"""
(RELEASE / "README.md").write_text(card, encoding="utf-8")
total = sum(f.stat().st_size for f in RELEASE.iterdir() if f.is_file())
log(f"release/ ready: {len(list(RELEASE.iterdir()))} files, {gb(total)} GB. Review release/README.md")
