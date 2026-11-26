# Accuracy drop by language: Qwen3-8B

KL divergence against BF16 per language, 512-token chunks (English: 150 chunks of wikitext-2 test, from step 06; other languages: 80 chunks). Lower is better in both tables.

## Next token differs from BF16 (100% − same top token)

| Type | English | Malayalam | Hindi | Python code |
|---|---|---|---|---|
| Q8_0 | 1.86% | 1.03% | 0.91% | 0.64% |
| Q6_K | 3.16% | 1.84% | 1.80% | 1.24% |
| Q5_K_M | 4.25% | 2.64% | 2.57% | 1.59% |
| Q4_K_M | 6.82% | 4.50% | 4.32% | 2.58% |
| IQ4_XS | 7.55% | 5.30% | 5.04% | 3.09% |
| Q3_K_M | 12.25% | 8.73% | 8.32% | 4.75% |
| IQ3_M | 13.56% | 9.60% | 9.72% | 5.28% |

## Mean KL divergence

| Type | English | Malayalam | Hindi | Python code |
|---|---|---|---|---|
| Q8_0 | 0.0015 | 0.0011 | 0.0010 | 0.0011 |
| Q6_K | 0.0049 | 0.0033 | 0.0036 | 0.0029 |
| Q5_K_M | 0.0092 | 0.0072 | 0.0070 | 0.0053 |
| Q4_K_M | 0.0262 | 0.0222 | 0.0220 | 0.0137 |
| IQ4_XS | 0.0353 | 0.0301 | 0.0294 | 0.0185 |
| Q3_K_M | 0.0920 | 0.0840 | 0.0790 | 0.0525 |
| IQ3_M | 0.1175 | 0.0978 | 0.1012 | 0.0617 |

Texts: English = wikitext-2 test; Malayalam and Hindi = Wikipedia articles (wikimedia/wikipedia, 20231101); Python code = llama.cpp's own scripts. None of these texts is in the calibration data.
