# Qwen GGUF Quantization

A reproducible pipeline that converts official Qwen models into importance-matrix (imatrix) GGUF
quantizations, measures every quant against the original BF16 model, tests thinking, tool calling and
(for vision models) image input, and publishes the results to Hugging Face.

## Models

| Model | Original | Config | Input | Quantized model |
|---|---|---|---|---|
| Qwen3.8-27B | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | [`config.yaml`](config.yaml) | Text + images | [muhammed-afsal-p-m/Qwen3.8-27B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3.8-27B-GGUF) |
| Qwen3-8B | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | [`configs/qwen3-8b.yaml`](configs/qwen3-8b.yaml) | Text | [muhammed-afsal-p-m/Qwen3-8B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3-8B-GGUF) |
| Qwen3-14B | [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) | [`configs/qwen3-14b.yaml`](configs/qwen3-14b.yaml) | Text | [muhammed-afsal-p-m/Qwen3-14B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3-14B-GGUF) |

Each model has its own configuration file and its own output folders, so models never overwrite each other.

---

## Contents

- [Models](#models)
- [Features](#features)
- [Quantization explained](#quantization-explained)
- [Quantization types](#quantization-types)
- [Results](#results)
- [Pipeline](#pipeline)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Methodology](#methodology)
- [Project structure](#project-structure)
- [FAQ](#faq)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Verified source:** every original weight file is checked by SHA256 against the Hugging Face repository,
  and the exact commit is recorded.
- **Calibrated quantization:** the importance matrix is built from a mixed calibration set (general text,
  multi-turn chat, math, code, `<think>` reasoning traces and multilingual data), rendered with the model's
  own chat template so both thinking and non-thinking modes are represented.
- **Measured accuracy:** perplexity and KL divergence of every quant against BF16 logits, on held-out text.
- **Functional tests:** thinking on, thinking off, tool calling and (for vision models) image input, run through `llama-server`.
- **Vision support:** for vision models, the multimodal projector (`mmproj`) is exported alongside the text model.
- **Resumable:** every step skips work that is already complete, so an interrupted run continues where it stopped.
- **One configuration file per model:** [`config.yaml`](config.yaml) for Qwen3.8-27B and
  [`configs/`](configs/) for the other models; all settings live there, not in code.

## Quantization explained

This section is for readers who are new to quantization.

### What is a model?

A language model is a very large collection of numbers called **weights**. Qwen3.8-27B has about
**27 billion** of them. Running the model means doing arithmetic with all of these numbers, so how
precisely each number is stored decides how large the model file is and how much GPU memory it needs.

### What is quantization?

Quantization stores each weight with **fewer bits**. Think of storing the number 3.14159265:

| Precision | Stored as | Comparable to |
|---|---|---|
| 16 bits (BF16) | 3.1416 | The original photo |
| 8 bits | 3.14 | A high-quality JPEG: no visible difference |
| 4 bits | 3.1 | A smaller JPEG: small differences when you zoom in |
| 2 bits | 3 | A heavily compressed JPEG: visible blur |

Fewer bits give a **smaller file**, **less GPU memory** and **faster generation**, at the cost of a small
loss in accuracy. Good quantization keeps that loss as small as possible.

### The original model: BF16 and safetensors

Qwen releases the model in **BF16** ("Brain Float 16"): 16 bits, or 2 bytes, per weight.
27 billion weights × 2 bytes ≈ **54 GB**. This full-precision version is the master copy that every
quantized version is made from.

The weights are stored as **safetensors** files, the standard format on Hugging Face, split into
18 parts for easier downloading. Safetensors is used by Python libraries such as PyTorch and
Transformers. Running it requires a GPU with more than 54 GB of memory.

### The formats this pipeline produces: GGUF and mmproj

**GGUF** is the file format of [llama.cpp](https://github.com/ggml-org/llama.cpp), used by Ollama,
LM Studio and most local AI applications. A GGUF file contains everything needed to run the model
in a single file: the weights, the model settings, the tokenizer and the chat template. It supports
quantized weights and runs without Python, on GPU or CPU.

**mmproj** (multimodal projector) is a small, separate GGUF file that contains the **vision** part of
the model. It turns an image into tokens that the language model can read:

```
Image ──► mmproj (vision encoder) ──► image tokens ─┐
                                                    ├──► language model ──► answer
Text  ──────────────────────────────► text tokens ──┘
```

One mmproj file works with every quantized version. It is kept at 16-bit precision because it is small
and image understanding is sensitive to precision. It is only needed for image input; text-only use
does not require it.

| | Safetensors (original) | GGUF model | mmproj GGUF |
|---|---|---|---|
| Contains | Weights only, in 18 files | Language model, tokenizer and settings, in 1 file | Vision encoder, in 1 file |
| Size | ~54 GB | 54 GB (BF16) down to ~12.5 GB (quantized) | ~0.9 GB |
| Used by | PyTorch, Transformers | llama.cpp, Ollama, LM Studio | The same apps, for image input |
| Quantized | No | Yes | No (kept at F16) |

### What changes, and what does not

Quantization compresses **almost the entire model**, but not every part equally:

| Part of the model | Treatment | Reason |
|---|---|---|
| Large weight matrices (attention and feed-forward blocks in every layer) | Compressed | They hold over 99% of the weights, so this is where the size reduction comes from |
| Small normalization tensors (`attn_norm`, `q_norm`, `post_attention_norm`, ...) | Kept at full precision | They are tiny but sensitive; compressing them saves nothing and can hurt quality |
| Model structure (layers, architecture, vocabulary, chat template, thinking mode) | Unchanged | Only the way numbers are stored changes |

A useful picture: quantization is like reprinting a large book in a smaller font. Every page is still
there, in the same order, telling the same story. Only the way the letters are printed changes, and
the most important headings keep their original size.

### Reading the quantization names

A name such as **`Q4_K_M`** has three parts:

```
 Q4   _   K   _   M
 │        │       │
 │        │       └── mix size: S (small), M (medium) or L (large)
 │        └────────── method: K = "k-quant"
 └─────────────────── approximate bits per weight
```

- **The number (Q8, Q6, Q5, Q4, Q3):** the approximate number of bits per weight. A higher number means
  a larger file and higher accuracy.
- **`_0`:** the original, simple method. Every weight in a block is treated the same way. At 8 bits this
  is still the best choice, because 8 bits is already precise enough.
- **`_K` (k-quants):** a smarter method. Weights are grouped into blocks, and blocks into super-blocks,
  so the scaling information is stored efficiently. More sensitive tensors (for example `attn_v`,
  `ffn_down` and the output layer) receive more bits than less sensitive ones. `Q4_K_M` is therefore
  about 4.8 bits on average, not 4 bits everywhere.
- **`_S`, `_M`, `_L`:** how many sensitive tensors are given extra bits. `M` (medium) is the usual
  balance between size and accuracy.
- **`IQ` (i-quants):** the newest method. Instead of storing each value directly, it stores references to
  a table of common value patterns (a codebook), similar to how a ZIP file replaces repeated text with
  short codes. This gives better quality at low bit rates (2–4 bits). I-quants depend on an importance
  matrix to work well. Sizes are named `XS` (extra small), `S` and `M`.

**Why Q8_0 is 8.5 bits per weight, not 8:** weights are stored in blocks of 32, and each block also stores
one scale value that says how large the numbers in that block are. That extra value adds about 0.5 bits
per weight.

### The importance matrix (imatrix)

Before summarizing a textbook, you might highlight the most important sentences so you know what to keep
in full detail. The importance matrix does the same for the model:

1. The model reads a varied calibration text (chat, code, math, reasoning, many languages).
2. It records which weights have the most influence on the output.
3. During quantization, those weights are rounded more carefully.

The result is better accuracy at the same file size, especially at 4 bits and below.

### How the versions are made

Every quantized version is made **directly from the BF16 original**. The Q8_0 file is never used as a
source for the smaller versions:

```
                    ┌──► Q8_0  (made first)
                    │
BF16 (original) ────┼──► Q6_K
  ~54 GB            ├──► Q5_K_M
                    ├──► Q4_K_M
                    ├──► IQ4_XS
                    ├──► Q3_K_M
                    └──► IQ3_M

Q8_0 ──► importance matrix ──► used as a guide when making Q6_K … IQ3_M from BF16
```

Each compression loses a little detail. Compressing an already-compressed file would add a second loss,
like saving a JPEG, reopening it and saving it again at lower quality. Starting from the original every
time means each version loses detail only once.

Q8_0 has one extra job: it is the model that reads the calibration text to build the importance matrix.
It fits entirely in a 48 GB GPU (BF16 does not) and is practically identical to BF16, so the importance
matrix stays accurate.

```bash
llama-quantize --imatrix Qwen3.8-27B.imatrix.gguf  Qwen3.8-27B-BF16.gguf  Qwen3.8-27B-Q6_K.gguf  Q6_K
#                        (guide)                    (source: original)     (output)
```

### Expected size and accuracy

| Version | Bits per weight | Size | Typical accuracy vs. original | Suitable for |
|---|---|---|---|---|
| BF16 (original) | 16 | ~54 GB | 100% | Master copy (not published) |
| Q8_0 | 8.5 | ~29 GB | ~99.9% | 32 GB+ GPUs, maximum quality |
| Q6_K | ~6.6 | ~22 GB | ~99.5% | 24–32 GB GPUs |
| Q5_K_M | ~5.7 | ~19.5 GB | ~99% | 24 GB GPUs |
| Q4_K_M | ~4.8 | ~16.5 GB | ~97–98% | 20–24 GB GPUs; the most popular choice |
| IQ4_XS | ~4.3 | ~14.5 GB | ~97% | 16 GB GPUs |
| Q3_K_M | ~3.9 | ~13 GB | ~94% | 16 GB GPUs with longer context |
| IQ3_M | ~3.7 | ~12.5 GB | ~93% | 12–16 GB GPUs |

The accuracy column shows typical values for these formats. The **measured** results for this model
are in the [Results](#results) section.

**Rule of thumb:** choose the largest version that fits in your GPU memory while leaving 2–4 GB free for
the conversation context.

## Quantization types

| Type | Size | Use case |
|---|---|---|
| Q8_0 | 29.0 GB | Near-lossless, 32 GB+ GPUs |
| Q6_K | 22.4 GB | Excellent quality, 24–32 GB GPUs |
| Q5_K_M | 19.6 GB | Very high quality, 24 GB GPUs |
| Q4_K_M | 17.0 GB | Recommended default |
| IQ4_XS | 15.5 GB | 16 GB GPUs |
| Q3_K_M | 13.7 GB | 16 GB GPUs with longer context |
| IQ3_M | 13.0 GB | 12–16 GB GPUs |

The vision projector `mmproj-Qwen3.8-27B-F16.gguf` (0.9 GB) works with every type.

### GPU memory needed

Approximate GPU memory to run each type entirely on the GPU: the model file, the 0.9 GB vision projector and
about 2 GB for an 8K-token context. Longer context needs more; without image input, subtract about 1 GB.

| Type | File size | GPU memory needed (8K context) | Example GPUs |
|---|---|---|---|
| Q8_0 | 29.0 GB | ~32 GB | RTX 5090 (32 GB), RTX 6000 Ada (48 GB) |
| Q6_K | 22.4 GB | ~25 GB | 32 GB GPUs, or 24 GB with a shorter context |
| Q5_K_M | 19.6 GB | ~23 GB | RTX 3090 / 4090 (24 GB) |
| Q4_K_M | 17.0 GB | ~20 GB | RTX 3090 / 4090 (24 GB) |
| IQ4_XS | 15.5 GB | ~18 GB | 16 GB GPUs with a small context, or 20–24 GB |
| Q3_K_M | 13.7 GB | ~17 GB | 16 GB GPUs (tight) |
| IQ3_M | 13.0 GB | ~16 GB | 16 GB GPUs; 12 GB GPUs with some layers on the CPU (slower) |

A GPU with less memory can still run a type by keeping some layers in system RAM (lower `-ngl`), at a
noticeably lower speed.

**Compatibility:** the files need **llama.cpp build b12345 or newer**. This llama.cpp version stores some of the
model's tensors in a combined layout (`attn_qkv_gate`, `ssm_beta_alpha`) that older runtimes cannot read.
Ollama 0.40.16 (the latest release when tested) fails with `tensor 'blk.0.ssm_beta.weight' not found`; use
`llama-server` directly, or an app whose bundled llama.cpp is at least build b12345.

## Results

Results for Qwen3.8-27B. [Qwen3-8B results](#qwen3-8b-results), [Qwen3-14B results](#qwen3-14b-results) and a
[comparison of the three models](#comparing-the-three-models) follow below.

Measured with llama.cpp `b12345` on an NVIDIA RTX 6000 Ada. Accuracy is compared with the original BF16
model (perplexity **6.4334 ± 0.08**) on the held-out wikitext-2 test split (150 chunks × 512 tokens).
Full data: [`results/eval.json`](results/eval.json).

| Type | Bits/weight | Perplexity ↓ | Mean KLD ↓ | 99.9% KLD ↓ | Same top token ↑ | Speed (tok/s) |
|---|---|---|---|---|---|---|
| Q8_0 | 8.50 | 6.4399 | 0.0007 | 0.031 | 98.86% | 27.7 |
| Q6_K | 6.57 | 6.4312 | 0.0020 | 0.069 | 97.91% | 35.5 |
| Q5_K_M | 5.75 | 6.4544 | 0.0041 | 0.168 | 97.10% | 39.6 |
| Q4_K_M | 4.98 | 6.4644 | 0.0121 | 0.396 | 95.09% | 43.7 |
| IQ4_XS | 4.55 | 6.5045 | 0.0164 | 0.601 | 94.66% | 46.9 |
| Q3_K_M | 4.01 | 6.6493 | 0.0468 | 1.661 | 90.81% | 48.6 |
| IQ3_M | 3.80 | 6.7204 | 0.0563 | 1.651 | 90.33% | 50.2 |

**All seven types passed all four functional tests** (thinking on, thinking off, tool calling and vision).

How to read the table:
- **Mean KLD** (KL divergence) measures how far the quant's next-token probabilities are from the original's.
  0 means identical. It is the most reliable accuracy measure.
- **99.9% KLD** shows the worst cases: the 1-in-1000 tokens where the quant differs most.
- **Same top token** is how often the quant picks the same most likely next token as the original.
- **Perplexity** differences smaller than the measurement uncertainty (±0.08) are noise; this is why Q6_K
  can score slightly below BF16.
- **Speed** is single-request generation speed with the vision projector loaded.

Summary: Q8_0, Q6_K and Q5_K_M are practically indistinguishable from the original. Q4_K_M stays very close
at less than a third of the original size. The 3-bit types show a measurable but moderate loss and remain
fully functional.

**Scope:** the functional tests are smoke tests (one prompt per feature) that confirm each feature works;
they do not score quality. Accuracy is measured on English Wikipedia text at 512-token context, so code,
math, other languages, long context and image quality are not separately measured.

### Accuracy drop

The same measurements expressed as a loss against the original BF16 model, together with the result of the
same-question comparison ([`tools/compare_quants.py`](tools/compare_quants.py), 12 graded prompts covering logic,
math, code, knowledge, instruction following, Malayalam, Hindi, a 6K-token needle test, tool calling and vision;
reports in [`results/compare/`](results/compare/)).

| Type | Bits/weight | Next token differs from original ↓ | Perplexity increase ↓ | Graded prompts passed |
|---|---|---|---|---|
| BF16 (original) | 16 | 0% | 0% (PPL 6.4334) | reference |
| Q8_0 | 8.50 | 1.14% | +0.10% | 12/12 |
| Q6_K | 6.57 | 2.09% | −0.03% (noise) | 12/12 |
| Q5_K_M | 5.75 | 2.90% | +0.33% | 12/12 |
| Q4_K_M | 4.98 | 4.91% | +0.48% | 12/12 |
| IQ4_XS | 4.55 | 5.34% | +1.10% | 12/12 |
| Q3_K_M | 4.01 | 9.19% | +3.36% | 12/12 |
| IQ3_M | 3.80 | 9.67% | +4.46% | 12/12 |

- **Next token differs** is 100% minus the same-top-token rate: how often the quant's most likely next token is
  not the original's. Most of these are near-ties where both tokens were almost equally likely, so a different
  token is usually still a correct one.
- **Perplexity increase** is relative to the original's 6.4334. Increases up to about 1.2% are within the
  measurement uncertainty (±0.08).
- The graded prompts confirm that every type still answers correctly; they are too easy to separate the types,
  so use the first two columns to compare them.

### Speed benchmark

Measured with `llama-bench` (llama.cpp `b12345`, all layers on the RTX 6000 Ada, mean ± standard deviation).
Raw output: `results/Qwen3.8-27B-<type>.stdout.txt`.

| Type | Prompt processing, 512 tokens (tok/s) ↑ | Generation, 128 tokens (tok/s) ↑ |
|---|---|---|
| Q8_0 | 2458 ± 64 | 27.4 ± 0.9 |
| Q6_K | 1981 ± 42 | 35.4 ± 0.2 |
| Q5_K_M | 2097 ± 37 | 38.7 ± 0.7 |
| Q4_K_M | 2208 ± 66 | 43.6 ± 1.7 |
| IQ4_XS | 2410 ± 112 | 46.2 ± 1.7 |
| Q3_K_M | 2125 ± 49 | 49.7 ± 2.1 |
| IQ3_M | 2215 ± 64 | 50.5 ± 0.7 |

Generation speed rises as the files get smaller, because generating each token reads the whole model from
GPU memory. Prompt processing is limited by computation instead, so it stays around 2,000–2,500 tok/s for
every type. The generation numbers agree with the functional-test speeds above to within 1 tok/s.

### Serving every version at once

[`models.ini`](models.ini) is a `llama-server` preset that lists all seven types with the vision projector
(`ngl = 99`, 8K context), so one server can switch between them.

### Qwen3-8B results

Same method as above (wikitext-2 test, 150 chunks × 512 tokens, against BF16 logits). The BF16 model
fits in GPU memory, so the importance matrix was computed on BF16 directly. Original perplexity **9.5927 ± 0.15**.
Full data: [`results/Qwen3-8B/eval.json`](results/Qwen3-8B/eval.json).
Download: [muhammed-afsal-p-m/Qwen3-8B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3-8B-GGUF).

| Type | Size | Bits/weight | Perplexity ↓ | Mean KLD ↓ | Same top token ↑ | Speed (tok/s) |
|---|---|---|---|---|---|---|
| Q8_0 | 8.7 GB | 8.50 | 9.6168 | 0.0015 | 98.14% | 89.2 |
| Q6_K | 6.7 GB | 6.57 | 9.6072 | 0.0049 | 96.84% | 107.5 |
| Q5_K_M | 5.8 GB | 5.71 | 9.6407 | 0.0092 | 95.75% | 123.8 |
| Q4_K_M | 5.0 GB | 4.91 | 9.6697 | 0.0262 | 93.18% | 140.3 |
| IQ4_XS | 4.6 GB | 4.45 | 9.8062 | 0.0353 | 92.45% | 152.1 |
| Q3_K_M | 4.1 GB | 4.03 | 10.0569 | 0.0920 | 87.75% | 155.3 |
| IQ3_M | 3.9 GB | 3.80 | 9.9729 | 0.1175 | 86.44% | 148.4 |

**All seven types passed the functional tests** (thinking on, thinking off and tool calling).

The 8B model loses about twice as much as the 27B model at every level (mean KLD 0.0262 vs 0.0121 at
Q4_K_M): a smaller model has less spare capacity, so rounding the weights costs more. For quality-sensitive
use, Q5_K_M or higher is the better choice for 8B.

### Qwen3-14B results

Same method as above (wikitext-2 test, 150 chunks × 512 tokens, against BF16 logits); the importance matrix
was computed on BF16 directly. Original perplexity **8.5685 ± 0.13**.
Full data: [`results/Qwen3-14B/eval.json`](results/Qwen3-14B/eval.json).
Download: [muhammed-afsal-p-m/Qwen3-14B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3-14B-GGUF).

| Type | Size | Bits/weight | Perplexity ↓ | Mean KLD ↓ | Same top token ↑ | Speed (tok/s) |
|---|---|---|---|---|---|---|
| Q8_0 | 15.7 GB | 8.50 | 8.5871 | 0.0010 | 98.63% | 51.4 |
| Q6_K | 12.1 GB | 6.56 | 8.6077 | 0.0034 | 97.66% | 64.3 |
| Q5_K_M | 10.5 GB | 5.69 | 8.6217 | 0.0059 | 96.75% | 71.7 |
| Q4_K_M | 9.0 GB | 4.88 | 8.6734 | 0.0188 | 94.25% | 80.9 |
| IQ4_XS | 8.1 GB | 4.39 | 8.6165 | 0.0257 | 93.59% | 88.6 |
| Q3_K_M | 7.3 GB | 3.97 | 8.8382 | 0.0614 | 90.14% | 92.7 |
| IQ3_M | 6.9 GB | 3.73 | 8.8144 | 0.0716 | 89.31% | 91.9 |

**All seven types passed the functional tests** (thinking on, thinking off and tool calling), and every type
answered all 17 graded extended questions correctly
([`results/Qwen3-14B/compare/`](results/Qwen3-14B/compare/)). Accuracy on Malayalam, Hindi and Python code is in
[`results/Qwen3-14B/kld_by_language.md`](results/Qwen3-14B/kld_by_language.md).

### Comparing the three models

At the recommended Q4_K_M level (same calibration data, same evaluation text, llama.cpp `b12345`,
RTX 6000 Ada):

| Model | Q4_K_M size | Mean KLD ↓ | Same top token ↑ | Malayalam KLD ↓ | Hindi KLD ↓ | Speed (tok/s) |
|---|---|---|---|---|---|---|
| Qwen3.8-27B | 17.0 GB | 0.0121 | 95.09% | 0.0153 | 0.0115 | 43.7 |
| Qwen3-14B | 9.0 GB | 0.0188 | 94.25% | 0.0142 | 0.0150 | 80.9 |
| Qwen3-8B | 5.0 GB | 0.0262 | 93.18% | 0.0222 | 0.0220 | 140.3 |

Larger models lose less to quantization: the 27B model drifts least from its original, the 8B model most.
The 14B model at Q4_K_M fits a 12 GB GPU and stays close to its original, a good middle ground between quality and
hardware.

## Pipeline

```
Hugging Face (BF16 safetensors)
        │  01 verify (SHA256)
        ▼
02 convert ──► BF16 GGUF + mmproj (vision)
        │
03 calibration data ──► 04 Q8_0 reference + importance matrix
        │
05 quantize ──► Q6_K, Q5_K_M, Q4_K_M, IQ4_XS, Q3_K_M, IQ3_M + SHA256SUMS
        │
06 evaluate ──► perplexity, KL divergence, thinking / tool / vision tests
        │
07 model card ──► release/ folder
        │
08 upload ──► Hugging Face (manual, requires --yes)
```

| Step | Script | Output |
|---|---|---|
| 01 | `pipeline/01_verify_download.py` | `results/source_manifest.json` |
| 02 | `pipeline/02_convert.py` | `out/Qwen3.8-27B-BF16.gguf`, `out/mmproj-Qwen3.8-27B-F16.gguf` |
| 03 | `pipeline/03_calibration.py` | `data/calibration.txt`, `data/wiki.test.raw`, `results/calibration_stats.json` |
| 04 | `pipeline/04_imatrix.py` | `out/Qwen3.8-27B-Q8_0.gguf`, `out/Qwen3.8-27B.imatrix.gguf` |
| 05 | `pipeline/05_quantize.py` | All quantized files and `out/SHA256SUMS.txt` |
| 06 | `pipeline/06_evaluate.py` | `results/eval.json` |
| 07 | `pipeline/07_model_card.py` | `release/` and `release/README.md` |
| 08 | `pipeline/08_upload.py` | Hugging Face repository |

## Requirements

| Component | Tested with |
|---|---|
| OS | Windows 11 |
| GPU | NVIDIA RTX 6000 Ada (48 GB VRAM) |
| RAM | 64 GB |
| Disk | ~200 GB free |
| Python | 3.11 (conda) |
| llama.cpp | build `b12345`, CUDA 13.5 |

The conversion runs on CPU. A GPU with at least 32 GB of VRAM is recommended for the importance matrix
and evaluation steps; smaller GPUs work with partial offloading (`ngl` in `config.yaml`).

## Setup

**1. Python environment**

```bash
conda create -n quant python=3.11 -y
conda activate quant
```

**2. llama.cpp**

```bash
git clone --depth 1 https://github.com/ggml-org/llama.cpp tools/llama.cpp
pip install -r tools/llama.cpp/requirements/requirements-convert_hf_to_gguf.txt
pip install -r requirements.txt
```

Download the Windows CUDA build from the [llama.cpp releases](https://github.com/ggml-org/llama.cpp/releases)
(`llama-<build>-bin-win-cuda-13.5-x64.zip` and `cudart-llama-bin-win-cuda-13.5-x64.zip`)
and extract both archives into `tools/llama-bin/`.

**3. Hugging Face login and model download**

```bash
hf auth login
hf download Qwen/Qwen3.8-27B --local-dir models/Qwen3.8-27B
```

Use a token with **write** access if you plan to upload. The token is stored locally by the
Hugging Face CLI and is never written to this repository.

## Usage

Run steps 01–07:

```bash
python run_all.py
```

Resume from a specific step, or run a single step:

```bash
python run_all.py --from 4
python run_all.py --only 6
```

Review `release/README.md`, then upload:

```bash
python pipeline/08_upload.py         # dry run: lists files and destination
python pipeline/08_upload.py --yes   # upload (resumable)
```

**Other models:** add `--config` to any command. Each model writes to its own folders
(`out/<model>/`, `results/<model>/`, `release/<model>/`, `logs/<model>/`, `data/<model>/`):

```bash
hf download Qwen/Qwen3-8B --local-dir models/Qwen3-8B
python run_all.py --config configs/qwen3-8b.yaml
python tools/compare_quants.py --config configs/qwen3-8b.yaml
python pipeline/08_upload.py --config configs/qwen3-8b.yaml
```

Monitor a running model download:

```bash
python tools/progress.py
```

Ask every quant the same questions and compare answers and latency:

```bash
python tools/compare_quants.py                       # all quants, all prompts (~15–30 min)
python tools/compare_quants.py --only Q4_K_M IQ3_M   # selected quants
python tools/compare_quants.py --prompts-only bat-ball needle --repeats 1
```

Each quant is loaded on its own in `llama-server` (with the vision projector), warmed up, and asked every
prompt in [`tools/prompts.yaml`](tools/prompts.yaml) at temperature 0 with a fixed seed. Answers with a known
result are graded automatically (logic, math, code tests, knowledge, instruction following, Malayalam and
Hindi, a 6K-token needle-in-text test, tool calling, a chart image); open answers are compared with the Q8_0
answer. Add your own questions to `prompts.yaml`. The report is written to
`results/compare/<date-time>/report.md`, with `results.csv` and `results.json` beside it.

## Configuration

All settings are in [`config.yaml`](config.yaml) (Qwen3.8-27B) and in one file per model in
[`configs/`](configs/). To add a model, copy a file from `configs/` and change the `model`, `paths` and `hf` sections.

| Section | Controls |
|---|---|
| `model` | Source repository, revision, local folder, output name; `vision` (has an mmproj) and `reasoning_effort` (thinking levels, or `false` for on/off only) |
| `paths` | Output folders (one set per model) |
| `quantize` | Quant types to build, reference type, types built without an imatrix |
| `calibration` | Token budget, random seed, data sources and their share |
| `imatrix` | Context size, GPU layers, number of chunks; `source: bf16` computes it on BF16 when it fits in GPU memory |
| `eval` | Evaluation text, chunks, GPU layers, server settings |
| `card` | Optional model card text: tags, notes, GPU guide, tested Ollama version, language results |
| `hf` | Destination repository and collection |

## Methodology

**Calibration.** About 160K tokens drawn from six public datasets:

| Source | Dataset | Purpose |
|---|---|---|
| General | `Salesforce/wikitext` (train) | Natural English text |
| Chat | `HuggingFaceH4/ultrachat_200k` | Multi-turn conversations |
| Math | `openai/gsm8k` | Step-by-step arithmetic reasoning |
| Code | `iamtarun/python_code_instructions_18k_alpaca` | Python instruction following |
| Reasoning | `nvidia/OpenCodeReasoning` | Long `<think>` reasoning traces |
| Multilingual | `CohereLabs/aya_dataset` | Many languages |

Samples are rendered with the model's chat template. Reasoning traces use thinking mode with a mix of
reasoning-effort levels; other samples use thinking-off mode. Sources are shuffled together so every
imatrix chunk sees a mix.

**Importance matrix.** Computed on the Q8_0 quant, which fits entirely in GPU memory and is practically
identical to BF16. Chat-template tokens are parsed as special tokens.

**Evaluation.** Perplexity and KL divergence on the held-out wikitext-2 **test** split
(calibration uses only the train split), compared with logits from the BF16 model. Reported metrics:
perplexity, mean / 99.9th percentile / maximum KL divergence, RMS Δp and same-top-token rate.

**Functional tests.** Each quant is served with `llama-server` and the vision projector, at temperature 0:

| Test | Pass condition |
|---|---|
| Thinking on | Produces a reasoning trace and the correct answer to a trick question |
| Thinking off | Answers directly with no reasoning trace |
| Tool calling | Calls the provided function with the correct argument |
| Vision | Identifies the colour of a shape in a generated test image |

## Project structure

```
.
├── config.yaml              Pipeline settings for Qwen3.8-27B
├── configs/
│   ├── qwen3-8b.yaml        Pipeline settings for Qwen3-8B
│   └── qwen3-14b.yaml       Pipeline settings for Qwen3-14B
├── run_all.py               Runs steps 01–07 (--config selects the model)
├── requirements.txt
├── pipeline/
│   ├── common.py            Shared paths and helpers
│   ├── 01_verify_download.py
│   ├── 02_convert.py
│   ├── 03_calibration.py
│   ├── 04_imatrix.py
│   ├── 05_quantize.py
│   ├── 06_evaluate.py
│   ├── 07_model_card.py
│   └── 08_upload.py
├── tools/
│   ├── progress.py              Download progress bar
│   ├── compare_quants.py        Same questions to every quant: answers, accuracy, latency
│   ├── prompts.yaml             13 basic questions (editable)
│   ├── prompts_extended.yaml    22 harder questions, including invoice and chart images
│   ├── prompts_multilingual.yaml The same problems in English, Malayalam and Hindi
│   ├── test_images/             Generated test images with known answers
│   ├── kld_by_language.py       Accuracy drop per language (Malayalam, Hindi, code)
│   └── concurrency_bench.py     Throughput and latency with 1 to 16 simultaneous users
└── results/                 Qwen3.8-27B results; results/<model>/ for the other models
```

Model weights, GGUF files, datasets, logs and third-party tools are excluded by `.gitignore`.

### Folders created when you run the pipeline

```
.
├── models/Qwen3.8-27B/    Original model from Hugging Face (safetensors, ~54 GB). Read only, never modified
├── out/                   All GGUF files: BF16, every quantized version, mmproj and the importance matrix
├── data/                  Calibration text and evaluation text
├── results/               Calibration statistics, source manifest, evaluation results and checksums
├── logs/                  One log file per step
├── release/               Exactly the files that are uploaded to Hugging Face (created by step 07)
└── tools/                 llama.cpp source and binaries
```

**The original model folder** (`models/Qwen3.8-27B/`):

| File | Contents |
|---|---|
| `model-00001-of-00018.safetensors` … `model-00018-of-00018.safetensors` | The weights, split into 18 parts |
| `model.safetensors.index.json` | Which weight is stored in which part |
| `config.json` | Model design: layers, sizes, architecture |
| `tokenizer.json`, `vocab.json`, `merges.txt`, `tokenizer_config.json` | How text is split into tokens |
| `chat_template.jinja` | Chat format, including thinking mode |
| `preprocessor_config.json`, `video_preprocessor_config.json` | Image and video input settings |
| `generation_config.json` | Default sampling settings (temperature, top-p) |
| `LICENSE`, `README.md` | Apache 2.0 license and the original model card |

**What is published to Hugging Face:** only the contents of `release/`: the seven quantized GGUF files,
the mmproj file, the importance matrix, `SHA256SUMS.txt` and the model card. The original weights and
the BF16 GGUF stay local.

## FAQ

**Why is the importance matrix computed on Q8_0 and not on BF16?**
For Qwen3.8-27B, the BF16 file (~54 GB) does not fit in a 48 GB GPU. Q8_0 (~29 GB) fits entirely and is
practically identical to BF16, so the importance matrix is just as accurate and much faster to compute.
For Qwen3-8B and Qwen3-14B the BF16 file fits, so their importance matrix is computed on BF16 directly
(`imatrix.source: bf16`).

**What are the "model has unused tensor blk.64 ..." warnings during the imatrix step?**
Layer 64 is an extra next-token-prediction layer (`nextn`) used only for speculative decoding.
Normal inference does not use it, so the importance matrix skips it. The layer is still kept in every
quantized file. The warnings are harmless.

**Why does a file end in `.partial.gguf`?**
The file is still being written. When a step finishes, the file is renamed to its final name, so an
interrupted run never leaves a broken file with a valid-looking name. Re-running the pipeline rebuilds it.

**Why do file sizes differ between the terminal and the file explorer?**
llama.cpp reports sizes in GB (1 GB = 1,000,000,000 bytes), while Windows Explorer and VS Code use GiB
(1 GiB = 1,073,741,824 bytes). For example, the Q8_0 file is 29.05 GB, which is 27.05 GiB.

**Can I stop the pipeline and continue later?**
Yes. Every step skips work that is already complete. Run `python run_all.py --from <step>` to continue.

## License

The code in this repository is released under the [MIT License](LICENSE).
The Qwen3.8-27B model weights and the quantized files are licensed under
[Apache 2.0](https://huggingface.co/Qwen/Qwen3.8-27B) by the Qwen team.

## Acknowledgements

- [Qwen team](https://huggingface.co/Qwen) for Qwen3.8-27B
- [llama.cpp](https://github.com/ggml-org/llama.cpp) for GGUF conversion, quantization and evaluation tools
- The authors of the calibration datasets listed above
