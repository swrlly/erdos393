# erdos393

Brute force checker for [Erdos problem #393](https://www.erdosproblems.com/393).

The problem says:

Let $f(n)$ denote the minimal $m \geq 1$ such that
$$n! = a_1 \cdot a_2 \cdots a_t$$
with $a_1 < a_2 < \cdots < a_t = a_1 + m$. What is the behaviour of $f(n)$?

For example, $f(4) = 2$ because $4! = 4 \cdot 6 = 4 + 2$ so $m = 2$. No other $m$ can be smaller, whatever factors you choose. Our job is to characterize $f(n)$ but the problem is still unsolved. Terence Tao created a [GitHub repository](https://github.com/teorth/erdosproblems) to try and link up Erdos problems to the [OEIS](https://oeis.org/).

# Usage

- `python brute_force_checker.py` to run the brute force checker, unfeasable after $f(12)$
- `python geometric_mean_heuristic.py` to run a geometric mean based heuristic for finding $f(n)$
- `generate_partitions.py` contain functions to generate multiset partitions
- `python test_generate_partitions.py` to run tests on `generate_partitions.py`. The tests including
    - Testing in-memory multiset partition creator (`partition_list`) on 5, 9, and 12 elements by comparing to the corresponding [Bell number](https://en.wikipedia.org/wiki/Bell_number)
    - Testing multiset partition generator (`partition_list_generator`) on 5, 9, and 12 elements in the same fashion
    - Comparing the partitions created by `partition_list` and `partition_list_generator` one by one on 12 elements to ensure the functions generate the same partitions

The `logs` folders contain a log of running `brute_force_checker.py` and `geometric_mean_heuristic.py`. `data` folders contain the results. Name of the `json` file corresponds to the results on $n$. Keys of the dictionaries are $m$, and values are factors of $n!$ corresponding to that $m$. In `logs-bruteforce/data`, the structure is a bit different, for example in `6.json` we have `{"2": {"[8, 9, 10]": 4}, "4": {"[2, 3, 4, 5, 6]": 24}}`. 

We found a best $m$ of $2$, corresponding to the factors $8\cdot9\cdot10$, and 4 means the total number of times we saw this result while brute forcing.

### Brute force approach

Because we're trying to find $a_1 \cdots a_t = n!$, we can find all possible $a_1\cdots a_t$ by moving each prime factor in the prime factorization of $n!$ into one of the slots $a_i$ such that $m$ is minimized. This implies if we find all multiset partitions of the prime factorization of $n!$, and find the smallest distance (the $m$) between $a_1$ and $a_t$, then we have found the solution $f(n)$. This is what my brute force approach did; I used [generators](https://github.com/swrlly/erdos393/blob/31c0bd979919ff06c69f98909e2968ec0bccc3c8/generate_partitions.py#L77) to ensure we could generate multiset partitions of the prime factorization of $n!$ on the fly (my computer crashed without generators on $f(10)$).

Through brute forcing I found:

<div style="display:flex; justify-content: center;">
    <table>
    <tr>
        <th>$n$</th>
        <td>2</td>
        <td>3 </td>
        <td>4 </td>
        <td>5 </td>
        <td>6 </td>
        <td>7 </td>
        <td>8 </td>
        <td>9 </td>
        <td>10 </td>
        <td>11 </td>
    </tr>
    <tr>
        <th>$f(n)$ </th>
        <td>1 </td>
        <td>1 </td>
        <td>2 </td>
        <td>2 </td>
        <td>2 </td>
        <td>2 </td>
        <td>4 </td>
        <td>6 </td>
        <td>7 </td>
        <td>6 </td>
    </tr>
    <tr>
        <th>Example </th>
        <td><div style="width:21px">1,2</div> </td>
        <td><div style="width:21px">2,3</div> </td>
        <td><div style="width:33px">2,3,4</div> </td>
        <td><div style="width:38px">10,12</div></td>
        <td><div style="width:42px">8,9,10</div> </td>
        <td><div style="width:38px">70,72</div></td>
        <td><div style="width:50px">12,14,15,16</div></td>
        <td><div style="width:50px">6,7,8,9,10,12</div></td>
        <td><div style="width:59px">9,10,12,14,15,16</div></td>
        <td><div style="width:46px">30,32,33,35,36</div></td>
    </tr>
    </table>
</div>

which is a new sequence not found in OEIS. $f(12)$ would have taken 175 days so I stopped. Code is available [here](https://github.com/swrlly/erdos393) with corresponding logging, test cases, and more examples in [`logs-bruteforce`](https://github.com/swrlly/erdos393/tree/main/logs-bruteforce).

I also found another interesting approach to generating more values of $f(n)$.

### Geometric mean approach

The brute force approach is looking at too many possible partitions. For example, $6! = 2 \cdot 12 \cdot 30$ is already out of the question because the naive lower bound is $n - 2 = 6 - 2$ from $6! = 6 \cdot 5 \cdot 4 \cdot 3 \cdot 2$. To reduce the number of partitions checked, consider  $12 \cdot 14 \cdot 15 \cdot 16 = 8!$. We're multiplying four numbers, and the geometric mean is $\sqrt[4]{12 \cdot 14 \cdot 15 \cdot 16} = \sqrt[4]{8!}$. This means if we check all $\sqrt[k]{n!}$, and search around a window of $\sqrt[k]{n!}$, then we're likely to find a result. Some evidence towards this is finding the minimum $m$ is trying to reduce the distance between the min $a_1$ and the max $a_t$ which is like minimizing the variance of the factors, clustering them around the geometric mean. I interpret this as maximizing the probability of finding a match.

This method also gives us a way to check all possible $k$-factorizations of $n!$ where $2 \leq k \leq n$. I went about this by defining a window $\sqrt[k]{n!} \pm n$ and choosing all possible combinations of $k$ factors from this window and checking if they multiplied to $n!$. Code is [here](https://github.com/swrlly/erdos393/blob/main/geometric_mean_heuristic.py).

This method agreed with the brute force method (found same factorizations and $m$'s) and was able to generate up to $f(19)$ in less than a day:

<div style="display:flex; justify-content: center;">
    <table>
    <tr>
        <th>$n$</th>
        <td>12</td>
        <td>13 </td>
        <td>14 </td>
        <td>15 </td>
        <td>16 </td>
        <td>17 </td>
        <td>18 </td>
        <td>19 </td>
    </tr>
    <tr>
        <th>$f(n)$ </th>
        <td>9 </td>
        <td>9 </td>
        <td>9 </td>
        <td>12 </td>
        <td>14 </td>
        <td>12 </td>
        <td>15 </td>
        <td>16 </td>
    </tr>
    <tr>
        <th>Example </th>
        <td><div style="width:42px">24,25,27,28,32,33</div> </td>
        <td><div style="width:42px">39,40,42,44,45,48</div> </td>
        <td><div style="width:42px">63,64,65,66,70,72</div> </td>
        <td><div style="width:55px">6,18,20,21,22, 25,26, 27,28</div></td>
        <td><div style="width:42px">14,16,18,20,22,24,25,26,27,28</div> </td>
        <td><div style="width:45px">60,63,64,65,66,68,70,72</div></td>
        <td><div style="width:50px">21,22,24,25,26,27,28,30,32,34,36</div></td>
        <td><div style="width:50px">6,8,9,10,12,13,14,15,16,17,18,19,20,21,22</div></td>
    </tr>
    </table>
</div>

These examples are not unique; there's more examples in [`logs-geometric-mean`](https://github.com/swrlly/erdos393/tree/main/logs-geometric-mean). Keys in the `json` files are $m$'s, with corresponding examples.


# Caveats?

I didn't consider negative factors in bruteforcing. But I did use the geometric mean approach with windows going to negative values and didn't see any negative factors showing up for minimal $m$. Also, if there were possible negative $a_i$'s, then I believe they should only happen when there's an even number of $a_i$'s corresponding to the lowest $m$, since they'd all be negative with the same $m$. If one $a_i$ was negative, then (I believe) it would be better to choose the positive version instead, because it'd be closer to the geometric mean. If that is true then is is sufficient to consider only positive factorizations.

Terence provided solid [reasoning](https://github.com/teorth/erdosproblems/issues/92#issuecomment-3293076473) on why negative numbers do not need to be considered.