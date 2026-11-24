# Quant comparison: Qwen3.8-27B

13 prompts × 7 quants, temperature 0, seed 42, context 16384, 2 timing run(s) per prompt, llama.cpp b12345. Similarity is measured against the Q8_0 answer (1.0 = identical text).

## Summary

| Quant | Correct | Avg total time (s) | Avg first-token / prefill (ms) | Avg generation (tok/s) | Avg similarity to Q8_0 | Load time (s) |
|---|---|---|---|---|---|---|
| Q8_0 | 12/12 | 1.64 | 294.33 | 27.28 | — | 37.3 |
| Q6_K | 12/12 | 1.46 | 331.62 | 33.89 | 0.98 | 16.6 |
| Q5_K_M | 12/12 | 1.43 | 318.39 | 37.29 | 0.926 | 14.6 |
| Q4_K_M | 12/12 | 1.37 | 310.27 | 42.22 | 0.908 | 14.6 |
| IQ4_XS | 12/12 | 1.18 | 291.45 | 45.5 | 0.899 | 14.6 |
| Q3_K_M | 12/12 | 1.11 | 303.46 | 48.91 | 0.947 | 12.6 |
| IQ3_M | 12/12 | 1.41 | 301.5 | 49.78 | 0.854 | 12.6 |

## Per prompt: correct and total time (s)

| Prompt | Category | Q8_0 | Q6_K | Q5_K_M | Q4_K_M | IQ4_XS | Q3_K_M | IQ3_M |
|---|---|---|---|---|---|---|---|---|
| bat-ball | Logic | ✅ 3.15 | ✅ 2.57 | ✅ 2.31 | ✅ 3.01 | ✅ 2.1 | ✅ 1.9 | ✅ 3.71 |
| multiply | Math | ✅ 0.33 | ✅ 0.32 | ✅ 0.32 | ✅ 0.26 | ✅ 0.27 | ✅ 0.3 | ✅ 0.23 |
| word-problem | Math | ✅ 5.02 | ✅ 4.26 | ✅ 5.27 | ✅ 4.17 | ✅ 3.59 | ✅ 3.03 | ✅ 5.22 |
| sheep | Reasoning | ✅ 2.23 | ✅ 1.86 | ✅ 1.68 | ✅ 1.55 | ✅ 1.41 | ✅ 1.4 | ✅ 1.33 |
| palindrome-code | Code | ✅ 1.56 | ✅ 1.33 | ✅ 1.21 | ✅ 1.1 | ✅ 1.01 | ✅ 0.96 | ✅ 0.94 |
| capital | Knowledge | ✅ 0.28 | ✅ 0.28 | ✅ 0.28 | ✅ 0.29 | ✅ 0.27 | ✅ 0.26 | ✅ 0.25 |
| three-bullets | Instruction following | ✅ 1.81 | ✅ 1.7 | ✅ 1.35 | ✅ 1.71 | ✅ 1.29 | ✅ 1.12 | ✅ 1.14 |
| malayalam | Multilingual | ✅ 0.88 | ✅ 0.75 | ✅ 0.68 | ✅ 0.63 | ✅ 0.63 | ✅ 0.55 | ✅ 0.54 |
| hindi | Multilingual | ✅ 0.6 | ✅ 0.55 | ✅ 0.53 | ✅ 0.48 | ✅ 0.47 | ✅ 0.45 | ✅ 0.45 |
| summary | Summarization | · 1.97 | · 1.66 | · 1.51 | · 1.33 | · 1.27 | · 1.31 | · 1.37 |
| needle | Long context | ✅ 1.84 | ✅ 2.13 | ✅ 2.03 | ✅ 1.93 | ✅ 1.77 | ✅ 1.96 | ✅ 1.93 |
| weather-tool | Tool calling | ✅ 1.25 | ✅ 1.17 | ✅ 1.04 | ✅ 0.98 | ✅ 0.94 | ✅ 0.89 | ✅ 0.86 |
| chart-vision | Vision | ✅ 0.4 | ✅ 0.37 | ✅ 0.33 | ✅ 0.33 | ✅ 0.32 | ✅ 0.34 | ✅ 0.31 |

✅ correct · ❌ wrong · · not graded (compare by reading)

## Answers side by side

### bat-ball (Logic)

> A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?

<details><summary><b>Q8_0</b> — 3.15 s, 80 tokens</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>Q6_K</b> — 2.57 s, 80 tokens, similarity 1.0</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>Q5_K_M</b> — 2.31 s, 80 tokens, similarity 1.0</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>Q4_K_M</b> — 3.01 s, 116 tokens, similarity 0.496</summary>

```text
The ball costs **$0.05** (5 cents).

If the ball is $0.05, the bat is $1.05, and together they cost $1.10.
```

</details>

<details><summary><b>IQ4_XS</b> — 2.1 s, 86 tokens, similarity 1.0</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>Q3_K_M</b> — 1.9 s, 83 tokens, similarity 1.0</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>IQ3_M</b> — 3.71 s, 174 tokens, similarity 0.326</summary>

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

<details><summary><b>Q8_0</b> — 0.33 s, 4 tokens</summary>

```text
391
```

</details>

<details><summary><b>Q6_K</b> — 0.32 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q5_K_M</b> — 0.32 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q4_K_M</b> — 0.26 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>IQ4_XS</b> — 0.27 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q3_K_M</b> — 0.3 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>IQ3_M</b> — 0.23 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

### word-problem (Math)

> A shop sells pens at 12 rupees each. Riya buys 7 pens and pays with a 100 rupee note. She then spends half of her change on a notebook. How many rupees does she have left?

<details><summary><b>Q8_0</b> — 5.02 s, 135 tokens</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.

Change from 100 rupees: \(100 - 84 = 16\) rupees.

She spends half of the change: \(16 \div 2 = 8\) rupees.

So she has **8 rupees left**.
```

</details>

<details><summary><b>Q6_K</b> — 4.26 s, 140 tokens, similarity 1.0</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.

Change from 100 rupees: \(100 - 84 = 16\) rupees.

She spends half of the change: \(16 \div 2 = 8\) rupees.

So she has **8 rupees left**.
```

</details>

<details><summary><b>Q5_K_M</b> — 5.27 s, 192 tokens, similarity 0.668</summary>

```text
Riya’s pens cost:

\(7 \times 12 = 84\) rupees

Change from 100 rupees:

\(100 - 84 = 16\) rupees

She spends half of her change:

\(16 \div 2 = 8\) rupees

So she has:

\(16 - 8 = 8\) rupees left.

**Answer: 8 rupees**
```

</details>

<details><summary><b>Q4_K_M</b> — 4.17 s, 172 tokens, similarity 1.0</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.

Change from 100 rupees: \(100 - 84 = 16\) rupees.

She spends half of the change: \(16 \div 2 = 8\) rupees.

So she has **8 rupees left**.
```

</details>

<details><summary><b>IQ4_XS</b> — 3.59 s, 156 tokens, similarity 0.252</summary>

```text
Riya buys 7 pens at 12 rupees each:

7 × 12 = 84 rupees

She pays with a 100 rupee note, so her change is:

100 − 84 = 16 rupees

She spends half of her change on a notebook:

16 ÷ 2 = 8 rupees

So she has **8 rupees left**.
```

</details>

<details><summary><b>Q3_K_M</b> — 3.03 s, 140 tokens, similarity 0.979</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.  
Change from 100 rupees: \(100 - 84 = 16\) rupees.  
She spends half of the change: \(16 \div 2 = 8\) rupees.  

So she has **8 rupees left**.
```

</details>

<details><summary><b>IQ3_M</b> — 5.22 s, 254 tokens, similarity 0.429</summary>

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

<details><summary><b>Q8_0</b> — 2.23 s, 58 tokens</summary>

```text
9
```

</details>

<details><summary><b>Q6_K</b> — 1.86 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q5_K_M</b> — 1.68 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q4_K_M</b> — 1.55 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>IQ4_XS</b> — 1.41 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q3_K_M</b> — 1.4 s, 62 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>IQ3_M</b> — 1.33 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

### palindrome-code (Code)

> Write a Python function is_palindrome(s) that returns True if the string s is a palindrome, ignoring case, spaces and punctuation. Reply with only the code in one Python code block.

<details><summary><b>Q8_0</b> — 1.56 s, 39 tokens</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q6_K</b> — 1.33 s, 39 tokens, similarity 0.967</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q5_K_M</b> — 1.21 s, 39 tokens, similarity 1.0</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q4_K_M</b> — 1.1 s, 39 tokens, similarity 0.967</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>IQ4_XS</b> — 1.01 s, 39 tokens, similarity 0.978</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q3_K_M</b> — 0.96 s, 39 tokens, similarity 0.978</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>IQ3_M</b> — 0.94 s, 39 tokens, similarity 1.0</summary>

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

<details><summary><b>Q8_0</b> — 0.28 s, 3 tokens</summary>

```text
Canberra
```

</details>

<details><summary><b>Q6_K</b> — 0.28 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q5_K_M</b> — 0.28 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q4_K_M</b> — 0.29 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>IQ4_XS</b> — 0.27 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q3_K_M</b> — 0.26 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>IQ3_M</b> — 0.25 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

### three-bullets (Instruction following)

> Give exactly 3 bullet points on why model quantization is useful. Use '-' for each bullet and write nothing else.

<details><summary><b>Q8_0</b> — 1.81 s, 45 tokens</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by leveraging hardware optimizations for quantized operations.
- Lowers computational costs and energy consumption during model deployment.
```

</details>

<details><summary><b>Q6_K</b> — 1.7 s, 50 tokens, similarity 0.772</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by leveraging hardware optimizations for quantized operations.
- Lowers computational cost and energy consumption, enabling deployment on resource-constrained devices.
```

</details>

<details><summary><b>Q5_K_M</b> — 1.35 s, 44 tokens, similarity 0.655</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling faster arithmetic operations on hardware.
- Lowers energy consumption and computational costs during model deployment.
```

</details>

<details><summary><b>Q4_K_M</b> — 1.71 s, 63 tokens, similarity 0.373</summary>

```text
- Reduces memory footprint by storing weights in lower precision formats, enabling deployment on resource-constrained devices.
- Accelerates inference speed by leveraging hardware optimizations for quantized data types, resulting in lower latency.
- Decreases bandwidth requirements for data transfer between memory and processing units, improving overall system efficiency.
```

</details>

<details><summary><b>IQ4_XS</b> — 1.29 s, 51 tokens, similarity 0.552</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling faster computation on hardware optimized for reduced precision.
- Lowers energy consumption and operational costs, making deployment feasible on edge devices.
```

</details>

<details><summary><b>Q3_K_M</b> — 1.12 s, 44 tokens, similarity 0.664</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling more efficient computation on hardware.
- Lowers energy consumption and operational costs during model deployment.
```

</details>

<details><summary><b>IQ3_M</b> — 1.14 s, 47 tokens, similarity 0.664</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling faster computation on hardware optimized for reduced precision.
- Lowers energy consumption and operational costs during model deployment.
```

</details>

### malayalam (Multilingual)

> ഇന്ത്യയുടെ തലസ്ഥാനം ഏതാണ്? ഒരു വാക്യത്തിൽ ഉത്തരം നൽകുക.

<details><summary><b>Q8_0</b> — 0.88 s, 21 tokens</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q6_K</b> — 0.75 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.68 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.63 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.63 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.55 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>IQ3_M</b> — 0.54 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

### hindi (Multilingual)

> भारत की राजधानी क्या है? एक वाक्य में उत्तर दें।

<details><summary><b>Q8_0</b> — 0.6 s, 13 tokens</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q6_K</b> — 0.55 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q5_K_M</b> — 0.53 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q4_K_M</b> — 0.48 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ4_XS</b> — 0.47 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q3_K_M</b> — 0.45 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ3_M</b> — 0.45 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

### summary (Summarization)

> Summarize in two sentences: Quantization stores the weights of a neural network with fewer bits, for example 4 bits instead of 16. This makes the model file several times smaller and lets it run on GPUs with less memory, and generation usually becomes faster because less data is read for every token

<details><summary><b>Q8_0</b> — 1.97 s, 51 tokens</summary>

```text
Quantization reduces neural network model size and improves inference speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degradation becoming more significant as the bit depth decreases.
```

</details>

<details><summary><b>Q6_K</b> — 1.66 s, 51 tokens, similarity 1.0</summary>

```text
Quantization reduces neural network model size and improves inference speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degradation becoming more significant as the bit depth decreases.
```

</details>

<details><summary><b>Q5_K_M</b> — 1.51 s, 51 tokens, similarity 0.909</summary>

```text
Quantization reduces neural network model size and improves inference speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degree of loss increasing as the bit depth decreases.
```

</details>

<details><summary><b>Q4_K_M</b> — 1.33 s, 50 tokens, similarity 0.968</summary>

```text
Quantization reduces neural network file size and improves speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degradation becoming more significant as the bit depth decreases.
```

</details>

<details><summary><b>IQ4_XS</b> — 1.27 s, 51 tokens, similarity 0.909</summary>

```text
Quantization reduces neural network model size and improves inference speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degree of loss increasing as the bit depth decreases.
```

</details>

<details><summary><b>Q3_K_M</b> — 1.31 s, 57 tokens, similarity 0.692</summary>

```text
Quantization reduces neural network file sizes and improves generation speed by storing weights with fewer bits, enabling operation on GPUs with limited memory. However, this efficiency comes at the cost of reduced accuracy, which becomes more pronounced as the bit depth decreases from 8-bit to 3-bit.
```

</details>

<details><summary><b>IQ3_M</b> — 1.37 s, 60 tokens, similarity 0.68</summary>

```text
Quantization reduces neural network file sizes and improves generation speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, which remains minimal at 8-bit but becomes significantly more pronounced at lower bit depths like 3-bit.
```

</details>

### needle (Long context)

> Somewhere in the text above there is a sentence about a vault access code. What is the access code? Reply with just the number.

<details><summary><b>Q8_0</b> — 1.84 s, 5 tokens</summary>

```text
7341
```

</details>

<details><summary><b>Q6_K</b> — 2.13 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q5_K_M</b> — 2.03 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q4_K_M</b> — 1.93 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>IQ4_XS</b> — 1.77 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q3_K_M</b> — 1.96 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>IQ3_M</b> — 1.93 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

### weather-tool (Tool calling)

> What's the weather in Paris right now?

<details><summary><b>Q8_0</b> — 1.25 s, 26 tokens</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>Q6_K</b> — 1.17 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>Q5_K_M</b> — 1.04 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>Q4_K_M</b> — 0.98 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>IQ4_XS</b> — 0.94 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>Q3_K_M</b> — 0.89 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>IQ3_M</b> — 0.86 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

### chart-vision (Vision)

> This bar chart has a red, a green and a blue bar. Which colour is the tallest bar? Answer with one word.

<details><summary><b>Q8_0</b> — 0.4 s, 2 tokens</summary>

```text
green
```

</details>

<details><summary><b>Q6_K</b> — 0.37 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>

<details><summary><b>Q5_K_M</b> — 0.33 s, 2 tokens, similarity 0.8</summary>

```text
Green
```

</details>

<details><summary><b>Q4_K_M</b> — 0.33 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>

<details><summary><b>IQ4_XS</b> — 0.32 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>

<details><summary><b>Q3_K_M</b> — 0.34 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>

<details><summary><b>IQ3_M</b> — 0.31 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>
