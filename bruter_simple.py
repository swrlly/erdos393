import math
from sympy.utilities.iterables import multiset_partitions
from sympy.ntheory import factorint
# full source code is available at https://github.com/swrlly/erdos393

def a(n):
    prime_factors = [factors for prime in [[i for _ in range(j)] for i, j in factorint(math.factorial(n)).items()] for factors in prime]
    best_m = float('inf')
    data = {}
    for partition in multiset_partitions(prime_factors):
        factors = [math.prod(group) for group in partition]
        factors.sort()
        if len(factors) != len(set(factors)): continue
        test_m = factors[-1] - factors[0]
        if test_m <= n - 2 and len(factors) >= 2:
            if test_m < best_m:
                best_m = test_m
                data.update({test_m : [tuple(factors)]})
            elif test_m == best_m:
                data[test_m].append(tuple(factors))

    return f"Result for {n}! - f({n}) = {best_m}\n" + "\n".join(str(i) for i in set(tuple(data[best_m])))

for n in range(3, 26):  print(a(n) + "\n")