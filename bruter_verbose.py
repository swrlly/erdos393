import os
import json
import math
import logging
from logger import create_logger
import sympy as sp

def solve_erdos_problem_brute_force(n):
    """
    Brute force first few numbers to f(n) for Erdos #393 using partitions of the prime factors of n!
    https://www.erdosproblems.com/393
    Generates partitions of prime factorization of n! 
    
    Args:
        n: Find f(n)
    
    Returns:
        dict: Dictionary with best results
        dict: Dictionary with all equivalent best results, with a few worse results due to updating best results over time
    """
    import math
    
    factorial_n = math.factorial(n)
    prime_factors = [factors for prime in [[i for _ in range(j)] for i, j in sp.ntheory.factorint(factorial_n).items()] for factors in prime]
    
    logger.info(f"n = {n}")
    logger.info(f"n! = {factorial_n}")
    logger.info(f"Prime factors of {n}!: {prime_factors}")
    logger.info(f"Total prime factors: {len(prime_factors)}")
    
    best_m = float('inf')
    best_partition = None
    best_factors = None

    # save best results for later inspection
    data = {}

    for partition in sp.utilities.iterables.multiset_partitions(prime_factors):
        
        # calculate product of each group in partition
        factors = [math.prod(group) for group in partition]

        # sort factors and calculate range
        factors.sort()

        # check for duplicates, each factor needs to be ascending
        if len(factors) != len(set(factors)):
            continue
        
        test_m = factors[-1] - factors[0]
        
        # make sure we have at least two factors
        # minimum naive lower bound for m is n - 2, throw away now if fails
        if test_m <= n - 2 and len(factors) >= 2:

            # new best result
            if test_m < best_m:
                best_m = test_m
                best_partition = partition
                best_factors = factors
                logger.info(f"New best: m = {best_m}, Factors = {factors}")
                # first time seeing a better m
                data.update({test_m : [factors]})
            
            # same score, add and analyze later
            elif test_m == best_m:
                if test_m in data:
                    data[test_m].append(factors)
    
    return {
        'n': n,
        'factorial': factorial_n,
        'prime_factors': prime_factors,
        'best_m': best_m,
        'best_factors': best_factors,
        'best_partition': best_partition
    }, data

# brute force
if __name__ == "__main__":

    # create logger
    log_dir = "logs-bruteforce"
    create_logger(log_dir)
    logger = logging.getLogger("brute_force_checker")
    if not os.path.exists(log_dir + "/data"):
        os.makedirs(log_dir + "/data")
    
    # brute up to 25
    for n in range(3, 26):
        try:
            logger.info("\n" + "="*50)
            logger.info("Brute forcing Erdos #393 on n={}".format(n))
            result, data = solve_erdos_problem_brute_force(n)
            logger.info(f"Result: f({result['n']}) = {result['best_m']}")
            logger.info(f"Factors: {result['best_factors']}")
            logger.info(f"from the partition: {result['best_partition']}")
            # now save results
            with open(f"{log_dir}/data/{n}.json", "w") as f:
                json.dump(data, f, sort_keys = True)
        except KeyboardInterrupt:
            logger.info(f"User stopped execution.")
            break
