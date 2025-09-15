import os
import json
import math
import logging
from logger import create_logger
from test_generate_partitions import final_test
from generate_partitions import partition_list, partition_list_generator

# from https://github.com/fermi-fan/Python_Algorithms/blob/master/maths/special_numbers/bell_numbers.py
def bell_numbers(max_set_length: int) -> list[int]:
    if max_set_length < 0:
        raise ValueError("max_set_length must be non-negative")

    bell = [0] * (max_set_length + 1)
    bell[0] = 1

    for i in range(1, max_set_length + 1):
        for j in range(i):
            bell[i] += math.comb(i - 1, j) * bell[j]

    return bell

def prime_factors_list(n):
    """
    Return prime factorization as a list of prime factors (with repetition)
    Examples:
    >>> prime_factors_list(12)
    [2, 2, 3]

    >>> prime_factors_list(60)
    [2, 2, 3, 5]
    """
    def sieve_of_eratosthenes(limit):
        if limit < 2:
            return []
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(math.sqrt(limit)) + 1):
            if is_prime[i]:
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = False
        return [i for i in range(2, limit + 1) if is_prime[i]]
    
    # get primes up to sqrt(n)
    primes = sieve_of_eratosthenes(int(math.sqrt(n)) + 1)
    
    # get all factors of n
    factors = []
    for prime in primes:
        while n % prime == 0:
            factors.append(prime)
            n //= prime
    
    # if n > 1, it's a prime factor
    if n > 1:
        factors.append(n)
    
    return factors

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
    prime_factors = prime_factors_list(factorial_n)
    total_partitions_to_check = bell_numbers(len(prime_factors))[-1]
    
    logger.info(f"n = {n}")
    logger.info(f"n! = {factorial_n}")
    logger.info(f"Prime factors of {n}!: {prime_factors}")
    logger.info(f"Total prime factors: {len(prime_factors)}")
    logger.info(f"Total partitions to check: {total_partitions_to_check}")
    
    best_m = float('inf')
    best_partition = None
    best_factors = None
    ctr = 0

    # save best results for later inspection
    data = {}

    for partition in partition_list_generator(prime_factors):
        if ctr % 10 ** (n - 4) == 0:
            logger.info(f"Checked {ctr}/{total_partitions_to_check} partitions...")
        
        # calculate product of each group in partition
        factors = [math.prod(group) for group in partition]

        # sort factors and calculate range
        factors.sort()

        # check for duplicates, each factor needs to be ascending
        if len(factors) != len(set(factors)):
            ctr += 1
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

                # now add to data
                # keep track of how many times each factoring appears, lots of repeats because
                # the prime factors permute among the factors
                tup = str(factors)
                # first time seeing a better m
                data.update({test_m : {str(factors) : 1}})
            
            # same score, add and analyze later
            elif test_m == best_m:
                if test_m in data:
                    tup = str(factors)
                    if tup in data[test_m]:
                        data[test_m][tup] += 1
                    else:
                        data[test_m].update({str(factors) : 1})
                else:
                    # should never run into this case since test_m was added before!
                    data.update({test_m : {str(factors) : 1}})


        ctr += 1
    
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

    
    logger.info("Testing partition generator function")
    final_test(logger.info)
    logger.info("\n" + "="*50)
    

    logger.info("Testing prime_factors_list:")    
    for num in [12, 24, 60, 100]:
        factors = prime_factors_list(num)
        product_check = 1
        for f in factors:
            product_check *= f
        logger.info(f"{num}: {factors} (check: {product_check == num})")
    
    
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
