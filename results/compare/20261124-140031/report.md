# Quant comparison: Qwen3.8-27B

5 prompts × 1 quants, temperature 0, seed 42, context 16384, 1 timing run(s) per prompt, llama.cpp b12345. Similarity is measured against the Q8_0 answer (1.0 = identical text).

## Summary

| Quant | Correct | Avg total time (s) | Avg first-token / prefill (ms) | Avg generation (tok/s) | Avg similarity to Q8_0 | Load time (s) |
|---|---|---|---|---|---|---|
| IQ3_M | 5/5 | 12.12 | 470.59 | 51.95 | — | 12.7 |

## Per prompt: correct and total time (s)

| Prompt | Category | IQ3_M |
|---|---|---|
| q03-bat-ball-inr | Reasoning | ✅ 10.01 |
| q09-duplicates-code | Coding | ✅ 11.13 |
| q10-debugging | Coding | ✅ 20.69 |
| q22-invoice-json | Vision | ✅ 3.46 |
| q23-chart | Vision | ✅ 15.29 |

✅ correct · ❌ wrong · · not graded (compare by reading)

## Answers side by side

### q03-bat-ball-inr (Reasoning)

> A bat and a ball together cost ₹110.
The bat costs ₹100 more than the ball.

How much does the ball cost?

Explain why the intuitive answer may be incorrect.


<details><summary><b>IQ3_M</b> — 10.01 s, 498 tokens</summary>

```text
Let the ball cost **₹x**.

Then the bat costs **₹(x + 100)**.

Together they cost ₹110:

\[
x + (x + 100) = 110
\]

\[
2x + 100 = 110
\]

\[
2x = 10
\]

\[
x = 5
\]

So the **ball costs ₹5**.

The intuitive answer is often **₹10**, because people quickly think:

- Total = ₹110
- Bat costs ₹100 more
- So maybe ball = ₹10 and bat = ₹100

But that is wrong because if the ball costs ₹10, then the bat would need to cost ₹110 to be ₹100 more, making the total ₹120, not ₹110. The correct split is:

- Ball = ₹5
- Bat = ₹105
- Total = ₹110
- Difference = ₹100
```

</details>

### q09-duplicates-code (Coding)

> Write a Python function named find_duplicates(items) that identifies duplicate elements in a list.

Requirements:
1. Return only duplicate values.
2. Each duplicate should appear only once in the result.
3. Preserve the order in which duplicates are first detected.
4. Handle an empty list.
5. Provid

<details><summary><b>IQ3_M</b> — 11.13 s, 575 tokens</summary>

```text
```python
def find_duplicates(items):
    """
    Identify duplicate elements in a list.
    
    Args:
        items: A list of elements.
        
    Returns:
        A list of duplicate values, each appearing only once,
        in the order they were first detected as duplicates.
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not items:
        return []
    
    seen = set()
    duplicates = set()
    result = []
    
    for item in items:
        if item in seen:
            if item not in duplicates:
                duplicates.add(item)
                result.append(item)
        else:
            seen.add(item)
    
    return result


# Test cases
if __name__ == "__main__":
    # Test 1: Basic duplicates
    assert find_duplicates([1, 2, 3, 2, 4, 3, 5]) == [2, 3], f"Test 1 failed: {find_duplicates([1, 2, 3, 2, 4, 3, 5])}"
    
    # Test 2: No duplicates
    assert find_duplicates([1, 2, 3, 4, 5]) == [], f"Test 2 failed: {find_duplicates([1, 2, 3, 4, 5])}"
    
    # Test 3: Empty list
    assert find_duplicates([]) == [], f"Test 3 failed: {find_duplicates([])}"
    
    # Test 4: All same elements
    assert find_duplicates([7, 7, 7, 7]) == [7], f"Test 4 failed: {find_duplicates([7, 7, 7, 7])}"
    
    # Test 5: Multiple duplicates with different orders
    assert find_duplicates([5, 3, 5, 3, 5, 3]) == [5, 3], f"Test 5 failed: {find_duplicates([5, 3, 5, 3, 5, 3])}"
    
    # Test 6: Single element
    assert find_duplicates([1]) == [], f"Test 6 failed: {find_duplicates([1])}"
    
    # Test 7: Strings
    assert find_duplicates(["a", "b", "a", "c", "b"]) == ["a", "b"], f"Test 7 failed: {find_duplicates(['a', 'b', 'a', 'c', 'b'])}"
    
    print("All tests passed!")
```
```

</details>

### q10-debugging (Coding)

> ```python
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers) + 1):
        total += numbers[i]
    return total / len(numbers)
```

Identify every problem in this function.

Rewrite it correctly and explain:
1. Why the original code fails.
2. What happens with an empty lis

<details><summary><b>IQ3_M</b> — 20.69 s, 1064 tokens</summary>

```text
## Problems in the Original Code

Let's analyze the original function line by line:

```python
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers) + 1):   # ❌ Problem 1: Off-by-one error
        total += numbers[i]              # ❌ Problem 2: IndexError on last iteration
    return total / len(numbers)          # ❌ Problem 3: ZeroDivisionError on empty list
```

### Problem 1: Off-by-one error in `range()`
`range(len(numbers) + 1)` generates indices from `0` to `len(numbers)`, inclusive. But valid indices are `0` to `len(numbers) - 1`. So the loop iterates **one extra time**.

### Problem 2: `IndexError`
On the last iteration, `i = len(numbers)`, and `numbers[i]` raises an `IndexError` because that index is out of bounds.

### Problem 3: `ZeroDivisionError` on empty list
If `numbers` is empty, `len(numbers)` is `0`, so `total / len(numbers)` raises a `ZeroDivisionError`. There is no guard against this.

### Problem 4: No input validation
The function doesn't handle non-numeric inputs or non-list iterables gracefully (though this is more of a design concern).

---

## Corrected Code

```python
def calculate_average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list")
    total = sum(numbers)
    return total / len(numbers)
```

Or, if you prefer to keep the explicit loop (e.g., for educational purposes or to handle custom iterables):

```python
def calculate_average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list")
    total = 0
    for number in numbers:
        total += number
    return total / len(numbers)
```

> **Note:** Using `sum(numbers)` is idiomatic Python and is implemented in C under the hood, making it faster than a Python-level loop.

---

## Detailed Explanations

### 1. Why the Original Code Fails

| Issue | Explanation |
|-------|-------------|
| **Off-by-one in `range()`** | `range(len(numbers) + 1)` produces `len(numbers) + 1`
```

</details>

### q22-invoice-json (Vision)

> Extract the following information from this document:

1. Invoice number.
2. Invoice date.
3. Supplier name.
4. Customer name.
5. Total amount.
6. Tax amount.
7. Payment due date.

Return the result in JSON format.

If a field is missing or unreadable, return null. Do not guess.


<details><summary><b>IQ3_M</b> — 3.46 s, 110 tokens</summary>

```text
```json
{
  "invoice_number": "INV-2026-0457",
  "invoice_date": "12 October 2026",
  "supplier_name": "Bluewave Supplies Pvt Ltd",
  "customer_name": "Sunrise Retail LLC",
  "total_amount": "48,380.00",
  "tax_amount": "7,380.00",
  "payment_due_date": null
}
```
```

</details>

### q23-chart (Vision)

> Analyze this chart.

1. Identify the highest value.
2. Identify the lowest value.
3. Calculate the percentage change between the first and last periods.
4. Identify significant trends.
5. Explain what conclusions can and cannot be drawn.

Use only the information visible in the chart.


<details><summary><b>IQ3_M</b> — 15.29 s, 744 tokens</summary>

```text
Based on the provided bar chart titled **"Monthly Revenue, Jan to Jun 2026 (INR thousands)"**, here is the analysis:

---

### 1. **Highest Value**
- The highest monthly revenue is **140 (INR thousands)**, recorded in **June 2026**.

---

### 2. **Lowest Value**
- The lowest monthly revenue is **70 (INR thousands)**, recorded in **March 2026**.

---

### 3. **Percentage Change Between First and Last Periods**
- First period (January): **80**
- Last period (June): **140**

**Formula for percentage change:**
> ((New Value - Old Value) / Old Value) × 100

**Calculation:**
> ((140 - 80) / 80) × 100 = (60 / 80) × 100 = **75%**

✅ **Percentage change from January to June: +75%**

---

### 4. **Significant Trends**

- **Overall upward trend**: Despite a dip in March, revenue generally increases over the six-month period, ending at its peak in June.
  
- **Dip in March**: Revenue drops from 95 (Feb) to 70 (Mar), the lowest point in the dataset — a decline of ~26.3% from February.

- **Strong recovery and growth from April onward**: 
  - April: 120 (up from 70 in March → +71.4%)
  - May: 110 (slight dip from April, but still well above Jan–Mar levels)
  - June: 140 (new high, up from May)

- **Volatility**: There’s noticeable month-to-month fluctuation, especially between Feb→Mar (drop) and Mar→Apr (sharp rise).

- **End-of-period strength**: The last two months (May and June) show strong performance, with June being the absolute peak.

---

### 5. **Conclusions That Can and Cannot Be Drawn**

#### ✅ **Can be concluded (based only on visible data):**
- Revenue grew significantly from January to June (+75%).
- March was the weakest month; June was the strongest.
- There was a sharp drop in March followed by a strong rebound in April.
- The business showed resilience and growth after the March dip.
- The overall trajectory from January to June is positive.

#### ❌ **Cannot be concluded (not visible or inferable from this chart alone):**
- **Why** revenue dropped in March (e.g.
```

</details>
