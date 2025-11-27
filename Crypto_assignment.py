from math import isqrt

"""
-----------------------------------------------------------
Reference Values for pi(x) (Prime Counting Function)
-----------------------------------------------------------
x           pi(x)
-----------------------------------------------------------
10^1        4
10^2        25
10^3        168
10^4        1,229
10^5        9,592
10^6        78,498
10^7        664,579
10^8        5,761,455
10^9        50,847,534
10^10       455,052,511
10^11       4,118,054,813
10^12       37,607,912,018
10^13       346,065,536,839
10^14       3,204,941,750,802
10^15       29,844,570,422,669
-----------------------------------------------------------
"""

def prime_sieve(n):
    """returns a sieve of primes >= 5 and < n"""
    flag = n % 6 == 2
    sieve = bytearray((n // 3 + flag >> 3) + 1)
    for i in range(1, int(n**0.5) // 3 + 1):
        if not (sieve[i >> 3] >> (i & 7)) & 1:
            k = (3 * i + 1) | 1
            for j in range(k * k // 3, n // 3 + flag, 2 * k):
                sieve[j >> 3] |= 1 << (j & 7)
            for j in range(k * (k - 2 * (i & 1) + 4) // 3, n // 3 + flag, 2 * k):
                sieve[j >> 3] |= 1 << (j & 7)
    return sieve

def sieve(n):
    """returns a list of primes <= n using Wheel Sieve."""
    res = []
    if n > 1:
        res.append(2)
    if n > 2:
        res.append(3)
    if n > 4:
        sieve_data = prime_sieve(n + 1)
        res.extend([3 * i + 1 | 1 for i in range(1, (n + 1) // 3 + (n % 6 == 1)) 
                    if not (sieve_data[i >> 3] >> (i & 7)) & 1])
    return res

def prime_pi(N):
    """
    Computes pi(N) using Iterative Meissel-Lehmer,
    accelerated by pre-sieving primes up to sqrt(N),
    Also called Lucy Hedgehog method, O(pow(N,3/4)/ln(N)).
    """
    if N < 2: return 0
    if N == 2: return 1
    
    v = int(isqrt(N))
    
    # 1. Pre-compute primes <= v for sieve steps 
    primes = sieve(v)
    
    # 2. smalls[i] stores count of numbers <= i
    # and larges[i] stores count of numbers <= floor(N/i)

    smalls = [i - 1 for i in range(v + 1)]
    larges = [0] * (v + 1)
    for i in range(1, v + 1):
        larges[i] = (N // i) - 1
        
    # 3. Iterate ONLY over primes (Skipping composites entirely)
    for p in primes:
        # In the standard version, we check: if smalls[p] > smalls[p-1].
        # Since we are iterating a pre-computed prime list, we know p is prime.
        # However, 'smalls' still updates dynamically, so we need the 
        # value of pi(p-1) from the CURRENT state of smalls.
        
        sp = smalls[p - 1]  # This is effectively pi(p-1)
        p2 = p * p
        
        # Optimization: If p^2 > N, we can stop. 
        # But since we only generated primes up to v=sqrt(N), 
        # p^2 will never exceed N significantly enough to break early 
        # except at the very end.
        if p2 > N: 
            break

        # --- Update 'larges' (Values > v) ---
        # We subtract the count of composites formed by p.
        # Logic: larges[i] -= (count of numbers <= (N/i)/p) - (count of primes < p)
        
        # We only loop while floor(N/i) >= p^2
        # i.e., i <= N // p^2
        limit_larges = min(v, N // p2)
        
        for i in range(1, limit_larges + 1):
            # d = floor(floor(N/i) / p)
            d = (N // i) // p 
            
            # Lookup the count for d in either smalls or larges
            if d <= v:
                count_sub = smalls[d] - sp
            else:
                k = N // d
                count_sub = larges[k] - sp
            
            larges[i] -= count_sub

        # --- Update 'smalls' (Values <= v) ---
        # Standard sieve logic: remove multiples of p starting from p^2
        # Iterate backwards to avoid using updated values for current step
        
        # Since smalls[x] for x < p^2 is already "finished" relative to p,
        # we stop at p^2.
        if p2 <= v:
            for i in range(v, p2 - 1, -1):
                smalls[i] -= (smalls[i // p] - sp)

    return larges[1]

# target = pow(10,12)
# print("PI(Target)==",prime_pi(target))


def nth_prime(n):
    """Finds the n_th prime number in O(pow(n,3/4))
    (~ 10 sec) for n upto (3 * 10^9)
    """
    l = 0; r = 70*n
    print("L==",l,"R==",r)
    while(r-l>1):
        m = (r+l)>>1
        print("L==",l,"M==",m,"R==",r, "RANGE==",r-l-1)
        if(prime_pi(m)<n):
            l = m
        else:
            r = m
    print("N_th prime number is ==",r)

# 1st 10 dig prime
# nth_prime(50847535)

nth_prime(3*pow(10,8))



