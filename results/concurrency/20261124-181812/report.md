# Concurrent load: Qwen3.8-27B

llama-server (llama.cpp b12345), 16 slots × 4096 tokens, continuous batching. Each request: ~500-token prompt, exactly 256 generated tokens, thinking off, 1 waves per level. Text only (no vision projector).

## Total throughput (generated tokens/s, all users combined)

| Type | 1 user | 4 users | 16 users |
|---|---|---|---|
| Q8_0 | 25.9 | 77.6 | 170.5 |
| Q4_K_M | 33.5 | 103.6 | 196.9 |
| IQ3_M | 46.2 | 116.5 | 194.6 |

## Generation speed per user (tokens/s)

| Type | 1 | 4 | 16 |
|---|---|---|---|
| Q8_0 | 28.4 | 23.7 | 14.2 |
| Q4_K_M | 41.2 | 32.1 | 17.2 |
| IQ3_M | 50.6 | 36.1 | 17.8 |

## Time to first token, p95 (s)

| Type | 1 | 4 | 16 |
|---|---|---|---|
| Q8_0 | 0.47 | 1.48 | 7.22 |
| Q4_K_M | 0.44 | 1.63 | 6.84 |
| IQ3_M | 0.48 | 1.37 | 8.1 |

## GPU memory (GB): after loading / peak at the highest level

| Type | Loaded | Peak | Errors |
|---|---|---|---|
| Q8_0 | 33.6 | 33.7 | 0 |
| Q4_K_M | 23.2 | 23.3 | 0 |
| IQ3_M | 19.7 | 19.8 | 0 |
