# Quant comparison: Qwen3.8-27B

13 prompts × 2 quants, temperature 0, seed 42, context 16384, 1 timing run(s) per prompt, llama.cpp b12345. Similarity is measured against the Q8_0 answer (1.0 = identical text).

## Summary

| Quant | Correct | Avg total time (s) | Avg first-token / prefill (ms) | Avg generation (tok/s) | Avg similarity to Q8_0 | Load time (s) |
|---|---|---|---|---|---|---|
| Q4_K_M | 12/12 | 1.52 | 425.34 | 42.68 | — | 14.7 |
| IQ3_M | 12/12 | 1.51 | 411.99 | 51.74 | — | 12.6 |

## Per prompt: correct and total time (s)

| Prompt | Category | Q4_K_M | IQ3_M |
|---|---|---|---|
| bat-ball | Logic | ✅ 2.95 | ✅ 3.63 |
| multiply | Math | ✅ 0.3 | ✅ 0.28 |
| word-problem | Math | ✅ 4.22 | ✅ 5.05 |
| sheep | Reasoning | ✅ 1.66 | ✅ 1.39 |
| palindrome-code | Code | ✅ 1.14 | ✅ 0.92 |
| capital | Knowledge | ✅ 0.27 | ✅ 0.26 |
| three-bullets | Instruction following | ✅ 1.66 | ✅ 1.05 |
| malayalam | Multilingual | ✅ 0.67 | ✅ 0.59 |
| hindi | Multilingual | ✅ 0.51 | ✅ 0.43 |
| summary | Summarization | · 1.38 | · 1.32 |
| needle | Long context | ✅ 3.4 | ✅ 3.34 |
| weather-tool | Tool calling | ✅ 1.15 | ✅ 0.96 |
| chart-vision | Vision | ✅ 0.44 | ✅ 0.41 |

✅ correct · ❌ wrong · · not graded (compare by reading)

## Answers side by side

### bat-ball (Logic)

> A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?

<details><summary><b>Q4_K_M</b> — 2.95 s, 116 tokens</summary>

```text
The ball costs **$0.05** (5 cents).

If the ball is $0.05, the bat is $1.05, and together they cost $1.10.
```

</details>

<details><summary><b>IQ3_M</b> — 3.63 s, 174 tokens</summary>

```text
The ball costs **$0.05** (5 cents).

Let the ball cost \(x\). Then the bat costs \(x + 1.00\).

\[
x + (x + 1.00) = 1.10
\]

\[
2x + 1.00 = 1.10
\]

\[
2x = 0.10
\]

\[
x = 0.05
\]
```

</details>

### multiply (Math)

> What is 17 multiplied by 23? Reply with just the number.

<details><summary><b>Q4_K_M</b> — 0.3 s, 4 tokens</summary>

```text
391
```

</details>

<details><summary><b>IQ3_M</b> — 0.28 s, 4 tokens</summary>

```text
391
```

</details>

### word-problem (Math)

> A shop sells pens at 12 rupees each. Riya buys 7 pens and pays with a 100 rupee note. She then spends half of her change on a notebook. How many rupees does she have left?

<details><summary><b>Q4_K_M</b> — 4.22 s, 172 tokens</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.

Change from 100 rupees: \(100 - 84 = 16\) rupees.

She spends half of the change: \(16 \div 2 = 8\) rupees.

So she has **8 rupees left**.
```

</details>

<details><summary><b>IQ3_M</b> — 5.05 s, 254 tokens</summary>

```text
Riya’s pens cost:

\[
7 \times 12 = 84
\]

Change from a 100-rupee note:

\[
100 - 84 = 16
\]

She spends half of her change on a notebook:

\[
16 \div 2 = 8
\]

So she has:

\[
16 - 8 = 8
\]

**Answer: 8 rupees**
```

</details>

### sheep (Reasoning)

> A farmer has 17 sheep. All but 9 run away. How many sheep does the farmer have left? Answer with the number.

<details><summary><b>Q4_K_M</b> — 1.66 s, 58 tokens</summary>

```text
9
```

</details>

<details><summary><b>IQ3_M</b> — 1.39 s, 58 tokens</summary>

```text
9
```

</details>

### palindrome-code (Code)

> Write a Python function is_palindrome(s) that returns True if the string s is a palindrome, ignoring case, spaces and punctuation. Reply with only the code in one Python code block.

<details><summary><b>Q4_K_M</b> — 1.14 s, 39 tokens</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>IQ3_M</b> — 0.92 s, 39 tokens</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

### capital (Knowledge)

> What is the capital city of Australia? Answer in one word.

<details><summary><b>Q4_K_M</b> — 0.27 s, 3 tokens</summary>

```text
Canberra
```

</details>

<details><summary><b>IQ3_M</b> — 0.26 s, 3 tokens</summary>

```text
Canberra
```

</details>

### three-bullets (Instruction following)

> Give exactly 3 bullet points on why model quantization is useful. Use '-' for each bullet and write nothing else.

<details><summary><b>Q4_K_M</b> — 1.66 s, 63 tokens</summary>

```text
- Reduces memory footprint by storing weights in lower precision formats, enabling deployment on resource-constrained devices.
- Accelerates inference speed by leveraging hardware optimizations for quantized data types, resulting in lower latency.
- Decreases bandwidth requirements for data transfer between memory and processing units, improving overall system efficiency.
```

</details>

<details><summary><b>IQ3_M</b> — 1.05 s, 47 tokens</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling faster computation on hardware optimized for reduced precision.
- Lowers energy consumption and operational costs during model deployment.
```

</details>

### malayalam (Multilingual)

> ഇന്ത്യയുടെ തലസ്ഥാനം ഏതാണ്? ഒരു വാക്യത്തിൽ ഉത്തരം നൽകുക.

<details><summary><b>Q4_K_M</b> — 0.67 s, 21 tokens</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>IQ3_M</b> — 0.59 s, 21 tokens</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

### hindi (Multilingual)

> भारत की राजधानी क्या है? एक वाक्य में उत्तर दें।

<details><summary><b>Q4_K_M</b> — 0.51 s, 13 tokens</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ3_M</b> — 0.43 s, 13 tokens</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

### summary (Summarization)

> Summarize in two sentences: Quantization stores the weights of a neural network with fewer bits, for example 4 bits instead of 16. This makes the model file several times smaller and lets it run on GPUs with less memory, and generation usually becomes faster because less data is read for every token

<details><summary><b>Q4_K_M</b> — 1.38 s, 50 tokens</summary>

```text
Quantization reduces neural network file size and improves speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degradation becoming more significant as the bit depth decreases.
```

</details>

<details><summary><b>IQ3_M</b> — 1.32 s, 60 tokens</summary>

```text
Quantization reduces neural network file sizes and improves generation speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, which remains minimal at 8-bit but becomes significantly more pronounced at lower bit depths like 3-bit.
```

</details>

### needle (Long context)

> Somewhere in the text above there is a sentence about a vault access code. What is the access code? Reply with just the number.

<details><summary><b>Q4_K_M</b> — 3.4 s, 5 tokens</summary>

```text
7341
```

</details>

<details><summary><b>IQ3_M</b> — 3.34 s, 5 tokens</summary>

```text
7341
```

</details>

### weather-tool (Tool calling)

> What's the weather in Paris right now?

<details><summary><b>Q4_K_M</b> — 1.15 s, 26 tokens</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>IQ3_M</b> — 0.96 s, 26 tokens</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

### chart-vision (Vision)

> This bar chart has a red, a green and a blue bar. Which colour is the tallest bar? Answer with one word.

<details><summary><b>Q4_K_M</b> — 0.44 s, 2 tokens</summary>

```text
green
```

</details>

<details><summary><b>IQ3_M</b> — 0.41 s, 2 tokens</summary>

```text
green
```

</details>
