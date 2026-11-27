# Kaggle dataset and notebook text

## Dataset

**Title:** Qwen3 GGUF Quantization Benchmarks (27B, 14B, 8B)

**Subtitle:** KL divergence, perplexity, speed and test scores for 21 GGUF files, measured against BF16

**Files to upload** (from `docs/launch/data/`): `quant_results.csv`, `kld_by_language.csv`, `question_tests.csv`

**Licence:** CC BY 4.0 · **Tags:** nlp, large language models, benchmark, quantization, text generation

### Description

These are the measurements behind my GGUF quants of Qwen3.8-27B, Qwen3-14B and Qwen3-8B. Each of the
21 files (7 quant types × 3 models) was compared with its own BF16 model using llama.cpp b12345.

**quant_results.csv**: one row per file
- `size_gb`, `bits_per_weight`
- `perplexity`, `bf16_perplexity`: wikitext-2 test, 150 chunks × 512 tokens
- `mean_kld`, `kld_p99_9`: KL divergence of next-token probabilities against BF16 (lower is better)
- `same_top_token_pct`: how often the quant picks the same next token as BF16
- `gen_tokens_per_sec`: generation speed on one RTX 6000 Ada, all layers on GPU
- `thinking_on`, `thinking_off`, `tool_call`, `vision`: functional test results (vision only for 27B)

**kld_by_language.csv**: mean KLD on English (wikitext-2), Malayalam and Hindi (Wikipedia articles) and
Python code (llama.cpp scripts), 80 × 512 tokens each. None of these texts were in the calibration data.

**question_tests.csv**: correct answers out of the graded questions per file (basic, extended,
multilingual), at temperature 0, one run each. Automatic checks were confirmed by reading the answers.

Models: https://huggingface.co/collections/muhammed-afsal-p-m/qwen3-quants ·
Code: https://github.com/muhammedafsalpm/qwen-gguf-quantization

---

## Notebook

**Title:** Qwen3 27B / 14B / 8B GGUF on a Kaggle T4: measured quality and speed

**File:** `docs/launch/kaggle/qwen3-gguf-kaggle-t4.ipynb`

**Settings:** Accelerator GPU T4 x2 · Internet on · Licence Apache 2.0

**Tags:** nlp, large language models, gpu, beginner, text generation

**Inputs to add (Add Input → Models):** the three Kaggle model pages once they exist (so they show as
"used in" on each model page). The notebook itself downloads from Hugging Face, so it works either way.

Run it once fully (Save Version → Save & Run All) before making it public, so readers see the outputs.
