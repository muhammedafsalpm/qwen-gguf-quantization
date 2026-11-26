# Quant comparison: Qwen3-8B

12 prompts × 7 quants, temperature 0, seed 42, context 16384, 2 timing run(s) per prompt, llama.cpp b12345. Similarity is measured against the Q8_0 answer (1.0 = identical text).

## Summary

| Quant | Correct | Avg total time (s) | Avg first-token / prefill (ms) | Avg generation (tok/s) | Avg similarity to Q8_0 | Load time (s) |
|---|---|---|---|---|---|---|
| Q8_0 | 10/11 | 4.47 | 66.51 | 82.81 | — | 8.6 |
| Q6_K | 10/11 | 3.48 | 73.91 | 98.99 | 0.854 | 6.5 |
| Q5_K_M | 10/11 | 3.77 | 71.41 | 107.97 | 0.822 | 6.6 |
| Q4_K_M | 10/11 | 2.41 | 66.68 | 120.17 | 0.79 | 6.6 |
| IQ4_XS | 11/11 | 2.48 | 57.86 | 130.46 | 0.851 | 4.5 |
| Q3_K_M | 10/11 | 4.29 | 65.46 | 134.99 | 0.798 | 4.5 |
| IQ3_M | 10/11 | 4.36 | 62.33 | 140.56 | 0.822 | 4.6 |

## Per prompt: correct and total time (s)

| Prompt | Category | Q8_0 | Q6_K | Q5_K_M | Q4_K_M | IQ4_XS | Q3_K_M | IQ3_M |
|---|---|---|---|---|---|---|---|---|
| bat-ball | Logic | ✅ 23.77 | ✅ 19.56 | ✅ 19.57 | ✅ 10.29 | ✅ 12.28 | ✅ 22.07 | ✅ 26.5 |
| multiply | Math | ✅ 0.14 | ✅ 0.13 | ✅ 0.16 | ✅ 0.09 | ✅ 0.11 | ✅ 0.16 | ✅ 0.17 |
| word-problem | Math | ✅ 18.7 | ✅ 11.6 | ✅ 15.24 | ✅ 11.08 | ✅ 10.4 | ✅ 12.47 | ✅ 16.75 |
| sheep | Reasoning | ✅ 6.5 | ✅ 6.73 | ✅ 6.84 | ✅ 4.3 | ✅ 4.12 | ✅ 13.7 | ✅ 5.83 |
| palindrome-code | Code | ✅ 0.71 | ✅ 0.6 | ✅ 0.54 | ✅ 0.42 | ✅ 0.38 | ✅ 0.4 | ✅ 0.51 |
| capital | Knowledge | ✅ 0.07 | ✅ 0.06 | ✅ 0.07 | ✅ 0.05 | ✅ 0.05 | ✅ 0.06 | ✅ 0.06 |
| three-bullets | Instruction following | ✅ 0.52 | ✅ 0.4 | ✅ 0.37 | ✅ 0.39 | ✅ 0.31 | ✅ 0.31 | ✅ 0.31 |
| malayalam | Multilingual | ❌ 0.61 | ❌ 0.51 | ❌ 0.45 | ❌ 0.43 | ✅ 0.37 | ❌ 0.37 | ❌ 0.37 |
| hindi | Multilingual | ✅ 0.38 | ✅ 0.32 | ✅ 0.28 | ✅ 0.27 | ✅ 0.24 | ✅ 0.25 | ✅ 0.23 |
| summary | Summarization | · 0.9 | · 0.75 | · 0.61 | · 0.56 | · 0.53 | · 0.47 | · 0.56 |
| needle | Long context | ✅ 0.67 | ✅ 0.73 | ✅ 0.7 | ✅ 0.65 | ✅ 0.58 | ✅ 0.65 | ✅ 0.62 |
| weather-tool | Tool calling | ✅ 0.69 | ✅ 0.41 | ✅ 0.46 | ✅ 0.39 | ✅ 0.33 | ✅ 0.54 | ✅ 0.38 |

✅ correct · ❌ wrong · · not graded (compare by reading)

## Answers side by side

### bat-ball (Logic)

> A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?

<details><summary><b>Q8_0</b> — 23.77 s, 2040 tokens</summary>

```text
To solve the problem, we begin by defining the variables:

Let the cost of the **ball** be $ x $ dollars.  
Then, the cost of the **bat** is $ x + 1.00 $ dollars, since the bat costs $1.00 more than the ball.

We are told that the **total cost** of the bat and the ball is $1.10. So we can write the equation:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

Now, subtract 1.00 from both sides:

$$
2x = 0.10
$$

Divide both sides by 2:

$$
x = 0.05
$$

---

### Interpretation:

This means the **ball costs $0.05**, or **5 cents**.  
Then the **bat costs** $ 0.05 + 1.00 = 1.05 $, or **$1.05**.

Adding them together:

$$
0.05 + 1.05 = 1.10
$$

This confirms the total is correct.

---

### Final Answer:

$$
\boxed{0.05}
$$
```

</details>

<details><summary><b>Q6_K</b> — 19.56 s, 1991.5 tokens, similarity 0.638</summary>

```text
To solve the problem, we begin by defining the variables:

- Let the cost of the **ball** be $ x $ dollars.
- Then, the cost of the **bat** is $ x + 1.00 $, since the bat costs $1.00 more than the ball.

We are told that the **total cost** of the bat and the ball is $1.10. So, we can write the equation:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

Now, subtract 1.00 from both sides:

$$
2x = 0.10
$$

Divide both sides by 2:

$$
x = 0.05
$$

---

### Final Answer:

The ball costs **$0.05**.

---

### Verification:

- Ball: $0.05
- Bat: $0.05 + $1.00 = $1.05
- Total: $0.05 + $1.05 = $1.10 ✅

This confirms the solution is correct. The key was recognizing that the bat is $1.00 more than the ball, not that the bat is $1.00 and the ball is $0.10. The difference is crucial to the correct interpretation.
```

</details>

<details><summary><b>Q5_K_M</b> — 19.57 s, 2187.5 tokens, similarity 0.513</summary>

```text
To solve the problem, we begin by defining the cost of the ball as a variable. Let:

- $ x $ = the cost of the ball (in dollars)
- Then, the cost of the bat is $ x + 1.00 $, since the bat costs $1.00 more than the ball.

We are told that the total cost of the bat and the ball is $1.10. Therefore, we can write the equation:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Now divide both sides by 2:

$$
x = 0.05
$$

---

### Final Answer:

The ball costs **$0.05**, or **5 cents**.

---

### Verification:

- Ball: $0.05
- Bat: $0.05 + $1.00 = $1.05
- Total: $0.05 + $1.05 = $1.10 ✅

This confirms the solution is correct. The key was recognizing that the bat is $1.00 more than the ball, not that the bat is $1.00 in total. This distinction is crucial to avoid the common mistake of assuming the ball costs $0.10.
```

</details>

<details><summary><b>Q4_K_M</b> — 10.29 s, 1270.5 tokens, similarity 0.123</summary>

```text
To solve the problem, we begin by defining the cost of the ball as a variable. Let:

- $ x $ = the cost of the ball in dollars.

Then, the bat costs $1.00 more than the ball, so the bat's cost is:

- $ x + 1.00 $

The total cost of the bat and the ball is given as $1.10. Therefore, we can write the equation:

$$
x + (x + 1.00) = 1.10
$$

Simplify the left-hand side:

$$
2x + 1.00 = 1.10
$$

Subtract 1.00 from both sides:

$$
2x = 0.10
$$

Now divide both sides by 2:

$$
x = 0.05
$$

So, the ball costs **$0.05**.

To verify:

- Ball: $0.05
- Bat: $0.05 + $1.00 = $1.05
- Total: $0.05 + $1.05 = $1.10

This confirms the solution is correct.

---

**Final Answer:**  
The ball costs \boxed{0.05} dollars.
```

</details>

<details><summary><b>IQ4_XS</b> — 12.28 s, 1640 tokens, similarity 0.462</summary>

```text
To solve the problem, we are given two key pieces of information:

1. The total cost of the bat and the ball is **$1.10**.
2. The **bat costs $1.00 more** than the ball.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.

Then, the cost of the **bat** is $ x + 1.00 $ dollars.

---

### Step 2: Set Up the Equation

The total cost of the bat and the ball is:

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
2x = 1.10 - 1.00 = 0.10
$$

Now divide both sides by 2:

$$
x = \frac{0.10}{2} = 0.05
$$

---

### Step 4: Interpret the Result

So, the **ball costs $0.05**, or **5 cents**.

To verify:

- Ball = $0.05
- Bat = $0.05 + $1.00 = $1.05
- Total = $0.05 + $1.05 = $1.10 ✅

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

<details><summary><b>Q3_K_M</b> — 22.07 s, 3041 tokens, similarity 0.262</summary>

```text
To solve the problem, we are given two pieces of information:

1. The total cost of a bat and a ball is **$1.10**.
2. The bat costs **$1.00 more** than the ball.

---

### Step 1: Define Variables

Let the cost of the ball be $ x $ dollars.  
Then, the cost of the bat is $ x + 1.00 $ dollars.

---

### Step 2: Set Up the Equation

The total cost of the bat and the ball is:

$$
x + (x + 1.00) = 1.10
$$

Simplify the equation:

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

So, the ball costs **$0.05**, and the bat costs:

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

<details><summary><b>IQ3_M</b> — 26.5 s, 3687.5 tokens, similarity 0.459</summary>

```text
To solve the problem, we are given two key pieces of information:

1. The **total cost** of the bat and the ball is **$1.10**.
2. The **bat costs $1.00 more** than the ball.

---

### Step 1: Define Variables

Let the cost of the **ball** be $ x $ dollars.  
Then, the cost of the **bat** is $ x + 1.00 $ dollars (since it's $1.00 more than the ball).

---

### Step 2: Set Up the Equation

The total cost of the bat and the ball is:

$$
x + (x + 1.00) = 1.10
$$

Simplify the equation:

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

So, the **ball costs $0.05**, and the **bat costs $1.05** (since it's $1.00 more than the ball). Adding them together:

$$
0.05 + 1.05 = 1.10
$$

This confirms the total is correct.

---

### Final Answer

$$
\boxed{0.05}
$$
```

</details>

### multiply (Math)

> What is 17 multiplied by 23? Reply with just the number.

<details><summary><b>Q8_0</b> — 0.14 s, 4 tokens</summary>

```text
391
```

</details>

<details><summary><b>Q6_K</b> — 0.13 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q5_K_M</b> — 0.16 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q4_K_M</b> — 0.09 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>IQ4_XS</b> — 0.11 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>Q3_K_M</b> — 0.16 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

<details><summary><b>IQ3_M</b> — 0.17 s, 4 tokens, similarity 1.0</summary>

```text
391
```

</details>

### word-problem (Math)

> A shop sells pens at 12 rupees each. Riya buys 7 pens and pays with a 100 rupee note. She then spends half of her change on a notebook. How many rupees does she have left?

<details><summary><b>Q8_0</b> — 18.7 s, 1577 tokens</summary>

```text
To determine how much money Riya has left after her purchases, we'll follow the sequence of transactions step by step.

---

### Step 1: Cost of the Pens

Riya buys **7 pens**, each costing **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### Step 2: Payment and Change

She pays with a **100 rupee note**. The change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### Step 3: Spending Half of the Change on a Notebook

She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### Step 4: Remaining Money

After spending 8 rupees on the notebook, the amount of money she has left is:

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

<details><summary><b>Q6_K</b> — 11.6 s, 1175.5 tokens, similarity 0.462</summary>

```text
To determine how much money Riya has left after her purchases, we follow these steps:

---

### Step 1: Calculate the total cost of the pens

Each pen costs **12 rupees**, and Riya buys **7 pens**.

$$
\text{Total cost of pens} = 12 \times 7 = 84 \text{ rupees}
$$

---

### Step 2: Determine the change from the 100 rupee note

Riya pays with a **100 rupee note**, so the change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### Step 3: Calculate the amount spent on the notebook

She spends **half** of her change on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### Step 4: Find the remaining amount of money

After spending 8 rupees on the notebook, the remaining amount is:

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

<details><summary><b>Q5_K_M</b> — 15.24 s, 1682.5 tokens, similarity 0.905</summary>

```text
To determine how much money Riya has left after her purchases, we follow a step-by-step breakdown of her transactions:

---

### **Step 1: Cost of Pens**
Riya buys **7 pens**, each costing **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### **Step 2: Payment and Change**
She pays with a **100 rupee note**. The change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### **Step 3: Spending Half of the Change**
She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### **Step 4: Remaining Money**
After spending 8 rupees on the notebook, the amount of money she has left is:

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

<details><summary><b>Q4_K_M</b> — 11.08 s, 1357 tokens, similarity 0.482</summary>

```text
To determine how much money Riya has left after her purchases, let's break the problem into clear steps:

---

### **Step 1: Calculate the cost of the pens**

Each pen costs **12 rupees**, and Riya buys **7 pens**.

$$
\text{Total cost of pens} = 12 \times 7 = 84 \text{ rupees}
$$

---

### **Step 2: Determine the change from the 100 rupee note**

Riya pays with a **100 rupee note**, so the change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### **Step 3: Calculate the amount spent on the notebook**

She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### **Step 4: Find the remaining money**

After spending 8 rupees on the notebook, the remaining amount from her change is:

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

<details><summary><b>IQ4_XS</b> — 10.4 s, 1375 tokens, similarity 0.8</summary>

```text
To determine how much money Riya has left after her purchases, we follow a step-by-step breakdown of the transactions:

---

### **Step 1: Calculate the cost of the pens**

Riya buys **7 pens**, each costing **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### **Step 2: Determine the change received**

She pays with a **100 rupee note**. The change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### **Step 3: Calculate the amount spent on the notebook**

She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### **Step 4: Find the remaining money**

After spending 8 rupees on the notebook, the remaining amount is:

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

<details><summary><b>Q3_K_M</b> — 12.47 s, 1735 tokens, similarity 0.596</summary>

```text
To determine how many rupees Riya has left after her purchases, we can break the problem into clear steps:

---

### **Step 1: Calculate the cost of the pens**

Riya buys **7 pens**, each costing **12 rupees**.

$$
\text{Total cost of pens} = 7 \times 12 = 84 \text{ rupees}
$$

---

### **Step 2: Determine the change from the 100 rupee note**

She pays with a **100 rupee note**, so the change she receives is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### **Step 3: Calculate the amount spent on the notebook**

She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{1}{2} \times 16 = 8 \text{ rupees}
$$

---

### **Step 4: Determine the remaining amount**

After spending 8 rupees on the notebook, the amount she has left is:

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

<details><summary><b>IQ3_M</b> — 16.75 s, 2363 tokens, similarity 0.594</summary>

```text
To determine how much money Riya has left after her purchases, we'll break the problem into clear, logical steps.

---

### Step 1: Calculate the total cost of the pens

Riya buys **7 pens**, and each pen costs **12 rupees**.

$$
\text{Total cost} = 7 \times 12 = 84 \text{ rupees}
$$

---

### Step 2: Determine the change she receives

She pays with a **100 rupee note**, so the change she gets back is:

$$
\text{Change} = 100 - 84 = 16 \text{ rupees}
$$

---

### Step 3: Calculate how much she spends on the notebook

She spends **half of her change** on a notebook:

$$
\text{Amount spent on notebook} = \frac{16}{2} = 8 \text{ rupees}
$$

---

### Step 4: Determine how much money she has left

After spending 8 rupees on the notebook, the remaining amount is:

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

<details><summary><b>Q8_0</b> — 6.5 s, 535.5 tokens</summary>

```text
The farmer initially has 17 sheep. The phrase "all but 9 run away" means that 9 sheep remain. Therefore, the number of sheep left is **9**.

**Answer:** 9
```

</details>

<details><summary><b>Q6_K</b> — 6.73 s, 683.5 tokens, similarity 1.0</summary>

```text
The farmer initially has 17 sheep. The phrase "all but 9 run away" means that 9 sheep remain. Therefore, the number of sheep left is **9**.

**Answer:** 9
```

</details>

<details><summary><b>Q5_K_M</b> — 6.84 s, 760.5 tokens, similarity 0.743</summary>

```text
The farmer initially has 17 sheep. The phrase "all but 9 run away" means that 9 sheep remain. This is because "all but" indicates that everything except for the specified number (9) is gone. Therefore, the number of sheep left is 9.

**Answer:** 9
```

</details>

<details><summary><b>Q4_K_M</b> — 4.3 s, 536 tokens, similarity 0.897</summary>

```text
The farmer initially has 17 sheep. The phrase "all but 9 run away" means that 9 sheep did not run away. Therefore, the number of sheep remaining is 9.

**Answer:** 9
```

</details>

<details><summary><b>IQ4_XS</b> — 4.12 s, 576 tokens, similarity 1.0</summary>

```text
The farmer initially has 17 sheep. The phrase "all but 9 run away" means that 9 sheep remain. Therefore, the number of sheep left is **9**.

**Answer:** 9
```

</details>

<details><summary><b>Q3_K_M</b> — 13.7 s, 1913.5 tokens, similarity 0.899</summary>

```text
The farmer initially has 17 sheep. The phrase "all but 9 run away" means that 9 sheep did **not** run away. Therefore, the number of sheep remaining is **9**.

**Answer:** 9
```

</details>

<details><summary><b>IQ3_M</b> — 5.83 s, 822.5 tokens, similarity 0.797</summary>

```text
The farmer starts with 17 sheep. The phrase "all but 9 run away" means that 9 sheep are left, and the rest (17 - 9 = 8) ran away. Therefore, the number of sheep remaining is **9**.

**Answer:** 9
```

</details>

### palindrome-code (Code)

> Write a Python function is_palindrome(s) that returns True if the string s is a palindrome, ignoring case, spaces and punctuation. Reply with only the code in one Python code block.

<details><summary><b>Q8_0</b> — 0.71 s, 54 tokens</summary>

```text
```python
import re

def is_palindrome(s):
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q6_K</b> — 0.6 s, 54 tokens, similarity 1.0</summary>

```text
```python
import re

def is_palindrome(s):
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q5_K_M</b> — 0.54 s, 54 tokens, similarity 1.0</summary>

```text
```python
import re

def is_palindrome(s):
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>Q4_K_M</b> — 0.42 s, 44 tokens, similarity 0.738</summary>

```text
```python
import re

def is_palindrome(s):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s)
    return cleaned.lower() == cleaned.lower()[::-1]
```
```

</details>

<details><summary><b>IQ4_XS</b> — 0.38 s, 44 tokens, similarity 0.738</summary>

```text
```python
import re

def is_palindrome(s):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s)
    return cleaned.lower() == cleaned[::-1].lower()
```
```

</details>

<details><summary><b>Q3_K_M</b> — 0.4 s, 42 tokens, similarity 0.804</summary>

```text
```python
import re

def is_palindrome(s):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]
```
```

</details>

<details><summary><b>IQ3_M</b> — 0.51 s, 67 tokens, similarity 0.874</summary>

```text
```python
import re

def is_palindrome(s):
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    # Check if the cleaned string is equal to its reverse
    return cleaned == cleaned[::-1]
```
```

</details>

### capital (Knowledge)

> What is the capital city of Australia? Answer in one word.

<details><summary><b>Q8_0</b> — 0.07 s, 3 tokens</summary>

```text
Canberra
```

</details>

<details><summary><b>Q6_K</b> — 0.06 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q5_K_M</b> — 0.07 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>Q4_K_M</b> — 0.05 s, 3 tokens, similarity 1.0</summary>

```text
Canberra
```

</details>

<details><summary><b>IQ4_XS</b> — 0.05 s, 3 tokens, similarity 1.0</summary>

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

<details><summary><b>Q8_0</b> — 0.52 s, 40 tokens</summary>

```text
- Reduces model size, enabling efficient deployment on resource-constrained devices  
- Lowers computational requirements, improving inference speed and energy efficiency  
- Facilitates model compression without significant loss of accuracy
```

</details>

<details><summary><b>Q6_K</b> — 0.4 s, 38 tokens, similarity 0.174</summary>

```text
- Reduces model size, enabling deployment on devices with limited memory  
- Lowers computational requirements, improving inference speed  
- Decreases energy consumption, enhancing efficiency in resource-constrained environments
```

</details>

<details><summary><b>Q5_K_M</b> — 0.37 s, 38 tokens, similarity 0.174</summary>

```text
- Reduces model size, enabling deployment on devices with limited memory  
- Lowers computational requirements, improving inference speed  
- Decreases energy consumption, enhancing efficiency in resource-constrained environments
```

</details>

<details><summary><b>Q4_K_M</b> — 0.39 s, 46 tokens, similarity 0.556</summary>

```text
- Reduces model size, enabling deployment on devices with limited memory and storage  
- Lowers computational requirements, improving inference speed and energy efficiency  
- Facilitates efficient model updates and real-time processing in resource-constrained environments
```

</details>

<details><summary><b>IQ4_XS</b> — 0.31 s, 36 tokens, similarity 0.534</summary>

```text
- Reduces model size for efficient deployment on resource-constrained devices  
- Lowers computational requirements and energy consumption during inference  
- Enables faster model execution without significant loss in accuracy
```

</details>

<details><summary><b>Q3_K_M</b> — 0.31 s, 38.5 tokens, similarity 0.338</summary>

```text
- Reduces the memory footprint of the model, enabling deployment on resource-constrained devices  
- Decreases computational requirements, leading to faster inference times  
- Lowers energy consumption and operational costs for model execution
```

</details>

<details><summary><b>IQ3_M</b> — 0.31 s, 42 tokens, similarity 0.449</summary>

```text
- Reduces the memory footprint of models, allowing deployment on devices with limited resources  
- Lowers computational requirements, improving inference speed and energy efficiency  
- Enables efficient model deployment on edge devices and mobile platforms
```

</details>

### malayalam (Multilingual)

> ഇന്ത്യയുടെ തലസ്ഥാനം ഏതാണ്? ഒരു വാക്യത്തിൽ ഉത്തരം നൽകുക.

<details><summary><b>Q8_0</b> — 0.61 s, 48 tokens</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡെഹലിയാണ്.
```

</details>

<details><summary><b>Q6_K</b> — 0.51 s, 48 tokens, similarity 0.971</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡെൽഹിയാണ്.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.45 s, 48 tokens, similarity 0.971</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡെൽഹിയാണ്.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.43 s, 49 tokens, similarity 0.957</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡെല്ഹിയാണ്.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.37 s, 46 tokens, similarity 0.955</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡൽഹിയാണ്.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.37 s, 48 tokens, similarity 1.0</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡെഹലിയാണ്.
```

</details>

<details><summary><b>IQ3_M</b> — 0.37 s, 49 tokens, similarity 0.957</summary>

```text
ഇന്ത്യയുടെ തലസ്ഥാനം ന്യൂഡെല്ഹിയാണ്.
```

</details>

### hindi (Multilingual)

> भारत की राजधानी क्या है? एक वाक्य में उत्तर दें।

<details><summary><b>Q8_0</b> — 0.38 s, 29 tokens</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q6_K</b> — 0.32 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q5_K_M</b> — 0.28 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q4_K_M</b> — 0.27 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ4_XS</b> — 0.24 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>Q3_K_M</b> — 0.25 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

<details><summary><b>IQ3_M</b> — 0.23 s, 29 tokens, similarity 1.0</summary>

```text
भारत की राजधानी नई दिल्ली है।
```

</details>

### summary (Summarization)

> Summarize in two sentences: Quantization stores the weights of a neural network with fewer bits, for example 4 bits instead of 16. This makes the model file several times smaller and lets it run on GPUs with less memory, and generation usually becomes faster because less data is read for every token

<details><summary><b>Q8_0</b> — 0.9 s, 73 tokens</summary>

```text
Quantization reduces the number of bits used to store neural network weights, such as from 16 to 4 bits, making the model smaller and faster to run with less memory. While this leads to a slight loss in accuracy, 8-bit versions retain most of the original performance, whereas lower-bit versions like 3-bit experience more significant accuracy drops.
```

</details>

<details><summary><b>Q6_K</b> — 0.75 s, 73.5 tokens, similarity 1.0</summary>

```text
Quantization reduces the number of bits used to store neural network weights, such as from 16 to 4 bits, making the model smaller and faster to run with less memory. While this leads to a slight loss in accuracy, 8-bit versions retain most of the original performance, whereas lower-bit versions like 3-bit experience more significant accuracy drops.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.61 s, 66 tokens, similarity 0.563</summary>

```text
Quantization reduces the number of bits used to store neural network weights, such as from 16 to 4 bits, making the model smaller and faster to run while using less memory. This technique slightly decreases accuracy, with greater loss observed as the bit depth decreases, though 8-bit versions maintain near-original performance.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.56 s, 67 tokens, similarity 0.731</summary>

```text
Quantization reduces the number of bits used to store neural network weights, such as from 16 to 4 bits, making the model smaller and faster to run with less memory. While this leads to a slight loss in accuracy, especially with fewer bits, 8-bit versions maintain nearly the same performance as the original model.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.53 s, 70.5 tokens, similarity 0.726</summary>

```text
Quantization reduces the number of bits used to store a neural network's weights, such as from 16 to 4 bits, making the model smaller and faster to run with less memory. While this leads to a slight loss in accuracy, especially with fewer bits, 8-bit versions maintain nearly the same performance as the original model.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.47 s, 64.5 tokens, similarity 0.678</summary>

```text
Quantization reduces the number of bits used to store neural network weights, such as from 16 to 4 bits, making the model smaller and faster to run with less memory. This slight loss in accuracy increases as the bit depth decreases, with 8-bit versions maintaining near-original performance while 3-bit versions show more significant degradation.
```

</details>

<details><summary><b>IQ3_M</b> — 0.56 s, 80 tokens, similarity 0.731</summary>

```text
Quantization reduces the number of bits used to store a neural network's weights, such as from 16 bits to 4 bits, making the model smaller and faster to run while using less memory. This slight decrease in accuracy becomes more noticeable as the bit depth decreases, with 8-bit models retaining most of the original performance, while lower-bit versions like 3-bit experience more loss.
```

</details>

### needle (Long context)

> Somewhere in the text above there is a sentence about a vault access code. What is the access code? Reply with just the number.

<details><summary><b>Q8_0</b> — 0.67 s, 5 tokens</summary>

```text
7341
```

</details>

<details><summary><b>Q6_K</b> — 0.73 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q5_K_M</b> — 0.7 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q4_K_M</b> — 0.65 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>IQ4_XS</b> — 0.58 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>Q3_K_M</b> — 0.65 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

<details><summary><b>IQ3_M</b> — 0.62 s, 5 tokens, similarity 1.0</summary>

```text
7341
```

</details>

### weather-tool (Tool calling)

> What's the weather in Paris right now?

<details><summary><b>Q8_0</b> — 0.69 s, 20 tokens</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>Q6_K</b> — 0.41 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>Q5_K_M</b> — 0.46 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>Q4_K_M</b> — 0.39 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>IQ4_XS</b> — 0.33 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>Q3_K_M</b> — 0.54 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>

<details><summary><b>IQ3_M</b> — 0.38 s, 20 tokens, similarity 1.0</summary>

```text
[{"name": "get_weather", "arguments": "{\"city\": \"Paris\"}"}]
```

</details>
