# Accuracy drop by language: Qwen3.8-27B

KL divergence against BF16 per language, 512-token chunks (English: 150 chunks of wikitext-2 test, from step 06; other languages: 80 chunks). Lower is better in both tables.

## Next token differs from BF16 (100% − same top token)

| Type | English | Malayalam | Hindi | Python code |
|---|---|---|---|---|
| Q8_0 | 1.14% | 1.29% | 1.12% | 0.61% |
| Q6_K | 2.09% | 2.21% | 1.94% | 0.96% |
| Q5_K_M | 2.90% | 2.87% | 2.43% | 1.36% |
| Q4_K_M | 4.91% | 5.21% | 4.53% | 2.18% |
| IQ4_XS | 5.34% | 6.30% | 5.46% | 2.68% |
| Q3_K_M | 9.19% | 10.34% | 9.47% | 4.37% |
| IQ3_M | 9.67% | 10.32% | 9.55% | 4.48% |

## Mean KL divergence

| Type | English | Malayalam | Hindi | Python code |
|---|---|---|---|---|
| Q8_0 | 0.0007 | 0.0008 | 0.0007 | 0.0009 |
| Q6_K | 0.0020 | 0.0024 | 0.0018 | 0.0021 |
| Q5_K_M | 0.0041 | 0.0047 | 0.0039 | 0.0041 |
| Q4_K_M | 0.0121 | 0.0153 | 0.0115 | 0.0124 |
| IQ4_XS | 0.0164 | 0.0205 | 0.0168 | 0.0169 |
| Q3_K_M | 0.0468 | 0.0587 | 0.0471 | 0.0439 |
| IQ3_M | 0.0563 | 0.0633 | 0.0524 | 0.0528 |

Texts: English = wikitext-2 test; Malayalam and Hindi = Wikipedia articles (wikimedia/wikipedia, 20231101); Python code = llama.cpp's own scripts. None of these texts is in the calibration data.
