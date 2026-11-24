# Quant comparison: Qwen3.8-27B

14 prompts × 7 quants, temperature 0, seed 42, context 16384, 1 timing run(s) per prompt, llama.cpp b12345. Similarity is measured against the Q8_0 answer (1.0 = identical text).

## Summary

| Quant | Correct | Avg total time (s) | Avg first-token / prefill (ms) | Avg generation (tok/s) | Avg similarity to Q8_0 | Load time (s) |
|---|---|---|---|---|---|---|
| Q8_0 | 12/14 | 10.86 | 291.25 | 27.68 | — | 26.8 |
| Q6_K | 12/14 | 8.61 | 250.28 | 35.1 | 0.838 | 18.7 |
| Q5_K_M | 12/14 | 8.09 | 242.93 | 39.52 | 0.832 | 16.6 |
| Q4_K_M | 13/14 | 7.68 | 284.6 | 43.09 | 0.756 | 16.7 |
| IQ4_XS | 13/14 | 6.94 | 236.56 | 47.24 | 0.73 | 14.6 |
| Q3_K_M | 12/14 | 5.07 | 233.35 | 51.36 | 0.625 | 12.6 |
| IQ3_M | 12/14 | 8.86 | 234.72 | 50.9 | 0.636 | 14.6 |

## Per prompt: correct and total time (s)

| Prompt | Category | Q8_0 | Q6_K | Q5_K_M | Q4_K_M | IQ4_XS | Q3_K_M | IQ3_M |
|---|---|---|---|---|---|---|---|---|
| en-coconuts | English | ✅ 8.95 | ✅ 6.72 | ✅ 5.97 | ✅ 5.83 | ✅ 5.33 | ✅ 5.64 | ✅ 3.95 |
| en-heights | English | ✅ 2.4 | ✅ 1.83 | ✅ 1.6 | ✅ 1.67 | ✅ 1.42 | ✅ 1.84 | ✅ 1.28 |
| en-weekday | English | ✅ 8.3 | ✅ 5.6 | ✅ 4.83 | ✅ 7.82 | ✅ 5.1 | ✅ 4.37 | ✅ 9.38 |
| en-discount | English | ✅ 10.59 | ✅ 8.66 | ✅ 7.42 | ✅ 7.22 | ✅ 6.18 | ✅ 5.04 | ✅ 5.31 |
| ml-coconuts | Malayalam | ✅ 20.91 | ✅ 15.8 | ✅ 18.88 | ✅ 13.56 | ✅ 11.54 | ✅ 9.39 | ✅ 14.13 |
| ml-heights | Malayalam | ✅ 4.92 | ✅ 4.54 | ✅ 4.32 | ✅ 7.04 | ✅ 3.07 | ✅ 3.63 | ✅ 6.53 |
| ml-weekday | Malayalam | ✅ 31.64 | ✅ 24.42 | ✅ 23.99 | ✅ 19.0 | ✅ 27.39 | ✅ 13.05 | ✅ 46.62 |
| ml-discount | Malayalam | ❌ 14.95 | ❌ 11.6 | ❌ 10.59 | ❌ 9.5 | ❌ 8.82 | ❌ 5.79 | ❌ 11.48 |
| ml-translate | Malayalam | ✅ 0.83 | ✅ 0.71 | ✅ 0.64 | ✅ 0.6 | ✅ 0.6 | ✅ 0.59 | ✅ 0.58 |
| hi-coconuts | Hindi | ✅ 16.36 | ✅ 13.16 | ✅ 10.54 | ✅ 10.44 | ✅ 9.32 | ✅ 7.36 | ✅ 7.54 |
| hi-heights | Hindi | ✅ 3.77 | ✅ 4.11 | ✅ 3.69 | ✅ 2.55 | ✅ 4.07 | ✅ 3.38 | ✅ 3.66 |
| hi-weekday | Hindi | ✅ 15.78 | ✅ 13.54 | ✅ 11.69 | ✅ 13.26 | ✅ 8.28 | ✅ 5.5 | ✅ 8.03 |
| hi-discount | Hindi | ❌ 11.74 | ❌ 9.21 | ❌ 8.42 | ✅ 8.43 | ✅ 5.48 | ❌ 4.82 | ❌ 4.99 |
| hi-translate | Hindi | ✅ 0.84 | ✅ 0.66 | ✅ 0.64 | ✅ 0.6 | ✅ 0.57 | ✅ 0.55 | ✅ 0.55 |

✅ correct · ❌ wrong · · not graded (compare by reading)

## Answers side by side

### en-coconuts (English)

> A farmer has 3 fields. Each field has 24 coconut trees. Each tree gives 15 coconuts per month. He sells each coconut for ₹12. How much does he earn in one month? Explain step by step.

<details><summary><b>Q8_0</b> — 8.95 s, 223 tokens</summary>

```text
Step 1: Find the total number of coconut trees.  
3 fields × 24 trees per field = 72 trees

Step 2: Find the total number of coconuts produced in one month.  
72 trees × 15 coconuts per tree = 1080 coconuts

Step 3: Find the total earning from selling the coconuts.  
1080 coconuts × ₹12 per coconut = ₹12,960

So, the farmer earns **₹12,960 in one month**.
```

</details>

<details><summary><b>Q6_K</b> — 6.72 s, 217 tokens, similarity 0.962</summary>

```text
Step 1: Find the total number of coconut trees.  
3 fields × 24 trees per field = 72 trees

Step 2: Find the total number of coconuts produced in one month.  
72 trees × 15 coconuts per tree = 1080 coconuts

Step 3: Find the total earning.  
1080 coconuts × ₹12 per coconut = ₹12,960

So, the farmer earns **₹12,960 in one month**.
```

</details>

<details><summary><b>Q5_K_M</b> — 5.97 s, 217 tokens, similarity 0.962</summary>

```text
Step 1: Find the total number of coconut trees.  
3 fields × 24 trees per field = 72 trees

Step 2: Find the total number of coconuts produced in one month.  
72 trees × 15 coconuts per tree = 1080 coconuts

Step 3: Find the total earning.  
1080 coconuts × ₹12 per coconut = ₹12,960

So, the farmer earns **₹12,960 in one month**.
```

</details>

<details><summary><b>Q4_K_M</b> — 5.83 s, 218 tokens, similarity 0.964</summary>

```text
Step 1: Find the total number of coconut trees.  
3 fields × 24 trees per field = 72 trees

Step 2: Find the total number of coconuts produced in one month.  
72 trees × 15 coconuts per tree = 1080 coconuts

Step 3: Find the total earnings.  
1080 coconuts × ₹12 per coconut = ₹12,960

So, the farmer earns **₹12,960 in one month**.
```

</details>

<details><summary><b>IQ4_XS</b> — 5.33 s, 218 tokens, similarity 0.964</summary>

```text
Step 1: Find the total number of coconut trees.  
3 fields × 24 trees per field = 72 trees

Step 2: Find the total number of coconuts produced in one month.  
72 trees × 15 coconuts per tree = 1080 coconuts

Step 3: Find the total earnings.  
1080 coconuts × ₹12 per coconut = ₹12,960

So, the farmer earns **₹12,960 in one month**.
```

</details>

<details><summary><b>Q3_K_M</b> — 5.64 s, 272 tokens, similarity 0.46</summary>

```text
Step 1: Find the total number of coconut trees.

- Number of fields = 3  
- Trees in each field = 24  

Total trees = 3 × 24 = 72 trees

Step 2: Find the total number of coconuts produced in one month.

- Each tree gives 15 coconuts per month  

Total coconuts = 72 × 15 = 1080 coconuts

Step 3: Find the total earning.

- Each coconut is sold for ₹12  

Total earning = 1080 × 12 = ₹12,960

So, the farmer earns **₹12,960 in one month**.
```

</details>

<details><summary><b>IQ3_M</b> — 3.95 s, 189 tokens, similarity 0.962</summary>

```text
Step 1: Find the total number of coconut trees.  
3 fields × 24 trees per field = 72 trees

Step 2: Find the total number of coconuts produced in one month.  
72 trees × 15 coconuts per tree = 1080 coconuts

Step 3: Find the total earning.  
1080 coconuts × ₹12 per coconut = ₹12,960

So, the farmer earns **₹12,960 in one month**.
```

</details>

### en-heights (English)

> Ravi is taller than Anu. Anu is taller than Meera. Meera is taller than Joseph. Who is the shortest? Who is the tallest?

<details><summary><b>Q8_0</b> — 2.4 s, 51 tokens</summary>

```text
The shortest is **Joseph**.  
The tallest is **Ravi**.
```

</details>

<details><summary><b>Q6_K</b> — 1.83 s, 51 tokens, similarity 1.0</summary>

```text
The shortest is **Joseph**.  
The tallest is **Ravi**.
```

</details>

<details><summary><b>Q5_K_M</b> — 1.6 s, 51 tokens, similarity 1.0</summary>

```text
The shortest is **Joseph**.  
The tallest is **Ravi**.
```

</details>

<details><summary><b>Q4_K_M</b> — 1.67 s, 51 tokens, similarity 1.0</summary>

```text
The shortest is **Joseph**.  
The tallest is **Ravi**.
```

</details>

<details><summary><b>IQ4_XS</b> — 1.42 s, 51 tokens, similarity 1.0</summary>

```text
The shortest is **Joseph**.  
The tallest is **Ravi**.
```

</details>

<details><summary><b>Q3_K_M</b> — 1.84 s, 79 tokens, similarity 0.5</summary>

```text
The tallest is **Ravi**.  
The shortest is **Joseph**.
```

</details>

<details><summary><b>IQ3_M</b> — 1.28 s, 51 tokens, similarity 0.52</summary>

```text
Joseph is the shortest.  
Ravi is the tallest.
```

</details>

### en-weekday (English)

> If today is Wednesday, what day of the week will it be 100 days from today? Explain.

<details><summary><b>Q8_0</b> — 8.3 s, 219 tokens</summary>

```text
It will be **Friday**.

There are 7 days in a week, so we only need to find the remainder when 100 is divided by 7:

\[
100 \div 7 = 14 \text{ remainder } 2
\]

So 100 days from today is the same as **2 days after Wednesday**:

- 1 day after Wednesday = Thursday  
- 2 days after Wednesday = **Friday**
```

</details>

<details><summary><b>Q6_K</b> — 5.6 s, 182 tokens, similarity 0.519</summary>

```text
It will be **Friday**.

There are 7 days in a week, and:

\[
100 \div 7 = 14 \text{ remainder } 2
\]

So 100 days is the same as 14 full weeks plus 2 extra days. Starting from Wednesday, 2 days later is **Friday**.
```

</details>

<details><summary><b>Q5_K_M</b> — 4.83 s, 182 tokens, similarity 0.519</summary>

```text
It will be **Friday**.

There are 7 days in a week, and:

\[
100 \div 7 = 14 \text{ remainder } 2
\]

So 100 days is the same as 14 full weeks plus 2 extra days. Starting from Wednesday, 2 days later is **Friday**.
```

</details>

<details><summary><b>Q4_K_M</b> — 7.82 s, 312 tokens, similarity 0.919</summary>

```text
It will be **Friday**.

There are 7 days in a week, so we only need to find the remainder when 100 is divided by 7:

\[
100 \div 7 = 14 \text{ remainder } 2
\]

So 100 days from today is the same as **2 days after Wednesday**:

- Wednesday + 1 day = Thursday  
- Wednesday + 2 days = **Friday**
```

</details>

<details><summary><b>IQ4_XS</b> — 5.1 s, 231 tokens, similarity 0.706</summary>

```text
It will be **Friday**.

There are 7 days in a week, so we only need to find the remainder when 100 is divided by 7:

\[
100 \div 7 = 14 \text{ remainder } 2
\]

So 100 days is the same as 2 days forward in the week. Starting from Wednesday:

- 1 day later: Thursday  
- 2 days later: Friday  

Therefore, 100 days from today will be **Friday**.
```

</details>

<details><summary><b>Q3_K_M</b> — 4.37 s, 211 tokens, similarity 0.532</summary>

```text
It will be **Friday**.

There are 7 days in a week, and:

\[
100 \div 7 = 14 \text{ remainder } 2
\]

So 100 days is 14 full weeks plus 2 extra days. Starting from Wednesday, 2 days later is **Friday**.
```

</details>

<details><summary><b>IQ3_M</b> — 9.38 s, 470 tokens, similarity 0.577</summary>

```text
It will be **Friday**.

Explanation: The days of the week repeat every **7 days**.

\[
100 \div 7 = 14 \text{ remainder } 2
\]

So 100 days from now is the same as **2 days from today**.

If today is **Wednesday**:
- 1 day from today = Thursday
- 2 days from today = **Friday**

Therefore, 100 days from today will be **Friday**.
```

</details>

### en-discount (English)

> A shirt costs ₹800. The shop gives a 25% discount, then adds 5% tax on the discounted price. What is the final price? Explain.

<details><summary><b>Q8_0</b> — 10.59 s, 285 tokens</summary>

```text
The final price is **₹630**.

**Explanation:**

1. **Original price:** ₹800  
2. **25% discount:**  
   \[
   25\% \text{ of } 800 = \frac{25}{100} \times 800 = 200
   \]  
   Discounted price:  
   \[
   800 - 200 = 600
   \]

3. **5% tax on discounted price:**  
   \[
   5\% \text{ of } 600 = \frac{5}{100} \times 600 = 30
   \]

4. **Final price:**  
   \[
   600 + 30 = 630
   \]

So, the customer pays **₹630**.
```

</details>

<details><summary><b>Q6_K</b> — 8.66 s, 285 tokens, similarity 1.0</summary>

```text
The final price is **₹630**.

**Explanation:**

1. **Original price:** ₹800  
2. **25% discount:**  
   \[
   25\% \text{ of } 800 = \frac{25}{100} \times 800 = 200
   \]  
   Discounted price:  
   \[
   800 - 200 = 600
   \]

3. **5% tax on discounted price:**  
   \[
   5\% \text{ of } 600 = \frac{5}{100} \times 600 = 30
   \]

4. **Final price:**  
   \[
   600 + 30 = 630
   \]

So, the customer pays **₹630**.
```

</details>

<details><summary><b>Q5_K_M</b> — 7.42 s, 285 tokens, similarity 1.0</summary>

```text
The final price is **₹630**.

**Explanation:**

1. **Original price:** ₹800  
2. **25% discount:**  
   \[
   25\% \text{ of } 800 = \frac{25}{100} \times 800 = 200
   \]  
   Discounted price:  
   \[
   800 - 200 = 600
   \]

3. **5% tax on discounted price:**  
   \[
   5\% \text{ of } 600 = \frac{5}{100} \times 600 = 30
   \]

4. **Final price:**  
   \[
   600 + 30 = 630
   \]

So, the customer pays **₹630**.
```

</details>

<details><summary><b>Q4_K_M</b> — 7.22 s, 284 tokens, similarity 0.995</summary>

```text
The final price is **₹630**.

Explanation:

1. **Original price:** ₹800  
2. **25% discount:**  
   \[
   25\% \text{ of } 800 = \frac{25}{100} \times 800 = 200
   \]  
   Discounted price:  
   \[
   800 - 200 = 600
   \]

3. **5% tax on discounted price:**  
   \[
   5\% \text{ of } 600 = \frac{5}{100} \times 600 = 30
   \]

4. **Final price:**  
   \[
   600 + 30 = 630
   \]

So, the customer pays **₹630**.
```

</details>

<details><summary><b>IQ4_XS</b> — 6.18 s, 280 tokens, similarity 1.0</summary>

```text
The final price is **₹630**.

**Explanation:**

1. **Original price:** ₹800  
2. **25% discount:**  
   \[
   25\% \text{ of } 800 = \frac{25}{100} \times 800 = 200
   \]  
   Discounted price:  
   \[
   800 - 200 = 600
   \]

3. **5% tax on discounted price:**  
   \[
   5\% \text{ of } 600 = \frac{5}{100} \times 600 = 30
   \]

4. **Final price:**  
   \[
   600 + 30 = 630
   \]

So, the customer pays **₹630**.
```

</details>

<details><summary><b>Q3_K_M</b> — 5.04 s, 247 tokens, similarity 0.618</summary>

```text
The final price is **₹630**.

Explanation:

1. **Original price:** ₹800  
2. **25% discount:**  
   \[
   800 \times 0.25 = 200
   \]  
   Discounted price:  
   \[
   800 - 200 = 600
   \]

3. **5% tax on discounted price:**  
   \[
   600 \times 0.05 = 30
   \]

4. **Final price:**  
   \[
   600 + 30 = 630
   \]

So, the final price is **₹630**.
```

</details>

<details><summary><b>IQ3_M</b> — 5.31 s, 257 tokens, similarity 0.431</summary>

```text
The final price is **₹630**.

**Explanation:**

1. **Original price:** ₹800  
2. **25% discount:**  
   \[
   25\% \text{ of } 800 = 0.25 \times 800 = 200
   \]  
   Discounted price:  
   \[
   800 - 200 = 600
   \]

3. **5% tax on discounted price:**  
   \[
   5\% \text{ of } 600 = 0.05 \times 600 = 30
   \]  
   Final price:  
   \[
   600 + 30 = 630
   \]

So, the customer pays **₹630**.
```

</details>

### ml-coconuts (Malayalam)

> ഒരു കർഷകന് 3 പറമ്പുകളുണ്ട്. ഓരോ പറമ്പിലും 24 തെങ്ങുകൾ ഉണ്ട്. ഓരോ തെങ്ങിൽ നിന്നും മാസം 15 തേങ്ങ കിട്ടും. ഒരു തേങ്ങ ₹12-ന് വിൽക്കുന്നു. ഒരു മാസം അദ്ദേഹത്തിന് എത്ര രൂപ ലഭിക്കും? മലയാളത്തിൽ ഘട്ടം ഘട്ടമായി വിശദീകരിക്കുക.

<details><summary><b>Q8_0</b> — 20.91 s, 582 tokens</summary>

```text
**ഘട്ടം 1: ആകെ തെങ്ങുകളുടെ എണ്ണം കണ്ടെത്തുക**

പറമ്പുകളുടെ എണ്ണം = 3  
ഓരോ പറമ്പിലുമുള്ള തെങ്ങുകൾ = 24  

ആകെ തെങ്ങുകൾ = 3 × 24 = **72 തെങ്ങുകൾ**

---

**ഘട്ടം 2: ഒരു മാസത്തിൽ കിട്ടുന്ന ആകെ തേങ്ങകളുടെ എണ്ണം കണ്ടെത്തുക**

ഓരോ തെങ്ങിൽ നിന്ന് മാസം കിട്ടുന്ന തേങ്ങ = 15  

ആകെ തേങ്ങ = 72 × 15 = **1080 തേങ്ങ**

---

**ഘട്ടം 3: ആകെ വരുമാനം കണ്ടെത്തുക**

ഒരു തേങ്ങയുടെ വില = ₹12  

ആകെ വരുമാനം = 1080 × 12 = **₹12,960**

---

**ഉത്തരം:**  
ഒരു മാസം കർഷകന് **₹12,960** ലഭിക്കും.
```

</details>

<details><summary><b>Q6_K</b> — 15.8 s, 542 tokens, similarity 0.42</summary>

```text
ഘട്ടം 1: മൊത്തം തെങ്ങുകളുടെ എണ്ണം കണ്ടെത്തുക  
3 പറമ്പുകളുണ്ട്. ഓരോ പറമ്പിലും 24 തെങ്ങുകൾ ഉണ്ട്.  
അതുകൊണ്ട്,  
മൊത്തം തെങ്ങുകൾ = 3 × 24 = 72 തെങ്ങുകൾ

ഘട്ടം 2: ഒരു മാസം കിട്ടുന്ന മൊത്തം തേങ്ങകളുടെ എണ്ണം കണ്ടെത്തുക  
ഓരോ തെങ്ങിൽ നിന്ന് മാസം 15 തേങ്ങ കിട്ടും.  
അതുകൊണ്ട്,  
മൊത്തം തേങ്ങകൾ = 72 × 15 = 1080 തേങ്ങകൾ

ഘട്ടം 3: മൊത്തം വിൽപ്പന വില കണ്ടെത്തുക  
ഒരു തേങ്ങ ₹12-ന് വിൽക്കുന്നു.  
അതുകൊണ്ട്,  
മൊത്തം വരുമാനം = 1080 × 12 = ₹12,960

ഉത്തരം: ഒരു മാസം അദ്ദേഹത്തിന് **₹12,960** ലഭിക്കും.
```

</details>

<details><summary><b>Q5_K_M</b> — 18.88 s, 732 tokens, similarity 0.406</summary>

```text
തന്നിരിക്കുന്ന വിവരങ്ങൾ:

- പറമ്പുകളുടെ എണ്ണം = 3  
- ഓരോ പറമ്പിലുമുള്ള തെങ്ങുകളുടെ എണ്ണം = 24  
- ഓരോ തെങ്ങിൽ നിന്നും ഒരു മാസം കിട്ടുന്ന തേങ്ങ = 15  
- ഒരു തേങ്ങയുടെ വില = ₹12  

---

### ഘട്ടം 1: മൊത്തം തെങ്ങുകളുടെ എണ്ണം കണ്ടെത്തുക

3 പറമ്പുകളിലും ഓരോന്നിലും 24 തെങ്ങുകൾ ഉണ്ട്.

\[
3 \times 24 = 72
\]

അതുകൊണ്ട്, മൊത്തം തെങ്ങുകൾ = **72**

---

### ഘട്ടം 2: ഒരു മാസം കിട്ടുന്ന മൊത്തം തേങ്ങകളുടെ എണ്ണം കണ്ടെത്തുക

ഓരോ തെങ്ങിൽ നിന്നും ഒരു മാസം 15 തേങ്ങ കിട്ടുന്നു.

\[
72 \times 15 = 1080
\]

അതുകൊണ്ട്, ഒരു മാസം കിട്ടുന്ന മൊത്തം തേങ്ങ = **1080**

---

### ഘട്ടം 3: മൊത്തം വരുമാനം കണ്ടെത്തുക

ഒരു തേങ്ങ ₹12-ന് വിൽക്കുന്നു.

\[
1080 \times 12 = 12960
\]

അതുകൊണ്ട്, ഒരു മാസം ലഭിക്കുന്ന വരുമാനം = **₹12,960**

---

### ഉത്തരം:

**ഒരു മാസം അദ്ദേഹത്തിന് ₹12,960 ലഭിക്കും.**
```

</details>

<details><summary><b>Q4_K_M</b> — 13.56 s, 552 tokens, similarity 0.588</summary>

```text
ഘട്ടം 1: മൊത്തം തെങ്ങുകളുടെ എണ്ണം കണ്ടെത്തുക

3 പറമ്പുകളുണ്ട്.  
ഓരോ പറമ്പിലും 24 തെങ്ങുകൾ ഉണ്ട്.

അതുകൊണ്ട്,  
മൊത്തം തെങ്ങുകൾ = 3 × 24 = 72 തെങ്ങുകൾ

---

ഘട്ടം 2: ഒരു മാസം കിട്ടുന്ന മൊത്തം തേങ്ങകളുടെ എണ്ണം കണ്ടെത്തുക

ഓരോ തെങ്ങിൽ നിന്ന് മാസം 15 തേങ്ങ കിട്ടും.

അതുകൊണ്ട്,  
മൊത്തം തേങ്ങകൾ = 72 × 15 = 1080 തേങ്ങകൾ

---

ഘട്ടം 3: മൊത്തം വിൽപ്പന വില കണ്ടെത്തുക

ഒരു തേങ്ങ ₹12-ന് വിൽക്കുന്നു.

അതുകൊണ്ട്,  
മൊത്തം വരുമാനം = 1080 × 12 = ₹12,960

---

**ഉത്തരം:** ഒരു മാസം അദ്ദേഹത്തിന് **₹12,960** ലഭിക്കും.
```

</details>

<details><summary><b>IQ4_XS</b> — 11.54 s, 529 tokens, similarity 0.363</summary>

```text
നൽകിയിരിക്കുന്ന വിവരങ്ങൾ:

- പറമ്പുകളുടെ എണ്ണം = 3  
- ഓരോ പറമ്പിലുമുള്ള തെങ്ങുകളുടെ എണ്ണം = 24  
- ഓരോ തെങ്ങിൽ നിന്നും ഒരു മാസം കിട്ടുന്ന തേങ്ങ = 15  
- ഒരു തേങ്ങയുടെ വില = ₹12  

**ഘട്ടം 1: ആകെ തെങ്ങുകളുടെ എണ്ണം കണ്ടെത്തുക**

3 പറമ്പുകളിലും ഓരോന്നിലും 24 തെങ്ങുകൾ ഉണ്ട്.

\[
3 \times 24 = 72
\]

അതുകൊണ്ട്, ആകെ തെങ്ങുകൾ = **72**

---

**ഘട്ടം 2: ഒരു മാസം കിട്ടുന്ന ആകെ തേങ്ങയുടെ എണ്ണം കണ്ടെത്തുക**

ഓരോ തെങ്ങിൽ നിന്നും 15 തേങ്ങ കിട്ടും.

\[
72 \times 15 = 1080
\]

അതുകൊണ്ട്, ഒരു മാസം കിട്ടുന്ന തേങ്ങ = **1080**

---

**ഘട്ടം 3: ആകെ ലഭിക്കുന്ന പണം കണ്ടെത്തുക**

ഒരു തേങ്ങ ₹12-ന് വിൽക്കുന്നു.

\[
1080 \times 12 = 12960
\]

അതുകൊണ്ട്, ഒരു മാസം അദ്ദേഹത്തിന് ലഭിക്കുന്ന പണം = **₹12,960**

**ഉത്തരം: ₹12,960**
```

</details>

<details><summary><b>Q3_K_M</b> — 9.39 s, 468 tokens, similarity 0.274</summary>

```text
ഘട്ടം ഘട്ടമായി കണക്കാക്കാം:

**1. ആകെ തെങ്ങുകളുടെ എണ്ണം**

ഒരു പറമ്പിൽ = 24 തെങ്ങുകൾ  
പറമ്പുകളുടെ എണ്ണം = 3

അതുകൊണ്ട്,  
ആകെ തെങ്ങുകൾ = 24 × 3 = **72 തെങ്ങുകൾ**

**2. ഒരു മാസം കിട്ടുന്ന ആകെ തേങ്ങകളുടെ എണ്ണം**

ഒരു തെങ്ങിൽ നിന്ന് ഒരു മാസം = 15 തേങ്ങ  
ആകെ തെങ്ങുകൾ = 72

അതുകൊണ്ട്,  
ആകെ തേങ്ങകൾ = 72 × 15 = **1080 തേങ്ങ**

**3. ഒരു മാസം ലഭിക്കുന്ന ആകെ വരുമാനം**

ഒരു തേങ്ങയുടെ വില = ₹12  
ആകെ തേങ്ങകൾ = 1080

അതുകൊണ്ട്,  
ആകെ വരുമാനം = 1080 × 12 = **₹12,960**

**ഉത്തരം:**  
ഒരു മാസം അദ്ദേഹത്തിന് **₹12,960** ലഭിക്കും.
```

</details>

<details><summary><b>IQ3_M</b> — 14.13 s, 691 tokens, similarity 0.211</summary>

```text
തന്നിരിക്കുന്ന വിവരങ്ങൾ:

- പറമ്പുകളുടെ എണ്ണം = 3  
- ഓരോ പറമ്പിലുമുള്ള തെങ്ങുകളുടെ എണ്ണം = 24  
- ഓരോ തെങ്ങിൽ നിന്ന് ഒരു മാസം കിട്ടുന്ന തേങ്ങ = 15  
- ഒരു തേങ്ങയുടെ വില = ₹12  

**ഘട്ടം 1: ആകെ തെങ്ങുകളുടെ എണ്ണം കണ്ടെത്തുക**

3 പറമ്പുകളിലും ആകെ തെങ്ങുകൾ:

\[
3 \times 24 = 72
\]

അതായത്, ആകെ **72 തെങ്ങുകൾ** ഉണ്ട്.

**ഘട്ടം 2: ഒരു മാസം കിട്ടുന്ന ആകെ തേങ്ങകളുടെ എണ്ണം കണ്ടെത്തുക**

ഓരോ തെങ്ങിൽ നിന്ന് 15 തേങ്ങ കിട്ടുന്നതിനാൽ:

\[
72 \times 15 = 1080
\]

അതായത്, ഒരു മാസം ആകെ **1080 തേങ്ങ** കിട്ടും.

**ഘട്ടം 3: ആകെ വരുമാനം കണ്ടെത്തുക**

ഒരു തേങ്ങ ₹12-ന് വിൽക്കുന്നതിനാൽ:

\[
1080 \times 12 = 12960
\]

അതുകൊണ്ട്, ഒരു മാസം അദ്ദേഹത്തിന് ലഭിക്കുന്ന പണം:

\[
\boxed{₹12,960}
\]

**ഉത്തരം: ഒരു മാസം അദ്ദേഹത്തിന് ₹12,960 ലഭിക്കും.**
```

</details>

### ml-heights (Malayalam)

> രവി അനുവിനേക്കാൾ ഉയരമുള്ളവനാണ്. അനു മീരയേക്കാൾ ഉയരമുള്ളവളാണ്. മീര ജോസഫിനേക്കാൾ ഉയരമുള്ളവളാണ്. ഏറ്റവും ഉയരം കുറഞ്ഞത് ആർക്കാണ്? ഏറ്റവും ഉയരം കൂടിയത് ആർക്കാണ്? മലയാളത്തിൽ ഉത്തരം നൽകുക.

<details><summary><b>Q8_0</b> — 4.92 s, 125 tokens</summary>

```text
ഏറ്റവും ഉയരം കുറഞ്ഞത്: **ജോസഫിൻ**  
ഏറ്റവും ഉയരം കൂടിയത്: **രവി**
```

</details>

<details><summary><b>Q6_K</b> — 4.54 s, 148 tokens, similarity 1.0</summary>

```text
ഏറ്റവും ഉയരം കുറഞ്ഞത്: **ജോസഫിൻ**  
ഏറ്റവും ഉയരം കൂടിയത്: **രവി**
```

</details>

<details><summary><b>Q5_K_M</b> — 4.32 s, 148 tokens, similarity 1.0</summary>

```text
ഏറ്റവും ഉയരം കുറഞ്ഞത്: **ജോസഫിൻ**  
ഏറ്റവും ഉയരം കൂടിയത്: **രവി**
```

</details>

<details><summary><b>Q4_K_M</b> — 7.04 s, 287 tokens, similarity 0.892</summary>

```text
ഏറ്റവും ഉയരം കുറഞ്ഞത് **ജോസഫിനാണ്**.  
ഏറ്റവും ഉയരം കൂടിയത് **രവിക്കാണ്**.
```

</details>

<details><summary><b>IQ4_XS</b> — 3.07 s, 125 tokens, similarity 1.0</summary>

```text
ഏറ്റവും ഉയരം കുറഞ്ഞത്: **ജോസഫിൻ**  
ഏറ്റവും ഉയരം കൂടിയത്: **രവി**
```

</details>

<details><summary><b>Q3_K_M</b> — 3.63 s, 169 tokens, similarity 1.0</summary>

```text
ഏറ്റവും ഉയരം കുറഞ്ഞത്: **ജോസഫിൻ**  
ഏറ്റവും ഉയരം കൂടിയത്: **രവി**
```

</details>

<details><summary><b>IQ3_M</b> — 6.53 s, 304 tokens, similarity 1.0</summary>

```text
ഏറ്റവും ഉയരം കുറഞ്ഞത്: **ജോസഫിൻ**  
ഏറ്റവും ഉയരം കൂടിയത്: **രവി**
```

</details>

### ml-weekday (Malayalam)

> ഇന്ന് ബുധനാഴ്ചയാണെങ്കിൽ, ഇന്നു മുതൽ 100 ദിവസം കഴിഞ്ഞാൽ ഏത് ദിവസമായിരിക്കും? മലയാളത്തിൽ വിശദീകരിക്കുക.

<details><summary><b>Q8_0</b> — 31.64 s, 852 tokens</summary>

```text
ഇന്ന് **ബുധനാഴ്ച**യാണെങ്കിൽ, ഇന്നു മുതൽ **100 ദിവസം കഴിഞ്ഞാൽ** ആവുന്ന ദിവസം **വെള്ളിയാഴ്ച** ആയിരിക്കും.

**വിശദീകരണം:**

- ഒരു ആഴ്ചയിൽ **7 ദിവസം** ഉണ്ട്.
- 100-നെ 7- കൊണ്ട് ഹരിക്കുമ്പോൾ:

\[
100 \div 7 = 14 \text{ ശിഷ്ടം } 2
\]

അതായത് 100 ദിവസം = 14 പൂർണ്ണ ആഴ്ചകൾ + **2 ദിവസം**.

- ഇന്ന് ബുധനാഴ്ച.
- 1 ദിവസം കഴിഞ്ഞാൽ → **വ്യാഴാഴ്ച**
- 2 ദിവസം കഴിഞ്ഞാൽ → **വെള്ളിയാഴ്ച**

അതിനാൽ, **100 ദിവസം കഴിഞ്ഞാൽ വെള്ളിയാഴ്ച** ആയിരിക്കും.
```

</details>

<details><summary><b>Q6_K</b> — 24.42 s, 852 tokens, similarity 0.646</summary>

```text
ഇന്ന് **ബുധനാഴ്ച**യാണെങ്കിൽ, ഇന്നു മുതൽ **100 ദിവസം കഴിഞ്ഞാൽ** ആവുന്ന ദിവസം **വെള്ളിയാഴ്ച** ആയിരിക്കും.

**വിശദീകരണം:**

- ഒരു ആഴ്ചയിൽ **7 ദിവസം** ഉണ്ട്.
- 100-നെ 7- കൊണ്ട് ഹരിക്കുമ്പോൾ:

\[
100 \div 7 = 14 \text{ ശിഷ്ടം } 2
\]

അതായത് 100 ദിവസം = **14 പൂർണ്ണ ആഴ്ചകൾ + 2 ദിവസം**.

- 14 പൂർണ്ണ ആഴ്ചകൾ കഴിഞ്ഞാലും ദിവസം മാറില്ല; അത് വീണ്ടും **ബുധനാഴ്ച** തന്നെ.
- അതിനു ശേഷം **2 ദിവസം** കൂടി കഴിയണം:
  - ബുധനാഴ്ച + 1 = **വ്യാഴാഴ്ച**
  - ബുധനാഴ്ച + 2 = **വെള്ളിയാഴ്ച**

അതിനാൽ ഉത്തരം: **വെള്ളിയാഴ്ച**.
```

</details>

<details><summary><b>Q5_K_M</b> — 23.99 s, 915 tokens, similarity 0.559</summary>

```text
ഇന്ന് **ബുധനാഴ്ച**യാണെങ്കിൽ, 100 ദിവസം കഴിഞ്ഞാൽ **വെള്ളിയാഴ്ച** ആയിരിക്കും.

**വിശദീകരണം:**

- ഒരു ആഴ്ചയിൽ **7 ദിവസം** ഉണ്ട്.
- 100-നെ 7- കൊണ്ട് ഹരിക്കുമ്പോൾ:

\[
100 \div 7 = 14 \text{ ശേഷിപ്പ് } 2
\]

അതായത്, 100 ദിവസം = **14 ആഴ്ച + 2 ദിവസം**.

- 14 ആഴ്ച കഴിഞ്ഞാൽ വീണ്ടും **ബുധനാഴ്ച** തന്നെയാകും.
- അതിനു ശേഷം 2 ദിവസം കൂടി:
  1. വ്യാഴാഴ്ച  
  2. വെള്ളിയാഴ്ച  

അതിനാൽ, 100 ദിവസം കഴിഞ്ഞാൽ **വെള്ളിയാഴ്ച** ആകും.
```

</details>

<details><summary><b>Q4_K_M</b> — 19.0 s, 804 tokens, similarity 0.35</summary>

```text
ഇന്ന് **ബുധനാഴ്ച**യാണെങ്കിൽ, 100 ദിവസം കഴിഞ്ഞാൽ **വെള്ളിയാഴ്ച** ആയിരിക്കും.

**വിശദീകരണം:**

ആഴ്ചയിൽ 7 ദിവസം ഉണ്ട്.  
അതിനാൽ 100-ൽ 7 കൊണ്ട് ഹരിക്കുമ്പോൾ:

\[
100 \div 7 = 14 \text{ ശിഷ്ടം } 2
\]

അതായത് 100 ദിവസം = 14 പൂർണ്ണ ആഴ്ചകൾ + 2 ദിവസം.

14 പൂർണ്ണ ആഴ്ചകൾ കഴിഞ്ഞാലും ദിവസം മാറില്ല, അത് വീണ്ടും ബുധനാഴ്ച തന്നെയാകും.  
അതിനു ശേഷം 2 ദിവസം കൂടി കൂട്ടണം:

- ബുധനാഴ്ച + 1 ദിവസം = **വ്യാഴാഴ്ച**
- ബുധനാഴ്ച + 2 ദിവസം = **വെള്ളിയാഴ്ച**

അതിനാൽ, 100 ദിവസം കഴിഞ്ഞാൽ **വെള്ളിയാഴ്ച** ആയിരിക്കും.
```

</details>

<details><summary><b>IQ4_XS</b> — 27.39 s, 1222 tokens, similarity 0.218</summary>

```text
ഉത്തരം: **വെള്ളിയാഴ്ച**

വിശദീകരണം:

- ആഴ്ചയിൽ **7 ദിവസം** ഉണ്ട്.
- 100 ദിവസം എന്നത് 7-ൽ ഹരിക്കുമ്പോൾ:

\[
100 \div 7 = 14 \text{ ആഴ്ചകൾ } + 2 \text{ ദിവസം ബാക്കി}
\]

അതായത് 14 പൂർണ്ണ ആഴ്ചകൾ കഴിഞ്ഞാൽ വീണ്ടും ബുധനാഴ്ച തന്നെയായിരിക്കും. അതിനു ശേഷം **2 ദിവസം** കൂടി കണക്കാക്കണം.

- ബുധനാഴ്ച + 1 ദിവസം = **വ്യാഴാഴ്ച**
- ബുധനാഴ്ച + 2 ദിവസം = **വെള്ളിയാഴ്ച**

അതിനാൽ, ഇന്ന് ബുധനാഴ്ചയാണെങ്കിൽ ഇന്നു മുതൽ **100 ദിവസം കഴിഞ്ഞാൽ വെള്ളിയാഴ്ച** ആയിരിക്കും.
```

</details>

<details><summary><b>Q3_K_M</b> — 13.05 s, 640 tokens, similarity 0.28</summary>

```text
ഇന്ന് **ബുധനാഴ്ച**യാണെങ്കിൽ, 100 ദിവസം കഴിഞ്ഞാൽ **വെള്ളിയാഴ്ച** ആയിരിക്കും.

**വിശദീകരണം:**

- 100 ദിവസം = 14 ആഴ്ച + 2 ദിവസം  
  കാരണം: 100 ÷ 7 = 14 ശിഷ്ടം 2.
- 14 ആഴ്ച കഴിഞ്ഞാൽ വീണ്ടും ബുധനാഴ്ച തന്നെ ആയിരിക്കും.
- അതിനു ശേഷം 2 ദിവസം കൂടി കഴിഞ്ഞാൽ:
  - ബുധനാഴ്ച → വ്യാഴാഴ്ച → **വെള്ളിയാഴ്ച**

അതുകൊണ്ട്, ഇന്ന് മുതൽ 100 ദിവസം കഴിഞ്ഞാൽ **വെള്ളിയാഴ്ച** ആയിരിക്കും.
```

</details>

<details><summary><b>IQ3_M</b> — 46.62 s, 2274 tokens, similarity 0.289</summary>

```text
ഉത്തരം: **വെള്ളിയാഴ്ച**

**വിശദീകരണം:**

- ഒരു ആഴ്ചയിൽ **7 ദിവസം** ഉണ്ട്.
- 100-നെ 7- കൊണ്ട് ഹരിച്ചാൽ:

\[
100 = 14 \times 7 + 2
\]

അതായത്, **14 പൂർണ്ണ ആഴ്ചകളും 2 ദിവസവും** ബാക്കി വരുന്നു.

- 14 ആഴ്ചകൾക്ക് ശേഷം ദിവസം മാറില്ല.
- അതിനാൽ ബാക്കി **2 ദിവസം** മാത്രം കണക്കാക്കണം.

ഇന്ന് **ബുധനാഴ്ച** ആണെങ്കിൽ:

1. 1 ദിവസം കഴിഞ്ഞാൽ → **വ്യാഴാഴ്ച**
2. 2 ദിവസം കഴിഞ്ഞാൽ → **വെള്ളിയാഴ്ച**

അതിനാൽ, **100 ദിവസം കഴിഞ്ഞാൽ വെള്ളിയാഴ്ച** ആയിരിക്കും.

> കുറിപ്പ്: “ഇന്ന് മുതൽ 100-ആം ദിവസം” എന്ന് ഇന്ന് എന്ന ദിവസം ഒന്നാമത്തെ ദിവസമായി കണക്കാക്കിയാൽ ഉത്തരം **വ്യാഴാഴ്ച** ആകും. പക്ഷേ സാധാരണ “100 ദിവസം കഴിഞ്ഞാൽ” എന്നത് ഇന്ന് കഴിഞ്ഞ ശേഷം 100 ദിവസം എന്നർത്ഥം; അതിനാൽ ഉത്തരം **വെള്ളിയാഴ്ച**.
```

</details>

### ml-discount (Malayalam)

> ഒരു ഷർട്ടിന്റെ വില ₹800 ആണ്. കട 25% കിഴിവ് നൽകുന്നു, തുടർന്ന് കിഴിവ് ചെയ്ത വിലയിൽ 5% നികുതി ചേർക്കുന്നു. അവസാന വില എത്ര? മലയാളത്തിൽ വിശദീകരിക്കുക.

<details><summary><b>Q8_0</b> — 14.95 s, 404 tokens</summary>

```text
അസൽ വില = ₹800

**1) 25% കിഴിവ്:**
കിഴിവ് = 800 × 25/100 = ₹200  
കിഴിവ് ചെയ്ത വില = 800 − 200 = ₹600

**2) 5% നികുതി:**
നികുതി = 600 × 5/100 = ₹30  
അവസാന വില = 600 + 30 = **₹630**

അതുകൊണ്ട് ഷർട്ടിന്റെ അവസാന വില **₹630** ആണ്.
```

</details>

<details><summary><b>Q6_K</b> — 11.6 s, 399 tokens, similarity 0.973</summary>

```text
അസൽ വില = ₹800

**1) 25% കിഴിവ്:**
കിഴിവ് = 800 × 25/100 = ₹200  
കിഴിവ് ചെയ്ത വില = 800 − 200 = ₹600

**2) 5% നികുതി:**
നികുതി = 600 × 5/100 = ₹30  
അവസാന വില = 600 + 30 = **₹630**

അതുകൊണ്ട്, അവസാന വില **₹630** ആണ്.
```

</details>

<details><summary><b>Q5_K_M</b> — 10.59 s, 404 tokens, similarity 1.0</summary>

```text
അസൽ വില = ₹800

**1) 25% കിഴിവ്:**
കിഴിവ് = 800 × 25/100 = ₹200  
കിഴിവ് ചെയ്ത വില = 800 − 200 = ₹600

**2) 5% നികുതി:**
നികുതി = 600 × 5/100 = ₹30  
അവസാന വില = 600 + 30 = **₹630**

അതുകൊണ്ട് ഷർട്ടിന്റെ അവസാന വില **₹630** ആണ്.
```

</details>

<details><summary><b>Q4_K_M</b> — 9.5 s, 403 tokens, similarity 0.607</summary>

```text
അവസാന വില **₹630** ആണ്.

**വിശദീകരണം:**

1. **അസൽ വില:** ₹800  
2. **25% കിഴിവ്:**  
   800 × 25/100 = ₹200  
3. **കിഴിവ് ചെയ്ത വില:**  
   800 − 200 = ₹600  
4. **5% നികുതി:**  
   600 × 5/100 = ₹30  
5. **അവസാന വില:**  
   600 + 30 = **₹630**
```

</details>

<details><summary><b>IQ4_XS</b> — 8.82 s, 400 tokens, similarity 0.655</summary>

```text
അവസാന വില = **₹630**

വിശദീകരണം:

1. **അസൽ വില** = ₹800  
2. **25% കിഴിവ്** = 800 × 25/100 = ₹200  
3. **കിഴിവ് ചെയ്ത വില** = 800 − 200 = ₹600  
4. **5% നികുതി** = 600 × 5/100 = ₹30  
5. **അവസാന വില** = 600 + 30 = **₹630**
```

</details>

<details><summary><b>Q3_K_M</b> — 5.79 s, 274 tokens, similarity 0.715</summary>

```text
ഷർട്ടിന്റെ ആദ്യ വില = ₹800

**1. 25% കിഴിവ്:**

കിഴിവ് = 800 × 25% = 800 × 0.25 = ₹200

കിഴിവ് ചെയ്ത വില = 800 − 200 = **₹600**

**2. 5% നികുതി:**

നികുതി = 600 × 5% = 600 × 0.05 = ₹30

**അവസാന വില:**

600 + 30 = **₹630**

അതുകൊണ്ട്, അവസാന വില **₹630** ആണ്.
```

</details>

<details><summary><b>IQ3_M</b> — 11.48 s, 553 tokens, similarity 0.409</summary>

```text
അവസാന വില **₹630** ആണ്.

**വിശദീകരണം:**

1. ഷർട്ടിന്റെ അസൽ വില = ₹800  
2. 25% കിഴിവ്:  
   \[
   800 \times 25\% = 800 \times 0.25 = ₹200
   \]
3. കിഴിവ് ചെയ്ത ശേഷമുള്ള വില:  
   \[
   800 - 200 = ₹600
   \]
4. ആ കിഴിവ് ചെയ്ത വിലയിൽ 5% നികുതി:  
   \[
   600 \times 5\% = 600 \times 0.05 = ₹30
   \]
5. അവസാന വില:  
   \[
   600 + 30 = ₹630
   \]

അതുകൊണ്ട്, ഷർട്ടിന്റെ അവസാന വില **₹630** ആണ്.
```

</details>

### ml-translate (Malayalam)

> താഴെയുള്ള മലയാളം വാക്യം ഇംഗ്ലീഷിലേക്ക് വിവർത്തനം ചെയ്യുക: "കനത്ത മഴ കാരണം കൊച്ചിയിലേക്കുള്ള ട്രെയിൻ രണ്ട് മണിക്കൂർ വൈകി."

<details><summary><b>Q8_0</b> — 0.83 s, 16 tokens</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>Q6_K</b> — 0.71 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.64 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.6 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.6 s, 17 tokens, similarity 0.688</summary>

```text
Due to heavy rain, the train to Kochi was delayed by two hours.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.59 s, 17 tokens, similarity 0.688</summary>

```text
Due to heavy rain, the train to Kochi was delayed by two hours.
```

</details>

<details><summary><b>IQ3_M</b> — 0.58 s, 17 tokens, similarity 0.688</summary>

```text
Due to heavy rain, the train to Kochi was delayed by two hours.
```

</details>

### hi-coconuts (Hindi)

> एक किसान के पास 3 खेत हैं। हर खेत में 24 नारियल के पेड़ हैं। हर पेड़ से हर महीने 15 नारियल मिलते हैं। वह एक नारियल ₹12 में बेचता है। एक महीने में उसकी कितनी कमाई होगी? हिंदी में चरण दर चरण समझाइए।

<details><summary><b>Q8_0</b> — 16.36 s, 439 tokens</summary>

```text
चरण-दर-चरण हल:

1. **कुल नारियल के पेड़**  
   खेतों की संख्या = 3  
   हर खेत में पेड़ = 24  
   कुल पेड़ = 3 × 24 = **72 पेड़**

2. **एक महीने में कुल नारियल**  
   हर पेड़ से हर महीने नारियल = 15  
   कुल नारियल = 72 × 15 = **1080 नारियल**

3. **एक महीने की कमाई**  
   एक नारियल की कीमत = ₹12  
   कुल कमाई = 1080 × 12 = **₹12,960**

**उत्तर:** एक महीने में उसकी कमाई **₹12,960** होगी।
```

</details>

<details><summary><b>Q6_K</b> — 13.16 s, 439 tokens, similarity 1.0</summary>

```text
चरण-दर-चरण हल:

1. **कुल नारियल के पेड़**  
   खेतों की संख्या = 3  
   हर खेत में पेड़ = 24  
   कुल पेड़ = 3 × 24 = **72 पेड़**

2. **एक महीने में कुल नारियल**  
   हर पेड़ से हर महीने नारियल = 15  
   कुल नारियल = 72 × 15 = **1080 नारियल**

3. **एक महीने की कमाई**  
   एक नारियल की कीमत = ₹12  
   कुल कमाई = 1080 × 12 = **₹12,960**

**उत्तर:** एक महीने में उसकी कमाई **₹12,960** होगी।
```

</details>

<details><summary><b>Q5_K_M</b> — 10.54 s, 401 tokens, similarity 1.0</summary>

```text
चरण-दर-चरण हल:

1. **कुल नारियल के पेड़**  
   खेतों की संख्या = 3  
   हर खेत में पेड़ = 24  
   कुल पेड़ = 3 × 24 = **72 पेड़**

2. **एक महीने में कुल नारियल**  
   हर पेड़ से हर महीने नारियल = 15  
   कुल नारियल = 72 × 15 = **1080 नारियल**

3. **एक महीने की कमाई**  
   एक नारियल की कीमत = ₹12  
   कुल कमाई = 1080 × 12 = **₹12,960**

**उत्तर:** एक महीने में उसकी कमाई **₹12,960** होगी।
```

</details>

<details><summary><b>Q4_K_M</b> — 10.44 s, 443 tokens, similarity 0.954</summary>

```text
चरण दर चरण हल:

1. **कुल नारियल के पेड़ ज्ञात करें**  
   खेतों की संख्या = 3  
   हर खेत में पेड़ = 24  
   कुल पेड़ = 3 × 24 = **72 पेड़**

2. **एक महीने में कुल नारियल ज्ञात करें**  
   हर पेड़ से हर महीने नारियल = 15  
   कुल नारियल = 72 × 15 = **1080 नारियल**

3. **एक महीने की कमाई ज्ञात करें**  
   एक नारियल की कीमत = ₹12  
   कुल कमाई = 1080 × 12 = **₹12,960**

**उत्तर:** एक महीने में उसकी कमाई **₹12,960** होगी।
```

</details>

<details><summary><b>IQ4_XS</b> — 9.32 s, 426 tokens, similarity 1.0</summary>

```text
चरण-दर-चरण हल:

1. **कुल नारियल के पेड़**  
   खेतों की संख्या = 3  
   हर खेत में पेड़ = 24  
   कुल पेड़ = 3 × 24 = **72 पेड़**

2. **एक महीने में कुल नारियल**  
   हर पेड़ से हर महीने नारियल = 15  
   कुल नारियल = 72 × 15 = **1080 नारियल**

3. **एक महीने की कमाई**  
   एक नारियल की कीमत = ₹12  
   कुल कमाई = 1080 × 12 = **₹12,960**

**उत्तर:** एक महीने में उसकी कमाई **₹12,960** होगी।
```

</details>

<details><summary><b>Q3_K_M</b> — 7.36 s, 352 tokens, similarity 0.724</summary>

```text
चरण-दर-चरण हल:

1. **कुल खेतों की संख्या** = 3  
2. **हर खेत में नारियल के पेड़** = 24  
   इसलिए, **कुल नारियल के पेड़** = 3 × 24 = **72 पेड़**

3. **हर पेड़ से हर महीने नारियल** = 15  
   इसलिए, **कुल नारियल हर महीने** = 72 × 15 = **1080 नारियल**

4. **एक नारियल की कीमत** = ₹12  
   इसलिए, **कुल कमाई** = 1080 × 12 = **₹12,960**

**उत्तर:** एक महीने में उसकी कमाई **₹12,960** होगी।
```

</details>

<details><summary><b>IQ3_M</b> — 7.54 s, 354 tokens, similarity 0.786</summary>

```text
चरण दर चरण हल:

1. **कुल खेतों की संख्या** = 3  
2. **हर खेत में नारियल के पेड़** = 24  
   तो कुल पेड़ = 3 × 24 = **72 पेड़**

3. **हर पेड़ से हर महीने नारियल** = 15  
   तो कुल नारियल = 72 × 15 = **1080 नारियल**

4. **एक नारियल का दाम** = ₹12  
   तो कुल कमाई = 1080 × 12 = **₹12,960**

**उत्तर: एक महीने में उसकी कमाई ₹12,960 होगी।**
```

</details>

### hi-heights (Hindi)

> रवि अनु से लंबा है। अनु मीरा से लंबी है। मीरा जोसेफ से लंबी है। सबसे छोटा कौन है? सबसे लंबा कौन है? हिंदी में उत्तर दीजिए।

<details><summary><b>Q8_0</b> — 3.77 s, 98 tokens</summary>

```text
सबसे लंबा: **रवि**  
सबसे छोटा: **जोसेफ**
```

</details>

<details><summary><b>Q6_K</b> — 4.11 s, 136 tokens, similarity 0.488</summary>

```text
सबसे छोटा: **जोसेफ**  
सबसे लंबा: **रवि**
```

</details>

<details><summary><b>Q5_K_M</b> — 3.69 s, 136 tokens, similarity 0.488</summary>

```text
सबसे छोटा: **जोसेफ**  
सबसे लंबा: **रवि**
```

</details>

<details><summary><b>Q4_K_M</b> — 2.55 s, 98 tokens, similarity 0.488</summary>

```text
सबसे छोटा: **जोसेफ**  
सबसे लंबा: **रवि**
```

</details>

<details><summary><b>IQ4_XS</b> — 4.07 s, 181 tokens, similarity 0.378</summary>

```text
सबसे छोटा: जोसेफ  
सबसे लंबा: रवि
```

</details>

<details><summary><b>Q3_K_M</b> — 3.38 s, 156 tokens, similarity 0.892</summary>

```text
सबसे लंबा: रवि  
सबसे छोटा: जोसेफ
```

</details>

<details><summary><b>IQ3_M</b> — 3.66 s, 168 tokens, similarity 0.488</summary>

```text
सबसे छोटा: **जोसेफ**  
सबसे लंबा: **रवि**
```

</details>

### hi-weekday (Hindi)

> अगर आज बुधवार है, तो आज से 100 दिन बाद कौन सा दिन होगा? हिंदी में समझाइए।

<details><summary><b>Q8_0</b> — 15.78 s, 441 tokens</summary>

```text
आज **बुधवार** है।

हफ्ते में **7 दिन** होते हैं, इसलिए दिन का चक्र हर 7 दिन में दोहराता है।

100 को 7 से भाग देने पर:

- 7 × 14 = 98  
- शेष = 100 − 98 = **2**

अर्थात 98 दिन बाद भी वही दिन रहेगा, यानी **बुधवार**।  
अब 2 दिन आगे बढ़ेंगे:

1. गुरुवार  
2. शुक्रवार

इसलिए आज से **100 दिन बाद शुक्रवार** होगा।
```

</details>

<details><summary><b>Q6_K</b> — 13.54 s, 473 tokens, similarity 0.723</summary>

```text
आज **बुधवार** है।

हफ्ते में **7 दिन** होते हैं, इसलिए दिन हर 7 दिन में दोहराते हैं।

100 को 7 से भाग दें:

\[
100 \div 7 = 14 \text{ शेष } 2
\]

यानी 100 दिन में **14 पूरे हफ्ते** और **2 दिन** बचते हैं।

14 पूरे हफ्ते बाद भी वही दिन रहेगा, यानी **बुधवार**।  
अब 2 दिन आगे बढ़ें:

1. गुरुवार  
2. शुक्रवार  

इसलिए आज से **100 दिन बाद शुक्रवार** होगा।
```

</details>

<details><summary><b>Q5_K_M</b> — 11.69 s, 453 tokens, similarity 0.718</summary>

```text
आज **बुधवार** है।

हफ्ते में **7 दिन** होते हैं, इसलिए दिन का चक्र हर 7 दिन में दोहराता है।

100 को 7 से भाग देने पर:

\[
100 \div 7 = 14 \text{ शेष } 2
\]

यानी 100 दिन में 14 पूरे हफ्ते और **2 दिन** बचते हैं।

अब बुधवार से 2 दिन आगे गिनें:

1. गुरुवार  
2. शुक्रवार  

इसलिए, आज से **100 दिन बाद शुक्रवार** होगा।
```

</details>

<details><summary><b>Q4_K_M</b> — 13.26 s, 556 tokens, similarity 0.424</summary>

```text
आज **बुधवार** है।

1 सप्ताह में **7 दिन** होते हैं।  
100 दिन को 7 से बांटें:

**100 ÷ 7 = 14 सप्ताह और 2 दिन शेष**

अर्थात 100 दिन = 14 पूरे सप्ताह + 2 दिन।  
14 पूरे सप्ताह बाद फिर वही दिन रहेगा, यानी **बुधवार**।  
अब बचे हुए **2 दिन** आगे बढ़ेंगे:

- 1 दिन बाद → **गुरुवार**
- 2 दिन बाद → **शुक्रवार**

इसलिए आज से **100 दिन बाद शुक्रवार** होगा।
```

</details>

<details><summary><b>IQ4_XS</b> — 8.28 s, 384 tokens, similarity 0.283</summary>

```text
आज **बुधवार** है।

एक सप्ताह में **7 दिन** होते हैं।  
100 को 7 से बांटें:

**100 ÷ 7 = 14 शेष 2**

यानी 100 दिन में 14 पूरे सप्ताह और **2 दिन** बचते हैं।

अब बुधवार से 2 दिन आगे गिनें:

1. गुरुवार  
2. शुक्रवार  

इसलिए, आज से **100 दिन बाद शुक्रवार** होगा।
```

</details>

<details><summary><b>Q3_K_M</b> — 5.5 s, 264 tokens, similarity 0.176</summary>

```text
आज **बुधवार** है।

100 दिन बाद का दिन निकालने के लिए 100 को 7 से बाँटते हैं:

**100 ÷ 7 = 14 शेष 2**

यानी 100 दिन में 14 पूरे सप्ताह और **2 दिन** बचते हैं।

बुधवार के बाद 2 दिन:

- 1 दिन बाद → गुरुवार  
- 2 दिन बाद → शुक्रवार  

इसलिए, आज से 100 दिन बाद **शुक्रवार** होगा।
```

</details>

<details><summary><b>IQ3_M</b> — 8.03 s, 389 tokens, similarity 0.621</summary>

```text
आज **बुधवार** है।

हफ्ते में **7 दिन** होते हैं, इसलिए दिन का क्रम हर 7 दिन में दोहराता है।

100 को 7 से भाग देने पर:

\[
100 \div 7 = 14 \text{ शेष } 2
\]

अर्थात् 100 दिन = 14 पूरे हफ्ते + **2 दिन**।

14 पूरे हफ्ते बाद भी दिन वही रहेगा, लेकिन **2 दिन आगे** जाना है:

- आज: बुधवार  
- 1 दिन बाद: गुरुवार  
- 2 दिन बाद: **शुक्रवार**

इसलिए आज से **100 दिन बाद शुक्रवार** होगा।
```

</details>

### hi-discount (Hindi)

> एक शर्ट की कीमत ₹800 है। दुकान 25% की छूट देती है, फिर छूट वाली कीमत पर 5% टैक्स जोड़ती है। अंतिम कीमत क्या है? हिंदी में समझाइए।

<details><summary><b>Q8_0</b> — 11.74 s, 312 tokens</summary>

```text
शर्ट की मूल कीमत = ₹800

1. **25% छूट**  
   छूट = 800 का 25% = ₹200  
   छूट के बाद कीमत = 800 − 200 = **₹600**

2. **5% टैक्स**  
   टैक्स = 600 का 5% = ₹30  
   अंतिम कीमत = 600 + 30 = **₹630**

**अतः अंतिम कीमत ₹630 है।**
```

</details>

<details><summary><b>Q6_K</b> — 9.21 s, 319 tokens, similarity 1.0</summary>

```text
शर्ट की मूल कीमत = ₹800

1. **25% छूट**  
   छूट = 800 का 25% = ₹200  
   छूट के बाद कीमत = 800 − 200 = **₹600**

2. **5% टैक्स**  
   टैक्स = 600 का 5% = ₹30  
   अंतिम कीमत = 600 + 30 = **₹630**

**अतः अंतिम कीमत ₹630 है।**
```

</details>

<details><summary><b>Q5_K_M</b> — 8.42 s, 320 tokens, similarity 1.0</summary>

```text
शर्ट की मूल कीमत = ₹800

1. **25% छूट**  
   छूट = 800 का 25% = ₹200  
   छूट के बाद कीमत = 800 − 200 = **₹600**

2. **5% टैक्स**  
   टैक्स = 600 का 5% = ₹30  
   अंतिम कीमत = 600 + 30 = **₹630**

**अतः अंतिम कीमत ₹630 है।**
```

</details>

<details><summary><b>Q4_K_M</b> — 8.43 s, 362 tokens, similarity 0.403</summary>

```text
शर्ट की मूल कीमत = ₹800

**1. 25% छूट निकालें:**  
25% of ₹800 = \( \frac{25}{100} \times 800 = ₹200 \)

**2. छूट के बाद कीमत:**  
₹800 − ₹200 = **₹600**

**3. छूट वाली कीमत पर 5% टैक्स:**  
5% of ₹600 = \( \frac{5}{100} \times 600 = ₹30 \)

**4. अंतिम कीमत:**  
₹600 + ₹30 = **₹630**

अतः शर्ट की अंतिम कीमत **₹630** है।
```

</details>

<details><summary><b>IQ4_XS</b> — 5.48 s, 248 tokens, similarity 0.964</summary>

```text
शर्ट की मूल कीमत = ₹800

1. **25% छूट**  
   छूट = 800 का 25% = ₹200  
   छूट के बाद कीमत = 800 − 200 = **₹600**

2. **5% टैक्स** छूट वाली कीमत पर  
   टैक्स = 600 का 5% = ₹30  
   अंतिम कीमत = 600 + 30 = **₹630**

**अतः अंतिम कीमत ₹630 है।**
```

</details>

<details><summary><b>Q3_K_M</b> — 4.82 s, 232 tokens, similarity 0.893</summary>

```text
शर्ट की मूल कीमत = ₹800

**1. 25% छूट:**
छूट = 800 का 25% = ₹200  
छूट के बाद कीमत = 800 − 200 = **₹600**

**2. 5% टैक्स:**
टैक्स = 600 का 5% = ₹30  
अंतिम कीमत = 600 + 30 = **₹630**

**उत्तर: अंतिम कीमत ₹630 है।**
```

</details>

<details><summary><b>IQ3_M</b> — 4.99 s, 236 tokens, similarity 0.923</summary>

```text
शर्ट की मूल कीमत = ₹800  

1. **25% छूट**  
   छूट = 800 का 25% = ₹200  
   छूट के बाद कीमत = 800 − 200 = ₹600  

2. **5% टैक्स**  
   टैक्स = 600 का 5% = ₹30  
   अंतिम कीमत = 600 + 30 = **₹630**  

**उत्तर: अंतिम कीमत ₹630 है।**
```

</details>

### hi-translate (Hindi)

> नीचे दिए गए हिंदी वाक्य का अंग्रेज़ी में अनुवाद कीजिए: "भारी बारिश के कारण कोच्चि जाने वाली ट्रेन दो घंटे लेट हो गई।"

<details><summary><b>Q8_0</b> — 0.84 s, 16 tokens</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>Q6_K</b> — 0.66 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>Q5_K_M</b> — 0.64 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>Q4_K_M</b> — 0.6 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>IQ4_XS</b> — 0.57 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>Q3_K_M</b> — 0.55 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>

<details><summary><b>IQ3_M</b> — 0.55 s, 16 tokens, similarity 1.0</summary>

```text
The train to Kochi was delayed by two hours due to heavy rain.
```

</details>
