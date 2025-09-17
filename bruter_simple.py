import math, sympy as sp
def a(n):
    prime_factors = [factors for prime in [[i for _ in range(j)] for i, j in sp.ntheory.factorint(math.factorial(n)).items()] for factors in prime]
    best_m, data = float('inf'), {}
    for partition in sp.utilities.iterables.multiset_partitions(prime_factors):
        factors = sorted([math.prod(group) for group in partition])
        if len(factors) != len(set(factors)): continue
        test_m = factors[-1] - factors[0]
        if test_m <= n - 2 and len(factors) >= 2:
            if test_m < best_m:
                best_m = test_m
                data.update({test_m : [factors]})
            elif test_m == best_m: data[test_m].append(factors)
    return f"Result for {n}! - f({n}) = {best_m}\n" + "\n".join(str(i) for i in data[best_m])
for n in range(3, 26):  print(a(n) + "\n")