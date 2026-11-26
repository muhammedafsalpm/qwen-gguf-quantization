# Quant comparison: Qwen3-14B

12 prompts × 7 quants, temperature 0, seed 42, context 16384, 2 timing run(s) per prompt, llama.cpp b12345. Similarity is measured against the Q8_0 answer (1.0 = identical text).

## Summary

| Quant | Correct | Avg total time (s) | Avg first-token / prefill (ms) | Avg generation (tok/s) | Avg similarity to Q8_0 | Load time (s) |
|---|---|---|---|---|---|---|
| Q8_0 | 11/11 | 6.35 | 112.12 | 50.7 | — | 12.7 |
| Q6_K | 11/11 | 4.53 | 124.17 | 62.62 | 0.918 | 10.6 |
| Q5_K_M | 11/11 | 4.39 | 114.03 | 69.97 | 0.848 | 8.6 |
| Q4_K_M | 11/11 | 4.42 | 109.88 | 79.46 | 0.837 | 8.6 |
| IQ4_XS | 10/11 | 3.41 | 103.53 | 85.79 | 0.816 | 8.6 |
| Q3_K_M | 10/11 | 3.67 | 116.36 | 90.7 | 0.798 | 6.6 |
| IQ3_M | 10/11 | 3.47 | 104.72 | 92.13 | 0.843 | 10.6 |

## Per prompt: correct and total time (s)

| Prompt | Category | Q8_0 | Q6_K | Q5_K_M | Q4_K_M | IQ4_XS | Q3_K_M | IQ3_M |
|---|---|---|---|---|---|---|---|---|
| bat-ball | Logic | ✅ 35.11 | ✅ 19.63 | ✅ 25.28 | ✅ 26.67 | ✅ 18.36 | ✅ 21.02 | ✅ 16.43 |
| multiply | Math | ✅ 0.18 | ✅ 0.16 | ✅ 0.16 | ✅ 0.13 | ✅ 0.15 | ✅ 0.14 | ✅ 0.12 |
| word-problem | Math | ✅ 27.47 | ✅ 21.79 | ✅ 16.71 | ✅ 16.63 | ✅ 14.22 | ✅ 10.96 | ✅ 14.7 |
| sheep | Reasoning | ✅ 6.88 | ✅ 6.97 | ✅ 5.46 | ✅ 4.9 | ✅ 3.86 | ✅ 7.49 | ✅ 6.19 |
| palindrome-code | Code | ✅ 0.81 | ✅ 0.66 | ✅ 0.6 | ✅ 0.55 | ✅ 0.54 | ✅ 0.48 | ✅ 0.46 |
| capital | Knowledge | ✅ 0.1 | ✅ 0.09 | ✅ 0.08 | ✅ 0.08 | ✅ 0.08 | ✅ 0.06 | ✅ 0.06 |
| three-bullets | Instruction following | ✅ 1.0 | ✅ 0.82 | ✅ 0.67 | ✅ 0.59 | ✅ 0.56 | ✅ 0.56 | ✅ 0.63 |
| malayalam | Multilingual | ✅ 0.91 | ✅ 0.75 | ✅ 0.67 | ✅ 0.62 | ❌ 0.58 | ❌ 0.55 | ❌ 0.54 |
| hindi | Multilingual | ✅ 0.59 | ✅ 0.47 | ✅ 0.45 | ✅ 0.39 | ✅ 0.35 | ✅ 0.35 | ✅ 0.33 |
| summary | Summarization | · 1.34 | · 1.09 | · 0.83 | · 0.82 | · 0.69 | · 0.74 | · 0.69 |
| needle | Long context | ✅ 1.18 | ✅ 1.33 | ✅ 1.24 | ✅ 1.17 | ✅ 1.09 | ✅ 1.22 | ✅ 1.08 |
| weather-tool | Tool calling | ✅ 0.64 | ✅ 0.57 | ✅ 0.54 | ✅ 0.51 | ✅ 0.49 | ✅ 0.46 | ✅ 0.46 |

✅ correct · ❌ wrong · · not graded (compare by reading)

## Answers side by side

### bat-ball (Logic)

> A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?

<details><summary><b>Q8_0</b> — 35.11 s, 1773 tokens</summary>

```text
To solve the problem, we are given the following information:

- A bat and a ball together cost **$1.10**.
- The **bat costs $1.00 more than the ball**.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.  
Then, the cost of the **bat** is $ x + 1.00 $ dollars.

---

### Step 2: Set Up the Equation

The total cost of the bat and the ball is given as $1.10:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

---

### Step 3: Solve for $ x $

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Divide both sides by 2:

$$
x = 0.05
$$

---

### Step 4: Interpret the Result

The ball costs **$0.05** (or 5 cents), and the bat costs $0.05 + $1.00 = **$1.05**.

Check the total:

$$
0.05 + 1.05 = 1.10
$$

This confirms the solution is correct.

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

<details><summary><b>Q6_K</b> — 19.63 s, 1251 tokens, similarity 0.976</summary>

```text
To solve the problem, we are given the following information:

- A bat and a ball together cost **$1.10**.
- The **bat costs $1.00 more than the ball**.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.

Then, the cost of the **bat** is $ x + 1.00 $ dollars.

---

### Step 2: Set Up the Equation

The total cost of the bat and the ball is $1.10:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

---

### Step 3: Solve for $ x $

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Divide both sides by 2:

$$
x = 0.05
$$

---

### Step 4: Interpret the Result

The ball costs **$0.05** (or 5 cents), and the bat costs:

$$
x + 1.00 = 0.05 + 1.00 = 1.05
$$

Check the total:

$$
0.05 + 1.05 = 1.10
$$

This confirms the solution is correct.

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

<details><summary><b>Q5_K_M</b> — 25.28 s, 1794 tokens, similarity 0.609</summary>

```text
To solve the problem, we are told that:

- A bat and a ball together cost **$1.10**.
- The **bat costs $1.00 more than the ball**.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.

Then, the **bat** costs $ x + 1.00 $ dollars.

---

### Step 2: Set Up the Equation

The total cost of the bat and the ball is given as $1.10:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

---

### Step 3: Solve for $ x $

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Divide both sides by 2:

$$
x = 0.05
$$

---

### Step 4: Interpret the Result

So, the **ball costs $0.05** (5 cents), and the **bat costs $1.05**.

Let’s verify:

- Ball: $0.05
- Bat: $1.05
- Total: $0.05 + $1.05 = $1.10 ✅
- Bat is $1.00 more than the ball: $1.05 - $0.05 = $1.00 ✅

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

<details><summary><b>Q4_K_M</b> — 26.67 s, 2133.5 tokens, similarity 0.591</summary>

```text
To solve the problem, we begin by translating the given information into a mathematical model.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.  
Since the **bat costs $1.00 more than the ball**, the cost of the **bat** is $ x + 1.00 $ dollars.

---

### Step 2: Use the Total Cost

We are told that the **total cost** of the bat and the ball is $1.10. So, we can write the equation:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

---

### Step 3: Solve for $ x $

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Now divide both sides by 2:

$$
x = 0.05
$$

---

### Step 4: Interpret the Result

This means the **ball costs $0.05** (or 5 cents), and the **bat costs $1.05** (since it is $1.00 more than the ball).  
Checking the total:

$$
0.05 + 1.05 = 1.10
$$

This confirms the solution is correct.

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

<details><summary><b>IQ4_XS</b> — 18.36 s, 1572 tokens, similarity 0.14</summary>

```text
To solve the problem, we begin by translating the given information into a mathematical equation.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.

Since the **bat costs $1.00 more than the ball**, the cost of the **bat** is $ x + 1.00 $ dollars.

---

### Step 2: Use the Total Cost

We are told that the **total cost of the bat and the ball is $1.10**. So, we can write the equation:

$$
x + (x + 1.00) = 1.10
$$

---

### Step 3: Simplify the Equation

$$
2x + 1.00 = 1.10
$$

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Divide both sides by 2:

$$
x = 0.05
$$

---

### Step 4: Interpret the Result

The value of $ x $ is **$0.05**, which means the **ball costs 5 cents**.

To verify:

- Ball: $0.05
- Bat: $0.05 + $1.00 = $1.05
- Total: $0.05 + $1.05 = $1.10 ✅

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

<details><summary><b>Q3_K_M</b> — 21.02 s, 1938 tokens, similarity 0.792</summary>

```text
To solve the problem, we are told that:

- A bat and a ball together cost **$1.10**.
- The **bat costs $1.00 more than the ball**.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.  
Then, the cost of the **bat** is $ x + 1.00 $ dollars.

---

### Step 2: Set Up the Equation

The total cost of the bat and the ball is $1.10:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

---

### Step 3: Solve for $ x $

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Divide both sides by 2:

$$
x = 0.05
$$

---

### Step 4: Interpret the Result

- The **ball costs** $ x = 0.05 $ dollars.
- The **bat costs** $ x + 1.00 = 1.05 $ dollars.
- Total: $ 0.05 + 1.05 = 1.10 $, which matches the given total.

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

<details><summary><b>IQ3_M</b> — 16.43 s, 1495.5 tokens, similarity 0.581</summary>

```text
To solve the problem, we begin by translating the given information into a mathematical equation.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.  
Then, the **bat** costs $ x + 1.00 $ dollars, since it is $1.00 more than the ball.

---

### Step 2: Set Up the Equation

The total cost of the bat and the ball is $1.10. So:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

---

### Step 3: Solve for $ x $

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Divide both sides by 2:

$$
x = 0.05
$$

---

### Step 4: Interpret the Result

This means the **ball costs $0.05** (or 5 cents), and the **bat costs $1.05**, which is indeed $1.00 more than the ball. The total is:

$$
0.05 + 1.05 = 1.10
$$

This confirms the solution is consistent with the problem's conditions.

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

### multiply (Math)

> What is 17 multiplied by 23? Reply with just the number.

<details><summary><b>Q8_0</b> — 0.18 s, 4 tokens</summary>

```text
391
```

</details>

<details><summary><b>Q6_K</b> — 0.16 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q5_K_M</b> — 0.16 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q4_K_M</b> — 0.13 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>IQ4_XS</b> — 0.15 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q3_K_M</b> — 0.14 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>IQ3_M</b> — 0.12 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

### word-problem (Math)

> A shop sells pens at 12 rupees each. Riya buys 7 pens and pays with a 100 rupee note. She then spends half of her change on a notebook. How many rupees does she have left?

<details><summary><b>Q8_0</b> — 27.47 s, 1388.5 tokens</summary>

```text
To determine how many rupees Riya has left, we'll break the problem into clear steps:

---

### **Step 1: Cost of Pens**
Riya buys **7 pens**, each costing **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### **Step 2: Change Received**
She pays with a **100 rupee note**, so the change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### **Step 3: Spending on a Notebook**
She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### **Step 4: Remaining Money**
Now, subtract the amount spent on the notebook from the change she had:

$$
\text{Remaining money} = 16 - 8 = 8 \text{ rupees}
$$

---

### **Final Answer**
$$
\boxed{8}
$$
```

</details>

<details><summary><b>Q6_K</b> — 21.79 s, 1363.5 tokens, similarity 0.954</summary>

```text
To determine how many rupees Riya has left, we'll break the problem into clear steps:

---

### **Step 1: Cost of Pens**
Riya buys **7 pens**, each costing **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### **Step 2: Payment and Change Received**
She pays with a **100 rupee note**.

$$
\text{Change received} = 100 - 84 = 16 \text{ rupees}
$$

---

### **Step 3: Spending on a Notebook**
She spends **half of her change** on a notebook.

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### **Step 4: Remaining Money**
Now, subtract the amount spent on the notebook from the change she had:

$$
\text{Remaining money} = 16 - 8 = 8 \text{ rupees}
$$

---

### ✅ Final Answer:
$$
\boxed{8}
$$
```

</details>

<details><summary><b>Q5_K_M</b> — 16.71 s, 1181.5 tokens, similarity 0.549</summary>

```text
To determine how many rupees Riya has left, let's break the problem into clear steps:

---

### Step 1: Calculate the total cost of the pens

Riya buys **7 pens**, each costing **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### Step 2: Determine the change received

Riya pays with a **100 rupee note**.

$$
\text{Change received} = 100 - 84 = 16 \text{ rupees}
$$

---

### Step 3: Calculate the amount spent on the notebook

She spends **half of her change** on a notebook.

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### Step 4: Determine the remaining amount

$$
\text{Remaining amount} = 16 - 8 = 8 \text{ rupees}
$$

---

### Final Answer

$$
\boxed{8}
$$
```

</details>

<details><summary><b>Q4_K_M</b> — 16.63 s, 1325 tokens, similarity 0.511</summary>

```text
To determine how many rupees Riya has left, we'll break the problem into clear steps:

---

### Step 1: Calculate the total cost of the pens

Each pen costs **12 rupees**, and Riya buys **7 pens**:

$$
7 \times 12 = 84 \text{ rupees}
$$

---

### Step 2: Determine the change she receives

Riya pays with a **100 rupee note**, so the change she gets back is:

$$
100 - 84 = 16 \text{ rupees}
$$

---

### Step 3: Calculate how much she spends on the notebook

She spends **half of her change** on a notebook:

$$
\frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### Step 4: Determine how much money she has left

After spending 8 rupees on the notebook, the remaining amount is:

$$
16 - 8 = 8 \text{ rupees}
$$

---

### Final Answer:

$$
\boxed{8}
$$
```

</details>

<details><summary><b>IQ4_XS</b> — 14.22 s, 1224 tokens, similarity 0.809</summary>

```text
To determine how many rupees Riya has left, let's analyze the situation step by step:

---

### Step 1: Cost of Pens
Riya buys **7 pens**, each costing **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### Step 2: Change Received
She pays with a **100 rupee note**, so the change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### Step 3: Spending on a Notebook
She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### Step 4: Remaining Money
Now, subtract the amount spent on the notebook from the change:

$$
\text{Remaining money} = 16 - 8 = 8 \text{ rupees}
$$

---

### Final Answer

$$
\boxed{8}
$$
```

</details>

<details><summary><b>Q3_K_M</b> — 10.96 s, 987 tokens, similarity 0.144</summary>

```text
Riya buys 7 pens at 12 rupees each. The total cost of the pens is calculated as follows:

$$
7 \times 12 = 84 \text{ rupees}
$$

She pays with a 100 rupee note, so the change she receives is:

$$
100 - 84 = 16 \text{ rupees}
$$

She then spends half of her change on a notebook. Half of 16 rupees is:

$$
\frac{16}{2} = 8 \text{ rupees}
$$

Therefore, the amount of money she has left after spending half of her change is:

$$
16 - 8 = 8 \text{ rupees}
$$

$$
\boxed{8}
$$
```

</details>

<details><summary><b>IQ3_M</b> — 14.7 s, 1309.5 tokens, similarity 0.918</summary>

```text
To determine how many rupees Riya has left after her purchases, let's break the problem into clear steps:

---

### Step 1: Cost of Pens
Riya buys **7 pens**, and each pen costs **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### Step 2: Change Received
She pays with a **100-rupee note**, so the change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### Step 3: Spending on a Notebook
She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### Step 4: Remaining Money
Now, subtract the amount spent on the notebook from the change she had:

$$
\text{Remaining money} = 16 - 8 = 8 \text{ rupees}
$$

---

### Final Answer

$$
\boxed{8}
$$
```

</details>

### sheep (Reasoning)

> A farmer has 17 sheep. All but 9 run away. How many sheep does the farmer have left? Answer with the number.

<details><summary><b>Q8_0</b> — 6.88 s, 349 tokens</summary>

```text
9
```

</details>

<details><summary><b>Q6_K</b> — 6.97 s, 436.5 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q5_K_M</b> — 5.46 s, 385.5 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q4_K_M</b> — 4.9 s, 392.5 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>IQ4_XS</b> — 3.86 s, 333 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>Q3_K_M</b> — 7.49 s, 679.5 tokens, similarity 1.0</summary>

```text
9
```

</details>

<details><summary><b>IQ3_M</b> — 6.19 s, 558.5 tokens, similarity 1.0</summary>

```text
9
```

</details>

### palindrome-code (Code)

> Write a Python function is_palindrome(s) that returns True if the string s is a palindrome, ignoring case, spaces and punctuation. Reply with only the code in one Python code block.

<details><summary><b>Q8_0</b> — 0.81 s, 39 tokens</summary>

```text
```python
import string

def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q6_K</b> — 0.66 s, 39 tokens, similarity 1.0</summary>

```text
```python
import string

def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q5_K_M</b> — 0.6 s, 39 tokens, similarity 1.0</summary>

```text
```python
import string

def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q4_K_M</b> — 0.55 s, 39 tokens, similarity 0.97</summary>

```text
```python
import string

def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>IQ4_XS</b> — 0.54 s, 43 tokens, similarity 0.847</summary>

```text
```python
import string

def is_palindrome(s):
    s = s.lower()
    s = ''.join(char for char in s if char.isalnum())
    return s == s[::-1]
```
```

</details>

<details><summary><b>Q3_K_M</b> — 0.48 s, 39 tokens, similarity 0.97</summary>

```text
```python
import string

def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>IQ3_M</b> — 0.46 s, 39 tokens, similarity 1.0</summary>

```text
```python
import string

def is_palindrome(s):
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]
```
```

</details>

### capital (Knowledge)

> What is the capital city of Australia? Answer in one word.

<details><summary><b>Q8_0</b> — 0.1 s, 3 tokens</summary>

```text
Canberra
```

</details>

<details><summary><b>Q6_K</b> — 0.09 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q5_K_M</b> — 0.08 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q4_K_M</b> — 0.08 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>IQ4_XS</b> — 0.08 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q3_K_M</b> — 0.06 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>IQ3_M</b> — 0.06 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

### three-bullets (Instruction following)

> Give exactly 3 bullet points on why model quantization is useful. Use '-' for each bullet and write nothing else.

<details><summary><b>Q8_0</b> — 1.0 s, 50 tokens</summary>

```text
- Reduces model size, making it easier to deploy on devices with limited storage.  
- Lowers computational requirements, leading to faster inference and lower power consumption.  
- Enables efficient execution on edge devices and mobile platforms with limited processing power.
```

</details>

<details><summary><b>Q6_K</b> — 0.82 s, 50 tokens, similarity 0.64</summary>

```text
- Reduces model size, making it easier to deploy on devices with limited storage.  
- Lowers computational requirements, enabling faster inference and lower power consumption.  
- Enhances model efficiency without significant loss in accuracy, improving real-time performance.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.67 s, 46 tokens, similarity 0.67</summary>

```text
- Reduces model size, making it easier to deploy on devices with limited storage.  
- Lowers computational requirements, improving inference speed and energy efficiency.  
- Enables deployment on edge devices and mobile platforms with constrained resources.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.59 s, 46 tokens, similarity 0.67</summary>

```text
- Reduces model size, making it easier to deploy on devices with limited storage.  
- Lowers computational requirements, improving inference speed and energy efficiency.  
- Enables deployment on edge devices and mobile platforms with constrained resources.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.56 s, 46 tokens, similarity 0.67</summary>

```text
- Reduces model size, making it easier to deploy on devices with limited storage.  
- Lowers computational requirements, improving inference speed and energy efficiency.  
- Enables deployment on edge devices and mobile platforms with constrained resources.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.56 s, 47 tokens, similarity 0.439</summary>

```text
- Reduces model size, making it easier to deploy on devices with limited memory.  
- Improves inference speed by enabling faster computations on hardware.  
- Lowers power consumption, which is beneficial for mobile and edge devices.
```

</details>

<details><summary><b>IQ3_M</b> — 0.63 s, 56.5 tokens, similarity 0.151</summary>

```text
- Model quantization reduces the memory footprint, allowing models to run on devices with limited memory.  
- It can significantly decrease inference latency, making models faster and more efficient.  
- Quantization often leads to lower power consumption, which is beneficial for mobile and edge devices.
```

</details>

### malayalam (Multilingual)

> ഇന്ത്യയുടെ തലസ്ഥാനം ഏതാണ്? ഒരു വാക്യത്തിൽ ഉത്തരം നൽകുക.

<details><summary><b>Q8_0</b> — 0.91 s, 46 tokens</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q6_K</b> — 0.75 s, 46 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.67 s, 46 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.62 s, 47 tokens, similarity 0.985</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂ ഡൽഹിയാണ്.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.58 s, 48 tokens, similarity 0.882</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂ ഡല്ലീയാണ്.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.55 s, 48 tokens, similarity 0.882</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂ ഡല്ലീയാണ്.
```

</details>

<details><summary><b>IQ3_M</b> — 0.54 s, 47 tokens, similarity 0.955</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂദെൽഹിയാണ്.
```

</details>

### hindi (Multilingual)

> भारत की राजधानी क्या है? एक वाक्य में उत्तर दें।

<details><summary><b>Q8_0</b> — 0.59 s, 29 tokens</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q6_K</b> — 0.47 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q5_K_M</b> — 0.45 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q4_K_M</b> — 0.39 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ4_XS</b> — 0.35 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q3_K_M</b> — 0.35 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ3_M</b> — 0.33 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

### summary (Summarization)

> Summarize in two sentences: Quantization stores the weights of a neural network with fewer bits, for example 4 bits instead of 16. This makes the model file several times smaller and lets it run on GPUs with less memory, and generation usually becomes faster because less data is read for every token

<details><summary><b>Q8_0</b> — 1.34 s, 68.5 tokens</summary>

```text
Quantization reduces the number of bits used to store neural network weights, making models smaller, more memory-efficient, and faster to run, especially on GPUs. While this comes with a slight accuracy loss that increases as bit count decreases, 8-bit models remain nearly identical to the original, whereas 3-bit models show more noticeable performance drops.
```

</details>

<details><summary><b>Q6_K</b> — 1.09 s, 67 tokens, similarity 0.443</summary>

```text
Quantization reduces the number of bits used to store neural network weights, making models smaller, more memory-efficient, and faster to run, though it slightly decreases accuracy. Lower bit versions, like 3-bit, experience more accuracy loss compared to higher bit versions such as 8-bit, which remain nearly identical to the original model.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.83 s, 58 tokens, similarity 0.346</summary>

```text
Quantization reduces the number of bits used to store neural network weights, making models smaller and faster by decreasing memory usage and data transfer. While this slightly reduces accuracy, the impact is minimal with 8-bit quantization, but becomes more noticeable with lower bit counts like 3 bits.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.82 s, 64 tokens, similarity 0.311</summary>

```text
Quantization reduces the number of bits used to store neural network weights, making models smaller and faster while requiring less memory, though it slightly decreases accuracy. Lower bit versions, like 3-bit, experience more accuracy loss compared to higher bit versions such as 8-bit, which remain nearly identical to the original model.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.69 s, 58 tokens, similarity 0.448</summary>

```text
Quantization reduces the number of bits used to store neural network weights, making models smaller and faster while slightly decreasing accuracy. Lower bit versions, like 3-bit, experience more accuracy loss compared to higher bit versions such as 8-bit, which remain nearly identical to the original model.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.74 s, 65 tokens, similarity 0.352</summary>

```text
Quantization reduces the bit width of neural network weights, significantly decreasing model size and improving inference speed on GPUs, though it comes with a slight accuracy loss. Lower bit versions, like 3-bit, experience more accuracy degradation compared to higher bit versions such as 8-bit, which remain nearly identical to the original model.
```

</details>

<details><summary><b>IQ3_M</b> — 0.69 s, 61 tokens, similarity 0.513</summary>

```text
Quantization reduces the number of bits used to store neural network weights, making models smaller, faster, and more memory-efficient, though it comes with a slight accuracy loss. While 8-bit models perform nearly as well as the original, lower bit versions like 3-bit experience more significant accuracy drops.
```

</details>

### needle (Long context)

> Somewhere in the text above there is a sentence about a vault access code. What is the access code? Reply with just the number.

<details><summary><b>Q8_0</b> — 1.18 s, 5 tokens</summary>

```text
7341
```

</details>

<details><summary><b>Q6_K</b> — 1.33 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q5_K_M</b> — 1.24 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q4_K_M</b> — 1.17 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>IQ4_XS</b> — 1.09 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q3_K_M</b> — 1.22 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>IQ3_M</b> — 1.08 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

### weather-tool (Tool calling)

> What's the weather in Paris right now?

<details><summary><b>Q8_0</b> — 0.64 s, 20 tokens</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>Q6_K</b> — 0.57 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>Q5_K_M</b> — 0.54 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>Q4_K_M</b> — 0.51 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>IQ4_XS</b> — 0.49 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>Q3_K_M</b> — 0.46 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>IQ3_M</b> — 0.46 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>
