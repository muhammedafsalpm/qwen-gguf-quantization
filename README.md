# Qwen3.8-27B GGUF Quantization

A reproducible pipeline that converts [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) into
importance-matrix (imatrix) GGUF quantizations, measures every quant against the original BF16 model,
tests thinking, tool calling and vision, and publishes the results to Hugging Face.

**Quantized model:** [muhammed-afsal-p-m/Qwen3.8-27B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3.8-27B-GGUF)

---

## Contents

- [Features](#features)
- [Quantization types](#quantization-types)
- [Pipeline](#pipeline)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Methodology](#methodology)
- [Project structure](#project-structure)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Verified source:** every original weight file is checked by SHA256 against the Hugging Face repository,
  and the exact commit is recorded.
- **Calibrated quantization:** the importance matrix is built from a mixed calibration set (general text,
  multi-turn chat, math, code, `<think>` reasoning traces and multilingual data), rendered with the model's
  own chat template so both thinking and non-thinking modes are represented.
- **Measured accuracy:** perplexity and KL divergence of every quant against BF16 logits, on held-out text.
- **Functional tests:** thinking on, thinking off, tool calling and image input, run through `llama-server`.
- **Vision support:** the multimodal projector (`mmproj`) is exported alongside the text model.
- **Resumable:** every step skips work that is already complete, so an interrupted run continues where it stopped.
- **Single configuration file:** all settings live in [`config.yaml`](config.yaml).

## Quantization types

| Type | Approx. size | Use case |
|---|---|---|
| Q8_0 | ~29 GB | Near-lossless reference |
| Q6_K | ~22 GB | Excellent quality, 24–32 GB GPUs |
| Q5_K_M | ~19.5 GB | Very high quality, 24 GB GPUs |
| Q4_K_M | ~16.5 GB | Recommended default |
| IQ4_XS | ~14.5 GB | 16 GB GPUs |
| Q3_K_M | ~13 GB | 16 GB GPUs with longer context |
| IQ3_M | ~12.5 GB | 12–16 GB GPUs |

Measured perplexity, KL divergence and test results for each file are published in the
[model card](https://huggingface.co/muhammed-afsal-p-m/Qwen3.8-27B-GGUF).

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

Monitor a running model download:

```bash
python tools/progress.py
```

## Configuration

All settings are in [`config.yaml`](config.yaml):

| Section | Controls |
|---|---|
| `model` | Source repository, revision, local folder, output name |
| `quantize` | Quant types to build, reference type, types built without an imatrix |
| `calibration` | Token budget, random seed, data sources and their share |
| `imatrix` | Context size, GPU layers, number of chunks |
| `eval` | Evaluation text, chunks, GPU layers, server settings |
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
├── config.yaml              Pipeline settings
├── run_all.py               Runs steps 01–07
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
│   └── progress.py          Download progress bar
└── results/                 Calibration statistics, source manifest, evaluation results
```

Model weights, GGUF files, datasets, logs and third-party tools are excluded by `.gitignore`.

## License

The code in this repository is released under the [MIT License](LICENSE).
The Qwen3.8-27B model weights and the quantized files are licensed under
[Apache 2.0](https://huggingface.co/Qwen/Qwen3.8-27B) by the Qwen team.

## Acknowledgements

- [Qwen team](https://huggingface.co/Qwen) for Qwen3.8-27B
- [llama.cpp](https://github.com/ggml-org/llama.cpp) for GGUF conversion, quantization and evaluation tools
- The authors of the calibration datasets listed above
