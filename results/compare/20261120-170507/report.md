# Quant comparison: Qwen3.8-27B

13 prompts × 7 quants, temperature 0, seed 42, context 16384, 2 timing run(s) per prompt, llama.cpp b12345. Similarity is measured against the Q8_0 answer (1.0 = identical text).

## Summary

| Quant | Correct | Avg total time (s) | Avg first-token / prefill (ms) | Avg generation (tok/s) | Avg similarity to Q8_0 | Load time (s) |
|---|---|---|---|---|---|---|
| Q8_0 | 12/12 | 1.65 | 305.08 | 27.21 | — | 22.6 |
| Q6_K | 12/12 | 1.53 | 331.09 | 31.92 | 0.98 | 22.7 |
| Q5_K_M | 12/12 | 1.49 | 318.99 | 35.56 | 0.926 | 16.6 |
| Q4_K_M | 12/12 | 1.41 | 304.04 | 39.81 | 0.908 | 14.7 |
| IQ4_XS | 12/12 | 1.23 | 290.34 | 42.76 | 0.899 | 12.6 |
| Q3_K_M | 12/12 | 1.16 | 303.61 | 46.07 | 0.947 | 14.6 |
| IQ3_M | 12/12 | 1.45 | 301.52 | 47.05 | 0.854 | 12.6 |

## Per prompt: correct and total time (s)

| Prompt | Category | Q8_0 | Q6_K | Q5_K_M | Q4_K_M | IQ4_XS | Q3_K_M | IQ3_M |
|---|---|---|---|---|---|---|---|---|
| bat-ball | Logic | ✅ 3.06 | ✅ 2.84 | ✅ 2.52 | ✅ 3.13 | ✅ 2.21 | ✅ 2.15 | ✅ 3.81 |
| multiply | Math | ✅ 0.33 | ✅ 0.31 | ✅ 0.28 | ✅ 0.24 | ✅ 0.27 | ✅ 0.28 | ✅ 0.24 |
| word-problem | Math | ✅ 4.97 | ✅ 4.53 | ✅ 5.5 | ✅ 4.42 | ✅ 3.79 | ✅ 3.2 | ✅ 5.37 |
| sheep | Reasoning | ✅ 2.21 | ✅ 1.95 | ✅ 1.78 | ✅ 1.61 | ✅ 1.5 | ✅ 1.47 | ✅ 1.38 |
| palindrome-code | Code | ✅ 1.54 | ✅ 1.37 | ✅ 1.25 | ✅ 1.14 | ✅ 1.05 | ✅ 1.01 | ✅ 0.96 |
| capital | Knowledge | ✅ 0.31 | ✅ 0.31 | ✅ 0.29 | ✅ 0.28 | ✅ 0.26 | ✅ 0.25 | ✅ 0.27 |
| three-bullets | Instruction following | ✅ 1.8 | ✅ 1.74 | ✅ 1.4 | ✅ 1.73 | ✅ 1.37 | ✅ 1.09 | ✅ 1.2 |
| malayalam | Multilingual | ✅ 0.92 | ✅ 0.8 | ✅ 0.73 | ✅ 0.66 | ✅ 0.62 | ✅ 0.57 | ✅ 0.59 |
| hindi | Multilingual | ✅ 0.66 | ✅ 0.58 | ✅ 0.54 | ✅ 0.52 | ✅ 0.49 | ✅ 0.43 | ✅ 0.47 |
| summary | Summarization | · 2.04 | · 1.74 | · 1.6 | · 1.39 | · 1.34 | · 1.38 | · 1.42 |
| needle | Long context | ✅ 1.88 | ✅ 2.19 | ✅ 2.09 | ✅ 1.96 | ✅ 1.82 | ✅ 2.03 | ✅ 1.96 |
| weather-tool | Tool calling | ✅ 1.38 | ✅ 1.18 | ✅ 1.09 | ✅ 0.99 | ✅ 0.98 | ✅ 0.9 | ✅ 0.89 |
| chart-vision | Vision | ✅ 0.38 | ✅ 0.37 | ✅ 0.34 | ✅ 0.32 | ✅ 0.32 | ✅ 0.31 | ✅ 0.31 |

✅ correct · ❌ wrong · · not graded (compare by reading)

## Answers side by side

### bat-ball (Logic)

> A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?

<details><summary><b>Q8_0</b> — 3.06 s, 80 tokens</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>Q6_K</b> — 2.84 s, 80 tokens, similarity 1.0</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>Q5_K_M</b> — 2.52 s, 80 tokens, similarity 1.0</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>Q4_K_M</b> — 3.13 s, 116 tokens, similarity 0.496</summary>

```text
The ball costs **$0.05** (5 cents).

If the ball is $0.05, the bat is $1.05, and together they cost $1.10.
```

</details>

<details><summary><b>IQ4_XS</b> — 2.21 s, 86 tokens, similarity 1.0</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>Q3_K_M</b> — 2.15 s, 83 tokens, similarity 1.0</summary>

```text
The ball costs **$0.05** (5 cents).
```

</details>

<details><summary><b>IQ3_M</b> — 3.81 s, 174 tokens, similarity 0.326</summary>

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

<details><summary><b>Q6_K</b> — 0.31 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q5_K_M</b> — 0.28 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q4_K_M</b> — 0.24 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>IQ4_XS</b> — 0.27 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q3_K_M</b> — 0.28 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>IQ3_M</b> — 0.24 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

### word-problem (Math)

> A shop sells pens at 12 rupees each. Riya buys 7 pens and pays with a 100 rupee note. She then spends half of her change on a notebook. How many rupees does she have left?

<details><summary><b>Q8_0</b> — 4.97 s, 135 tokens</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.

Change from 100 rupees: \(100 - 84 = 16\) rupees.

She spends half of the change: \(16 \div 2 = 8\) rupees.

So she has **8 rupees left**.
```

</details>

<details><summary><b>Q6_K</b> — 4.53 s, 140 tokens, similarity 1.0</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.

Change from 100 rupees: \(100 - 84 = 16\) rupees.

She spends half of the change: \(16 \div 2 = 8\) rupees.

So she has **8 rupees left**.
```

</details>

<details><summary><b>Q5_K_M</b> — 5.5 s, 192 tokens, similarity 0.668</summary>

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

<details><summary><b>Q4_K_M</b> — 4.42 s, 172 tokens, similarity 1.0</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.

Change from 100 rupees: \(100 - 84 = 16\) rupees.

She spends half of the change: \(16 \div 2 = 8\) rupees.

So she has **8 rupees left**.
```

</details>

<details><summary><b>IQ4_XS</b> — 3.79 s, 156 tokens, similarity 0.252</summary>

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

<details><summary><b>Q3_K_M</b> — 3.2 s, 140 tokens, similarity 0.979</summary>

```text
Riya spends \(7 \times 12 = 84\) rupees on pens.  
Change from 100 rupees: \(100 - 84 = 16\) rupees.  
She spends half of the change: \(16 \div 2 = 8\) rupees.  

So she has **8 rupees left**.
```

</details>

<details><summary><b>IQ3_M</b> — 5.37 s, 254 tokens, similarity 0.429</summary>

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

<details><summary><b>Q8_0</b> — 2.21 s, 58 tokens</summary>

```text
9
```

</details>

<details><summary><b>Q6_K</b> — 1.95 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q5_K_M</b> — 1.78 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q4_K_M</b> — 1.61 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>IQ4_XS</b> — 1.5 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q3_K_M</b> — 1.47 s, 62 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>IQ3_M</b> — 1.38 s, 58 tokens, similarity 1.0</summary>

```text
9
```

</details>

### palindrome-code (Code)

> Write a Python function is_palindrome(s) that returns True if the string s is a palindrome, ignoring case, spaces and punctuation. Reply with only the code in one Python code block.

<details><summary><b>Q8_0</b> — 1.54 s, 39 tokens</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q6_K</b> — 1.37 s, 39 tokens, similarity 0.967</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q5_K_M</b> — 1.25 s, 39 tokens, similarity 1.0</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q4_K_M</b> — 1.14 s, 39 tokens, similarity 0.967</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>IQ4_XS</b> — 1.05 s, 39 tokens, similarity 0.978</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q3_K_M</b> — 1.01 s, 39 tokens, similarity 0.978</summary>

```text
```python
def is_palindrome(s):
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>IQ3_M</b> — 0.96 s, 39 tokens, similarity 1.0</summary>

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

<details><summary><b>Q8_0</b> — 0.31 s, 3 tokens</summary>

```text
Canberra
```

</details>

<details><summary><b>Q6_K</b> — 0.31 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q5_K_M</b> — 0.29 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q4_K_M</b> — 0.28 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>IQ4_XS</b> — 0.26 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q3_K_M</b> — 0.25 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>IQ3_M</b> — 0.27 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

### three-bullets (Instruction following)

> Give exactly 3 bullet points on why model quantization is useful. Use '-' for each bullet and write nothing else.

<details><summary><b>Q8_0</b> — 1.8 s, 45 tokens</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by leveraging hardware optimizations for quantized operations.
- Lowers computational costs and energy consumption during model deployment.
```

</details>

<details><summary><b>Q6_K</b> — 1.74 s, 50 tokens, similarity 0.772</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by leveraging hardware optimizations for quantized operations.
- Lowers computational cost and energy consumption, enabling deployment on resource-constrained devices.
```

</details>

<details><summary><b>Q5_K_M</b> — 1.4 s, 44 tokens, similarity 0.655</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling faster arithmetic operations on hardware.
- Lowers energy consumption and computational costs during model deployment.
```

</details>

<details><summary><b>Q4_K_M</b> — 1.73 s, 63 tokens, similarity 0.373</summary>

```text
- Reduces memory footprint by storing weights in lower precision formats, enabling deployment on resource-constrained devices.
- Accelerates inference speed by leveraging hardware optimizations for quantized data types, resulting in lower latency.
- Decreases bandwidth requirements for data transfer between memory and processing units, improving overall system efficiency.
```

</details>

<details><summary><b>IQ4_XS</b> — 1.37 s, 51 tokens, similarity 0.552</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling faster computation on hardware optimized for reduced precision.
- Lowers energy consumption and operational costs, making deployment feasible on edge devices.
```

</details>

<details><summary><b>Q3_K_M</b> — 1.09 s, 44 tokens, similarity 0.664</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling more efficient computation on hardware.
- Lowers energy consumption and operational costs during model deployment.
```

</details>

<details><summary><b>IQ3_M</b> — 1.2 s, 47 tokens, similarity 0.664</summary>

```text
- Reduces memory footprint and storage requirements by using lower-precision data types.
- Accelerates inference speed by enabling faster computation on hardware optimized for reduced precision.
- Lowers energy consumption and operational costs during model deployment.
```

</details>

### malayalam (Multilingual)

> ഇന്ത്യയുടെ തലസ്ഥാനം ഏതാണ്? ഒരു വാക്യത്തിൽ ഉത്തരം നൽകുക.

<details><summary><b>Q8_0</b> — 0.92 s, 21 tokens</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q6_K</b> — 0.8 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.73 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.66 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.62 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.57 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>IQ3_M</b> — 0.59 s, 21 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

### hindi (Multilingual)

> भारत की राजधानी क्या है? एक वाक्य में उत्तर दें।

<details><summary><b>Q8_0</b> — 0.66 s, 13 tokens</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q6_K</b> — 0.58 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q5_K_M</b> — 0.54 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q4_K_M</b> — 0.52 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ4_XS</b> — 0.49 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q3_K_M</b> — 0.43 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ3_M</b> — 0.47 s, 13 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

### summary (Summarization)

> Summarize in two sentences: Quantization stores the weights of a neural network with fewer bits, for example 4 bits instead of 16. This makes the model file several times smaller and lets it run on GPUs with less memory, and generation usually becomes faster because less data is read for every token

<details><summary><b>Q8_0</b> — 2.04 s, 51 tokens</summary>

```text
Quantization reduces neural network model size and improves inference speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degradation becoming more significant as the bit depth decreases.
```

</details>

<details><summary><b>Q6_K</b> — 1.74 s, 51 tokens, similarity 1.0</summary>

```text
Quantization reduces neural network model size and improves inference speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degradation becoming more significant as the bit depth decreases.
```

</details>

<details><summary><b>Q5_K_M</b> — 1.6 s, 51 tokens, similarity 0.909</summary>

```text
Quantization reduces neural network model size and improves inference speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degree of loss increasing as the bit depth decreases.
```

</details>

<details><summary><b>Q4_K_M</b> — 1.39 s, 50 tokens, similarity 0.968</summary>

```text
Quantization reduces neural network file size and improves speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degradation becoming more significant as the bit depth decreases.
```

</details>

<details><summary><b>IQ4_XS</b> — 1.34 s, 51 tokens, similarity 0.909</summary>

```text
Quantization reduces neural network model size and improves inference speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, with the degree of loss increasing as the bit depth decreases.
```

</details>

<details><summary><b>Q3_K_M</b> — 1.38 s, 57 tokens, similarity 0.692</summary>

```text
Quantization reduces neural network file sizes and improves generation speed by storing weights with fewer bits, enabling operation on GPUs with limited memory. However, this efficiency comes at the cost of reduced accuracy, which becomes more pronounced as the bit depth decreases from 8-bit to 3-bit.
```

</details>

<details><summary><b>IQ3_M</b> — 1.42 s, 60 tokens, similarity 0.68</summary>

```text
Quantization reduces neural network file sizes and improves generation speed by storing weights with fewer bits, enabling operation on hardware with limited memory. However, this efficiency comes at the cost of reduced accuracy, which remains minimal at 8-bit but becomes significantly more pronounced at lower bit depths like 3-bit.
```

</details>

### needle (Long context)

> Somewhere in the text above there is a sentence about a vault access code. What is the access code? Reply with just the number.

<details><summary><b>Q8_0</b> — 1.88 s, 5 tokens</summary>

```text
7341
```

</details>

<details><summary><b>Q6_K</b> — 2.19 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q5_K_M</b> — 2.09 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q4_K_M</b> — 1.96 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>IQ4_XS</b> — 1.82 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q3_K_M</b> — 2.03 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>IQ3_M</b> — 1.96 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

### weather-tool (Tool calling)

> What's the weather in Paris right now?

<details><summary><b>Q8_0</b> — 1.38 s, 26 tokens</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>Q6_K</b> — 1.18 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>Q5_K_M</b> — 1.09 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>Q4_K_M</b> — 0.99 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>IQ4_XS</b> — 0.98 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>Q3_K_M</b> — 0.9 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

<details><summary><b>IQ3_M</b> — 0.89 s, 26 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\":\"Paris\"}"}]
```

</details>

### chart-vision (Vision)

> This bar chart has a red, a green and a blue bar. Which colour is the tallest bar? Answer with one word.

<details><summary><b>Q8_0</b> — 0.38 s, 2 tokens</summary>

```text
green
```

</details>

<details><summary><b>Q6_K</b> — 0.37 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>

<details><summary><b>Q5_K_M</b> — 0.34 s, 2 tokens, similarity 0.8</summary>

```text
Green
```

</details>

<details><summary><b>Q4_K_M</b> — 0.32 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>

<details><summary><b>IQ4_XS</b> — 0.32 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>

<details><summary><b>Q3_K_M</b> — 0.31 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>

<details><summary><b>IQ3_M</b> — 0.31 s, 2 tokens, similarity 1.0</summary>

```text
green
```

</details>
