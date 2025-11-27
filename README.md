# Fast N-th Prime Finder

This repository contains a high-performance, pure Python implementation for finding the **n-th prime number** without the memory overhead of generating all preceding primes.

The solution treats the problem as an inverse of the Prime Counting Function, $\pi(x)$. It combines a Binary Search on the answer with an optimized, iterative implementation of the Meissel-Lehmer algorithm (specifically the "Lucy Hedgehog" variant) to count primes efficiently.

## Mathematical Formulation

The algorithm solves for the n-th prime, $p_n$, by finding the smallest integer $x$ that satisfies the condition:

$$p_n = \min \{ x \in \mathbb{Z}^+ \mid \pi(x) \ge n \}$$

### Analytic Representation

The logic underlying the Prime Counting Function $\pi(x)$ can be summarized by the following compact analytic formula based on the Legendre-Meissel logic. This represents the calculation performed during each step of the binary search:

$$p_n = \text{BinarySearch}\left( x \in [0, 70n] \;\middle|\; \pi(x) - 1 + \sum_{S \subseteq \{p_1, \dots, p_a\}} (-1)^{|S|} \left\lfloor \frac{x}{\prod_{p \in S} p} \right\rfloor = n \right)$$

**Explanation of Terms:**
* **$x$**: The candidate integer being evaluated in the search.
* **$a$**: The number of primes less than or equal to $\sqrt{x}$.
* **$S$**: Iterates over all subsets of the first $a$ primes (distinct prime factors).
* **$(-1)^{|S|}$**: The Inclusion-Exclusion principle. We subtract multiples of single primes, add back multiples of pairs of primes, subtract multiples of triples, etc.
* **$\lfloor \dots \rfloor$**: The floor function, counting multiples of the prime subset within $x$.

### Combinatorial Implementation (Meissel-Lehmer)

Directly computing the sum above is too slow ($2^a$ terms). This implementation approximates the sum efficiently using the **Meissel-Lehmer Recurrence**.

The code computes the Partial Sieve Function $\phi(x, a)$ using Dynamic Programming on two arrays (`smalls` and `larges`) via the following recurrence relation:

$$\phi(m, k) = \phi(m, k-1) - \left( \phi\left(\left\lfloor \frac{m}{p_k} \right\rfloor, k-1\right) - (k-1) \right)$$

This approach effectively groups the terms of the analytic sum, reducing the time complexity from exponential to sub-linear.

## Algorithm Details

The solution consists of three main components:

1.  **Optimized Wheel Sieve:**
    A bitwise pre-sieve generates small primes up to $\sqrt{x}$. This reduces the overhead of the main combinatorial stage.

2.  **Iterative Meissel-Lehmer (Lucy Hedgehog):**
    Instead of deep recursion, this implementation uses Dynamic Programming to solve the combinatorial identity. This allows the calculation of $\pi(x)$ for large inputs (e.g., $10^{13}$) where standard sieves fail due to memory constraints.

3.  **Binary Search:**
    Since $\pi(x)$ is a monotonic non-decreasing function, we perform a binary search to locate the precise value.
    * **Search Space:** The search range is initialized to $[0, 70n]$.
    * **Bound Justification:** The Prime Number Theorem implies $x \approx n \ln n$. Empirically, the inverse density ratio $\frac{x}{\pi(x)}$ remains strictly below $65.7$ for all $x \le 10^{29}$. Therefore, setting the upper limit to $70n$ provides a guaranteed conservative bound for finding the $n$-th prime for any practical computational input.

## Complexity Analysis

| Component | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| **Prime Counting $\pi(x)$** | $O\left(\frac{x^{3/4}}{\ln x}\right)$ | $O(x^{1/2})$ |
| **Total N-th Prime** | $O\left(x^{3/4}\right)$ | $O(x^{1/2})$ |

*Note: The time complexity is dominated by the combinatorial counting steps. The space complexity is low because we only require storage proportional to the square root of the input.*

## Usage

Import the functions from the main script to calculate specific prime counts or find the n-th prime.

```python
from main import nth_prime, prime_pi

# Example 1: Count primes up to 10^11
# Expected output: 4,118,054,813
count = prime_pi(10**11)
print(f"Primes <= 10^11: {count}")

# Example 2: Find the 300 millionth prime
# This will output the result and the binary search steps
nth_prime(3 * 10**8)
