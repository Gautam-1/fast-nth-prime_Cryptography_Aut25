# fast-nth-prime_Cryptography_Aut25
A high-performance, pure Python implementation to find the N-th prime number using the Meissel-Lehmer algorithm (Iterative / Lucy Hedgehog variant) and Binary Search. Complexity: O(N^(3/4)).

# Fast N-th Prime Finder (Python)

This repository contains a high-performance, pure Python implementation for finding the **n-th prime number** without generating all preceding primes. 

It achieves this by combining **Binary Search** with an optimized **Prime Counting Function ($\pi(x)$)** based on the iterative Meissel-Lehmer algorithm (often referred to in competitive programming as the "Lucy Hedgehog" method).

## Features:-

* **Speed:** Calculates the n-th prime for large $n$ (e.g., $n=10^8$) in seconds, where standard sieving would fail or run out of memory.
* **Memory Efficient:** Uses $O(x^{1/2})$ space, avoiding the massive memory overhead of a standard Sieve of Eratosthenes for large ranges.
* **Pure Python:** No external C++ bindings or complex dependencies required.
* **Optimized Sieve:** Includes a bitwise Wheel Sieve for the pre-computation phase.

## How It Works:-

Finding the n-th prime is typically an inverse problem of counting primes. If we can quickly calculate $\pi(x)$ (the number of primes less than or equal to $x$), we can binary search for the answer.

### 1. The Prime Counting Function $\pi(x)$
Instead of iterating through every number, this project uses a combinatorial approach:
* **Algorithm:** Iterative Meissel-Lehmer (Lucy Hedgehog variant).
* **Logic:** It calculates partial sieve functions using Dynamic Programming on two arrays of size $\sqrt{x}$.
* **Complexity:** $O(x^{3/4})$ time and $O(x^{1/2})$ space.

### 2. Binary Search
We know that the n-th prime $p_n$ is approximately $n \ln n$. We perform a binary search on the answer:
1.  Guess a number $mid$.
2.  Calculate $\pi(mid)$ using the fast counting function.
3.  If $\pi(mid) < n$, the answer is higher. Otherwise, it is lower.

