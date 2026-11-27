# Kaggle model page: Qwen3.8-27B GGUF

**Title:** Qwen3.8-27B GGUF with vision (imatrix, measured against BF16)

**Subtitle (one line):** Seven llama.cpp quants of Qwen3.8-27B plus the vision projector, each compared with the original.

**Licence:** Apache 2.0 · **Framework:** GGUF · **Variations uploaded:** q4_k_m, iq3_m (each with the mmproj file)

---

## Description (paste into the model page)

GGUF versions of [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) with thinking mode, tool
calling and image input. Each variation includes `mmproj-Qwen3.8-27B-F16.gguf` (0.9 GB), which you load
next to the model for images.

This is the one I measured first and the most accurate of the three: at Q4_K_M it picks the same next token
as the original 95.09% of the time, and every quant answered every graded question I gave it, including
reading a chart and an invoice.

| Variation | Size | Mean KLD vs BF16 ↓ | Same top token ↑ | Notes |
|---|---|---|---|---|
| q4_k_m | 17.0 GB | 0.0121 | 95.09% | Recommended; 24 GB GPU, or Kaggle T4 x2 |
| iq3_m | 13.0 GB | 0.0563 | 90.33% | For 16 GB GPUs |

All seven quants (Q8_0 to IQ3_M), the vision projector and the importance matrix are on Hugging Face:
https://huggingface.co/muhammed-afsal-p-m/Qwen3.8-27B-GGUF

**Needs llama.cpp build b12345 or newer.** Recent llama.cpp stores some of this model's tensors in a
combined layout that older runtimes can't read, so Ollama 0.40.16 and older can't load these files.

### How it was measured
- Importance matrix computed on the Q8_0 quant (mean KLD 0.0007 against BF16) from 164K tokens of chat,
  code, math, reasoning traces and multilingual text.
- KL divergence and perplexity against BF16 logits on the held-out wikitext-2 test split
  (150 chunks × 512 tokens). Original perplexity 6.4334.
- Thinking on, thinking off, tool calling and vision tested on every file, plus 46 graded questions
  (including image questions, Malayalam and Hindi), answers read by hand.
- Malayalam KLD at Q4_K_M: 0.0153, Hindi 0.0115, Python code 0.0124.

### Run it
```bash
llama-server -m Qwen3.8-27B-Q4_K_M.gguf --mmproj mmproj-Qwen3.8-27B-F16.gguf -ngl 99 -c 16384 --jinja
```

**Try it on Kaggle (GPU T4 x2):** [notebook link — add after publishing]

### Links
- All three models: [Qwen3 Quants collection](https://huggingface.co/collections/muhammed-afsal-p-m/qwen3-quants)
- Other sizes on Kaggle: Qwen3-14B GGUF · Qwen3-8B GGUF [add links after publishing]
- Pipeline code and full results: https://github.com/muhammedafsalpm/qwen-gguf-quantization

Credit for the model goes to the Qwen team. Checksums are in `SHA256SUMS.txt`.
