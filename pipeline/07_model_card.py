"""Step 07: assemble the release folder and write the Hugging Face model card.

release/ holds exactly what will be uploaded (hard links, so no extra disk space):
quants, mmproj, imatrix, SHA256SUMS.txt and README.md built from the measured results.
Review release/README.md before running step 08.

    python pipeline/07_model_card.py
"""
import os
import shutil

from common import (BF16, CFG, IMATRIX, MMPROJ, NAME, OUT, REASONING_EFFORT, RELEASE, RESULTS, VISION,
                    gb, gguf, load_json, log, require)

qc, hf, mc = CFG["quantize"], CFG["hf"], CFG["model"]
cc = CFG.get("card", {})  # optional per-model card text; defaults reproduce the Qwen3.8-27B card
ev = load_json(RESULTS / "eval.json", {"base": {}, "quants": {}})
cal = load_json(RESULTS / "calibration_stats.json", {})
src = load_json(RESULTS / "source_manifest.json", {})
require(RESULTS / "checksums.json", "Run step 05 first.")

# ---- release folder (hard links) ----
RELEASE.mkdir(exist_ok=True)
files = [gguf(t) for t in qc["types"] if gguf(t).exists()] + ([MMPROJ] if VISION else []) + [IMATRIX, OUT / "SHA256SUMS.txt"]
def up_to_date(src, dst):
    # A hard link IS the source file. A copy (used when linking is not possible) is current
    # only if size and modification time match; a size check alone would keep a stale copy
    # of a rebuilt quant, since rebuilt quants have exactly the same size.
    if not dst.exists():
        return False
    if os.path.samefile(src, dst):
        return True
    a, b = src.stat(), dst.stat()
    return a.st_size == b.st_size and int(a.st_mtime) == int(b.st_mtime)


for f in files:
    require(f, "Run the earlier steps first.")
    dst = RELEASE / f.name
    if up_to_date(f, dst):
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
mmproj_gb = gb(MMPROJ.stat().st_size) if VISION else 0
ctx_gb = cc.get("context_gb", 2)  # GPU memory for ~8K tokens of context

NOTES = cc.get("notes") or {
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
OLLAMA_TESTED = "0.40.16"  # latest Ollama release tested; it could not load these files (Nov 2026)


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
    vram = gb(size) + mmproj_gb + ctx_gb  # 27B: ~2 GB for 8K context (hybrid attention keeps the KV cache small)
    rows.append(f"| [{f.name}](./{f.name}) | {t} | {gb(size):.1f} GB | {fmt(bpw, 2)} | ~{vram:.0f} GB | "
                f"{fmt(q.get('ppl'))} | {fmt(q.get('kld_mean'))} | {fmt(q.get('same_top'), 2)}% | {NOTES.get(t, '')} |")

func_rows = []
for t in qc["types"]:
    fn = ev["quants"].get(t, {}).get("functional")
    if not fn:
        continue
    mark = lambda k: "✅" if fn.get(k, {}).get("pass") else "❌"
    vision_cell = f"{mark('vision')} | " if VISION else ""
    func_rows.append(f"| {t} | {mark('thinking_on')} | {mark('thinking_off')} | {mark('tool_call')} | "
                     f"{vision_cell}{fn.get('tokens_per_sec', '—')} |")

base_ppl = ev["base"].get("ppl")
cal_rows = "\n".join(f"| {k} | `{v['repo']}` | {v['samples']} | {v['tokens']:,} |"
                     for k, v in cal.get("sources", {}).items())
repo = hf["repo_id"]
gh = f"\n**Pipeline code:** {hf['github_url']}\n" if hf.get("github_url") else ""
build = CFG["llama_cpp"]["build"]

# ---- model-specific text (defaults reproduce the Qwen3.8-27B card exactly) ----
tags = "\n".join(f"- {t}" for t in cc.get("tags", ["gguf", "qwen3.8", "quantized", "imatrix", "thinking",
                                                    "vision", "llama.cpp"]))
pipeline_tag = cc.get("pipeline_tag", "image-text-to-text" if VISION else "text-generation")
if VISION:
    features = "**thinking mode,\nvision (image input) and tool calling**"
    tested = "thinking on/off, tool calls, vision"
    vision_block = (f"**Vision:** also download [`{MMPROJ.name}`](./{MMPROJ.name}) ({mmproj_gb:.1f} GB); "
                    "it works with every quant above.\n\n")
    vram_note = "model + vision projector + ~8K context"
    func_intro = "Run through `llama-server` with the vision projector loaded (temperature 0):"
    func_head = ("| Quant | Thinking on | Thinking off | Tool call | Vision | Generation speed (tok/s, RTX 6000 Ada) |\n"
                 "|---|---|---|---|---|---|")
    func_empty = "| — | | | | | |"
    not_measured = "code, math, other languages, long context and image quality are not\nseparately measured."
    convert_note = f"; vision projector exported as {CFG['convert']['mmproj_outtype'].upper()}"
else:
    features = "**thinking mode and\ntool calling**"
    tested = "thinking on/off, tool calls"
    vision_block = ""
    vram_note = "model + ~8K context"
    func_intro = "Run through `llama-server` (temperature 0):"
    func_head = ("| Quant | Thinking on | Thinking off | Tool call | Generation speed (tok/s, RTX 6000 Ada) |\n"
                 "|---|---|---|---|---|")
    func_empty = "| — | | | | |"
    not_measured = "code, math, other languages and long context are not separately\nmeasured."
    convert_note = " (text-only model, no vision projector)"

gpu_guide = "\n".join(cc.get("gpu_guide") or [
    "- **32 GB+ GPU:** Q8_0 (practically identical to the original)",
    "- **24–32 GB GPU (RTX 3090/4090/5090):** Q6_K or Q5_K_M",
    "- **20–24 GB:** Q4_K_M (the usual default)",
    "- **16 GB:** IQ4_XS or Q3_K_M",
    "- **12 GB:** IQ3_M"])

if cc.get("ollama"):  # standard architecture: Ollama, LM Studio and other llama.cpp apps load it
    run_block = f"""**llama.cpp** (tested with build {build}):
```bash
llama-server -m {NAME}-Q4_K_M.gguf -ngl 99 -c 16384 --jinja
```

**Ollama** (tested with Ollama {cc['ollama']}): run a quant straight from this repository:
```bash
ollama run hf.co/{repo}:Q4_K_M
```

**LM Studio and other llama.cpp-based apps:** download any quant and load it; this is a standard
Qwen3 GGUF."""
elif not VISION:  # text-only model whose Ollama support has not been tested yet
    run_block = f"""**llama.cpp** (tested with build {build}):
```bash
llama-server -m {NAME}-Q4_K_M.gguf -ngl 99 -c 16384 --jinja
```

**Other llama.cpp-based apps** (LM Studio and others) can load these standard Qwen3 GGUF files."""
else:  # Qwen3.8-27B: vision model in a layout older runtimes cannot read
    run_block = f"""> **Compatibility:** these files need **llama.cpp build {build} or newer**. Recent llama.cpp
> stores some of this model's tensors in a combined layout (`attn_qkv_gate`, `ssm_beta_alpha`) that older
> runtimes cannot read. **Ollama {OLLAMA_TESTED} and older cannot load them** (error: `tensor 'blk.0.ssm_beta.weight'
> not found`). Other apps work once their bundled llama.cpp is at least build {build}.

**llama.cpp** (chat with image support; tested):
```bash
llama-server -m {NAME}-Q4_K_M.gguf --mmproj {MMPROJ.name} -ngl 99 -c 16384 --jinja
```

**Ollama:** not supported yet (see Compatibility). For Ollama, use its own library model instead:
`ollama run qwen3.8:27b`.

**LM Studio and other llama.cpp-based apps:** load a quant once the app's llama.cpp runtime is build
{build} or newer."""

if REASONING_EFFORT:
    thinking_block = f"""**Thinking mode** is on by default (reasoning effort `{REASONING_EFFORT[0]}`). Per request, with llama-server or any
OpenAI-compatible API:
- turn thinking off: `"chat_template_kwargs": {{"enable_thinking": false}}`
- shorter thinking: `"chat_template_kwargs": {{"reasoning_effort": "low"}}` ({', '.join(f'`{e}`' for e in REASONING_EFFORT[:-1])} or `{REASONING_EFFORT[-1]}`)"""
else:
    thinking_block = """**Thinking mode** is on by default. Per request, with llama-server or any OpenAI-compatible API:
- turn thinking off: `"chat_template_kwargs": {"enable_thinking": false}`
- or add `/no_think` to a message to answer without thinking (`/think` turns it back on)"""

imatrix_src = "the BF16 model" if CFG["imatrix"].get("source") == "bf16" else f"the {qc['reference']} quant"

# Optional section: accuracy by language (results of tools/kld_by_language.py)
lang_block = ""
lang = load_json(RESULTS / "kld_by_language.json", {}).get("langs", {})
if cc.get("language_results") and lang:
    names = [v["name"] for v in lang.values()]
    lrows = []
    for t in qc["types"]:
        e = ev["quants"].get(t, {}).get("kld_mean")
        cells = [fmt(v["quants"].get(t, {}).get("kld_mean")) for v in lang.values()]
        lrows.append(f"| {t} | {fmt(e)} | " + " | ".join(cells) + " |")
    lang_block = f"""
## Accuracy by language

Mean KL divergence against BF16 (lower is better) on held-out text in each language
({load_json(RESULTS / 'kld_by_language.json', {}).get('settings', {}).get('chunks', 80)} chunks × 512 tokens; English is the wikitext-2 test set above):

| Quant | English | {' | '.join(names)} |
|---|---|{'---|' * len(names)}
{chr(10).join(lrows)}
"""

# Optional card sections (off by default, so the Qwen3.8-27B card is unchanged)
language_yaml = "".join(f"- {code}\n" for code in cc.get("language", []))
language_yaml = f"language:\n{language_yaml}" if language_yaml else ""
top_block = ""
if cc.get("quick_start"):
    quick = (cc["quick_start"] if isinstance(cc["quick_start"], str)  # a tested command given in the config
             else f"ollama run hf.co/{repo}:Q4_K_M" if cc.get("ollama")
             else f"llama-server -hf {repo}:Q4_K_M -ngl 99 -c 16384 --jinja")
    top_block += f"## Quick start\n\n```bash\n{quick}\n```\n\n"
if cc.get("highlights"):
    top_block += "## Why these quants\n\n" + "\n".join(f"- {h}" for h in cc["highlights"]) + "\n\n"

tests_block = f"\n## Question tests\n\n{cc['test_summary'].strip()}\n" if cc.get("test_summary") else ""
if lang_block:  # other languages and code are measured below, so do not call them unmeasured
    not_measured = (("math, long context and image quality" if VISION else "math and long context")
                    + " are not separately measured (accuracy on Malayalam, Hindi and\ncode is in the next section).")

card = f"""---
base_model: {mc['repo_id']}
base_model_relation: quantized
license: {mc['license']}
pipeline_tag: {pipeline_tag}
library_name: gguf
quantized_by: {hf['username']}
{language_yaml}tags:
{tags}
---

# {NAME} GGUF (imatrix)

Quantized GGUF versions of [{mc['repo_id']}](https://huggingface.co/{mc['repo_id']}), with {features}. Every quant was **measured against the original BF16 model**
(perplexity + KL divergence) and **functionally tested** ({tested}).
{gh}
{top_block}## Files

| File | Type | Size | Bits/weight | VRAM* | PPL ↓ | Mean KLD ↓ | Same top token ↑ | Notes |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

{vision_block}\\*VRAM is approximate: {vram_note}. Longer context needs more.

**How to read the accuracy columns** (all measured against the original BF16 model, perplexity **{fmt(base_ppl)}**):
- **Mean KLD** (KL divergence): how far the quant's word probabilities are from the original's. Lower is better; 0 means identical. This is the most reliable measure.
- **Same top token:** how often the quant picks the same most-likely next word as the original.
- **PPL** (perplexity): how well the model predicts held-out text. Lower is better. The measurement
  uncertainty is about ±{fmt(ev['base'].get('ppl_err'), 2)}, so differences smaller than that (for example Q6_K vs BF16) are noise.

## Which file should I use?

{gpu_guide}

## How to run

{run_block}

{thinking_block}

## Functional tests

{func_intro}

{func_head}
{chr(10).join(func_rows) if func_rows else func_empty}

**Scope of the evaluation:** the functional tests are smoke tests (one prompt per feature) that confirm each
feature works; they do not score quality. Accuracy (perplexity, KL divergence) is measured on English
Wikipedia text at 512-token context, so {not_measured}
{lang_block}{tests_block}
## How these quants were made

1. Original weights: `{mc['repo_id']}` at commit `{src.get('commit', 'unknown')}` (SHA256-verified).
2. Converted to BF16 GGUF with llama.cpp `{build}`{convert_note}.
3. Importance matrix computed on {imatrix_src} using **{cal.get('total_tokens', 0):,} tokens** of calibration data,
   rendered with the model's own chat template (including `<think>` reasoning traces):

| Source | Dataset | Samples | Tokens |
|---|---|---|---|
{cal_rows}

4. All quants except {', '.join(qc['no_imatrix'])} use the importance matrix. The file [`{IMATRIX.name}`](./{IMATRIX.name}) is included.
5. Evaluated on the held-out **wikitext-2 test** split ({CFG['eval']['chunks']} chunks × {CFG['eval']['ctx']} tokens),
   with KL divergence against BF16 logits. Calibration used the train split only.

Checksums: [`SHA256SUMS.txt`](./SHA256SUMS.txt).

## License and credits

The model weights are licensed under **{LICENSE_NAMES.get(mc['license'], mc['license'])}**, the same as the original
[{mc['repo_id']}](https://huggingface.co/{mc['repo_id']}). All credit for the model goes to the Qwen team.
Quantized with [llama.cpp](https://github.com/ggml-org/llama.cpp).
"""
(RELEASE / "README.md").write_text(card, encoding="utf-8", newline="\n")
published = [f for f in RELEASE.iterdir() if f.is_file()]  # skips the uploader's hidden .cache folder
total = sum(f.stat().st_size for f in published)
log(f"release folder ready: {len(published)} files, {gb(total)} GB. Review {RELEASE / 'README.md'}")
