import os
import math
import json
import time
import logging

from itertools import combinations
from logger import create_logger

def geometric_mean_heuristic(n):
    """
    Searches for likely factors of `n` using a window around `k`th root of `n`, 2 <= k <= n.
    Chooses all possibilities of k numbers in that window, multiplies them and compares to n!.
    Established minimum lower bound is n - 2, which comes from n! = n x (n-1) x ... x 3 x 2

    Args:
        n: the n to check

    Returns:
        dict(list(list)): dictionary with keys `m`, and values list of lists of factors corresponding to that m
    """
    
    data = {}
    factorial_n = math.factorial(n)
    window_size = float("inf")
    best_m = float("inf")
    best_factors = None

    # choose all potential k-tuples within a window near kth root of n, k <= n
    # start from largest number of factors, empirically speaking I saw many more results with a large number of factors
    for k in range(n, 1, -1):

        # estimated central tendency of k factors multiplying to n!
        geo_mean = int(math.factorial(n) ** (1/k))
        logger.info(f"Starting estimation for k = {k}. Estimated geometric mean of {geo_mean}")

        # window width will be geo_mean +- n. the window could be smaller but just to make sure!
        window_size = n

        # clip minimum factor at 2
        window = list(range(max(2, geo_mean - window_size), geo_mean + window_size + 1))
        logger.info(f"Window size is {len(window)}")
        total_possibilities = math.comb(len(window), k)
        logger.info(f"Sampling {k} numbers between [{window[0]}, {window[-1]}]. Total possibilities: {total_possibilities}")
        
        i = 0
        # now choose all potential k-tuples within a window near kth root of n, k <= n
        for factors in combinations(window, k):

            # minimum naive lower bound for m is n - 2, throw away now if fails
            if max(factors) - min(factors) <= n - 2 and math.prod(factors) == factorial_n:
                    factors = sorted(factors)
                    test_m = factors[-1] - factors[0]

                    # new best result
                    if test_m < best_m:
                        best_m = test_m
                        best_factors = factors
                        logger.info(f"New best: m = {test_m}, Factors = {factors}")

                        # now add to results
                        if test_m in data:
                            data[test_m].append(factors)
                        else:
                            data.update({test_m : [factors]})

                    # same score, add and analyze later
                    elif test_m == best_m:
                        if test_m in data:
                            data[test_m].append(factors)
                        else:
                            data.update({test_m : [factors]})

            
            i += 1

            if int(total_possibilities * 0.2) > 0 and i % int(total_possibilities * 0.2) == 0:
                logger.info(f"Checked {i}/{total_possibilities} combinations...")
    
    logger.info(f"Finished testing n = {n}. Final m = {best_m}, Factors = {best_factors}")
    return data

if __name__ == "__main__":

    # create logger
    log_dir = "logs-geometric-mean"
    create_logger(log_dir)
    logger = logging.getLogger("main")
    if not os.path.exists(log_dir + "/data"):
        os.makedirs(log_dir + "/data")

    # check between 4 - 49
    for n in range(4, 50):
        try:
            logger.info("\n" + "="*50)
            logger.info(f"Starting search for n = {n}.")
            results = geometric_mean_heuristic(n)
            # now save results
            with open(f"{log_dir}/data/{n}.json", "w") as f:
                json.dump(results, f, sort_keys = True)
        except KeyboardInterrupt:
            logger.info(f"User stopped execution.")
            break