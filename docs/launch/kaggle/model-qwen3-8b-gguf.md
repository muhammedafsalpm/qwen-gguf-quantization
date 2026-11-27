# Kaggle model page: Qwen3-8B GGUF

**Title:** Qwen3-8B GGUF (imatrix, measured against BF16)

**Subtitle (one line):** Seven llama.cpp quants of Qwen3-8B, each compared with the original weights and tested.

**Licence:** Apache 2.0 · **Framework:** GGUF · **Variations uploaded:** q8_0, q4_k_m, iq4_xs

---

## Description (paste into the model page)

GGUF versions of [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B), made with llama.cpp and an
importance matrix. Every file was compared with the original BF16 model, so you can pick a size by measured
quality instead of rules of thumb.

**Recommended:** Q4_K_M (5.0 GB) for an 8 GB GPU. If quality matters more than memory, go to Q5_K_M or
higher: the 8B model loses about twice as much as the 27B at the same level.

| Variation | Size | Mean KLD vs BF16 ↓ | Same top token ↑ | Notes |
|---|---|---|---|---|
| q8_0 | 8.7 GB | 0.0015 | 98.14% | Practically identical; fits a single Kaggle T4 |
| q4_k_m | 5.0 GB | 0.0262 | 93.18% | The usual default |
| iq4_xs | 4.6 GB | 0.0353 | 92.45% | Smallest 4-bit, for 6 GB GPUs |

All seven quants (Q8_0 to IQ3_M) and the importance matrix are on Hugging Face:
https://huggingface.co/muhammed-afsal-p-m/Qwen3-8B-GGUF

### How it was measured
- Importance matrix computed on the BF16 model from 164K tokens of chat, code, math, reasoning traces and
  multilingual text, rendered with Qwen3's chat template.
- KL divergence and perplexity against BF16 logits on the held-out wikitext-2 test split
  (150 chunks × 512 tokens). Original perplexity 9.5927.
- Thinking on, thinking off and tool calling tested on every file, plus 43 graded questions. I read the
  answers myself: a few "fails" were the model running out of thinking tokens, and the 8B model sometimes
  uses non-standard Malayalam spellings even at Q8_0.
- Malayalam KLD at Q4_K_M: 0.0222, Hindi 0.0220, Python code 0.0137.

### Run it
```bash
llama-server -m Qwen3-8B-Q4_K_M.gguf -ngl 99 -c 16384 --jinja
```
or with Ollama: `ollama run hf.co/muhammed-afsal-p-m/Qwen3-8B-GGUF:Q4_K_M`

**Try it on a free Kaggle T4:** [notebook link — add after publishing]

### Links
- All three models: [Qwen3 Quants collection](https://huggingface.co/collections/muhammed-afsal-p-m/qwen3-quants)
- Other sizes on Kaggle: Qwen3-14B GGUF · Qwen3.8-27B GGUF [add links after publishing]
- Pipeline code and full results: https://github.com/muhammedafsalpm/qwen-gguf-quantization

Credit for the model goes to the Qwen team. Checksums are in `SHA256SUMS.txt`; source weights:
`Qwen/Qwen3-8B` at commit `b968826d`.
