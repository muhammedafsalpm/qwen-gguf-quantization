# Accuracy drop by language: Qwen3-14B

KL divergence against BF16 per language, 512-token chunks (English: 150 chunks of wikitext-2 test, from step 06; other languages: 80 chunks). Lower is better in both tables.

## Next token differs from BF16 (100% − same top token)

| Type | English | Malayalam | Hindi | Python code |
|---|---|---|---|---|
| Q8_0 | 1.37% | 0.75% | 0.68% | 0.53% |
| Q6_K | 2.34% | 1.28% | 1.50% | 0.93% |
| Q5_K_M | 3.25% | 1.78% | 1.97% | 1.25% |
| Q4_K_M | 5.75% | 3.35% | 3.56% | 2.30% |
| IQ4_XS | 6.41% | 3.88% | 4.06% | 2.51% |
| Q3_K_M | 9.86% | 6.34% | 6.61% | 3.85% |
| IQ3_M | 10.69% | 6.96% | 7.23% | 4.29% |

## Mean KL divergence

| Type | English | Malayalam | Hindi | Python code |
|---|---|---|---|---|
| Q8_0 | 0.0010 | 0.0006 | 0.0006 | 0.0006 |
| Q6_K | 0.0034 | 0.0025 | 0.0024 | 0.0017 |
| Q5_K_M | 0.0059 | 0.0044 | 0.0043 | 0.0034 |
| Q4_K_M | 0.0188 | 0.0142 | 0.0150 | 0.0090 |
| IQ4_XS | 0.0257 | 0.0195 | 0.0205 | 0.0124 |
| Q3_K_M | 0.0614 | 0.0498 | 0.0504 | 0.0316 |
| IQ3_M | 0.0716 | 0.0603 | 0.0603 | 0.0383 |

Texts: English = wikitext-2 test; Malayalam and Hindi = Wikipedia articles (wikimedia/wikipedia, 20231101); Python code = llama.cpp's own scripts. None of these texts is in the calibration data.
