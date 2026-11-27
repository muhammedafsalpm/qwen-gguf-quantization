# Kaggle model page: Qwen3-14B GGUF

**Title:** Qwen3-14B GGUF (imatrix, measured against BF16)

**Subtitle (one line):** Seven llama.cpp quants of Qwen3-14B, each compared with the original weights and tested.

**Licence:** Apache 2.0 · **Framework:** GGUF · **Variations uploaded:** q8_0, q4_k_m, iq3_m

---

## Description (paste into the model page)

GGUF versions of [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B) that I made with llama.cpp and an
importance matrix. I didn't want to pick a quant by guesswork, so every file was compared with the original
BF16 model and run through the same set of questions.

**Recommended:** Q4_K_M (9.0 GB) for a 12 GB GPU. It picks the same next token as the original 94.25% of the
time, and it answered all 17 of my graded extended questions correctly.

| Variation | Size | Mean KLD vs BF16 ↓ | Same top token ↑ | Notes |
|---|---|---|---|---|
| q8_0 | 15.7 GB | 0.0010 | 98.63% | Practically identical to the original |
| q4_k_m | 9.0 GB | 0.0188 | 94.25% | Best balance; fits a 12 GB GPU |
| iq3_m | 6.9 GB | 0.0716 | 89.31% | Smallest; for 8 GB GPUs with a short context |

All seven quants (Q8_0 to IQ3_M) and the importance matrix are on Hugging Face:
https://huggingface.co/muhammed-afsal-p-m/Qwen3-14B-GGUF

### How it was measured
- Importance matrix computed on the BF16 model from 164K tokens of chat, code, math, reasoning traces and
  multilingual text, rendered with Qwen3's chat template.
- KL divergence and perplexity against BF16 logits on the held-out wikitext-2 test split
  (150 chunks × 512 tokens). Original perplexity 8.5685.
- Thinking on, thinking off and tool calling tested on every file, plus 43 graded questions
  (reasoning, math, code, SQL, Malayalam and Hindi). I read the answers rather than trusting the automatic checks.
- Malayalam KLD at Q4_K_M: 0.0142, Hindi 0.0150, Python code 0.0090.

### Run it
```bash
llama-server -m Qwen3-14B-Q4_K_M.gguf -ngl 99 -c 16384 --jinja
```
or with Ollama: `ollama run hf.co/muhammed-afsal-p-m/Qwen3-14B-GGUF:Q4_K_M`

Turn thinking off per request with `"chat_template_kwargs": {"enable_thinking": false}`, or add `/no_think`
to a message.

**Try it on a free Kaggle T4:** [notebook link — add after publishing]

### Links
- All three models: [Qwen3 Quants collection](https://huggingface.co/collections/muhammed-afsal-p-m/qwen3-quants)
- Other sizes on Kaggle: Qwen3-8B GGUF · Qwen3.8-27B GGUF [add links after publishing]
- Pipeline code and full results: https://github.com/muhammedafsalpm/qwen-gguf-quantization

Credit for the model goes to the Qwen team. Checksums are in `SHA256SUMS.txt`; source weights:
`Qwen/Qwen3-14B` at commit `40c06982`.
