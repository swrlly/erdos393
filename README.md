# erdos393

Brute force checker for [Erdos problem #393](https://www.erdosproblems.com/393).

The problem says:

Let $f(n)$ denote the minimal $m \geq 1$ such that
$$n! = a_1 \cdot a_2 \cdots a_t$$
with $a_1 < a_2 < \cdots < a_t = a_1 + m$. What is the behaviour of $f(n)$?

For example, $f(4) = 2$ because $4! = 4 \cdot 6$ where $6 = 4 + 2$ so $m = 2$. No other $m$ can be smaller, whatever factors you choose. Our job is to characterize $f(n)$ but the problem is still unsolved. Terence Tao created a [GitHub repository](https://github.com/teorth/erdosproblems) to try and link up Erdos problems to the [OEIS](https://oeis.org/).

# Usage

- `python bruter_simple.py` to run the brute force checker, `python bruter_verbose.py` to generate logs and results in `logs-bruteforce`
- `python geometric_mean_heuristic.py` to run a geometric mean based heuristic for finding $f(n)$
- `generate_partitions.py` + `python test_generate_partitions.py`: depreciated partition generators/testers, `sympy` is faster due to removing duplicate partitions

The `logs` folders contain a log of running `bruter_verbose.py` and `geometric_mean_heuristic.py`. `data` folders contain the results. Name of the `json` file corresponds to the results on $n$. Keys of the dictionaries are $m$, and values are factors of $n!$ corresponding to that $m$.

# Brute force approach

Because we're trying to find $a_1 \cdots a_t = n!$, we can find all possible $a_1\cdots a_t$ by moving each prime factor in the prime factorization of $n!$ into one of the slots $a_i$ such that $m$ is minimized. This implies if we find all multiset partitions of the prime factorization of $n!$, and find the smallest distance (the $m$) between $a_1$ and $a_t$, then we have found the solution $f(n)$. This is what my brute force approach did; I used [generators](https://docs.sympy.org/latest/modules/utilities/iterables.html#sympy.utilities.iterables.multiset_partitions) to ensure we could generate multiset partitions of the prime factorization of $n!$ on the fly (my computer crashed without generators on $f(10)$).

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
        <td>12 </td>
        <td>13 </td>
        <td>14 </td>
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
        <td>9 </td>
        <td>9 </td>
        <td>9 </td>
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
        <td><div style="width:46px">24,25,27,28,32,33</div></td>
        <td><div style="width:46px">39,40,42,44,45,48</div></td>
        <td><div style="width:46px">63,64,65,66,70,72</div></td>
    </tr>
    </table>
</div>

which is a new sequence not found in OEIS. More examples in [`logs-bruteforce`](https://github.com/swrlly/erdos393/tree/main/logs-bruteforce).

I also found another interesting approach to generating more values of $f(n)$.

# Geometric mean approach

The brute force approach is looking at too many possible partitions. For example, $6! = 2 \cdot 12 \cdot 30$ is already out of the question because the naive lower bound is $n - 2 = 6 - 2$ from $6! = 6 \cdot 5 \cdot 4 \cdot 3 \cdot 2$. To reduce the number of partitions checked, consider  $12 \cdot 14 \cdot 15 \cdot 16 = 8!$. We're multiplying four numbers, and the geometric mean is $\sqrt[4]{12 \cdot 14 \cdot 15 \cdot 16} = \sqrt[4]{8!}$. This means if we check all $\sqrt[k]{n!}$, and search around a window of $\sqrt[k]{n!}$, then we're likely to find a result. Some evidence towards this is finding the minimum $m$ is trying to reduce the distance between the min $a_1$ and the max $a_t$ which is like minimizing the variance of the factors, clustering them around the geometric mean. I interpret this as maximizing the probability of finding a match.

This method also gives us a way to check all possible $k$-factorizations of $n!$ where $2 \leq k \leq n$. At the end of this process we'll have found all possible factorizations of $n!$ with $2, 3,\dots, n$ factors which minimizes $m$. I went about this by defining a window $\sqrt[k]{n!} \pm n$ and choosing all possible combinations of $k$ factors from this window and checking if they multiplied to $n!$.

This method agreed with the brute force method (found same factorizations and $m$'s) and was able to generate up to $f(19)$:

<div style="display:flex; justify-content: center;">
    <table>
    <tr>
        <th>$n$</th>
        <td>15 </td>
        <td>16 </td>
        <td>17 </td>
        <td>18 </td>
        <td>19 </td>
    </tr>
    <tr>
        <th>$f(n)$ </th>
        <td>12 </td>
        <td>14 </td>
        <td>12 </td>
        <td>15 </td>
        <td>16 </td>
    </tr>
    <tr>
        <th>Example </th>
        <td><div style="width:55px">6,18,20,21,22, 25,26, 27,28</div></td>
        <td><div style="width:42px">14,16,18,20,22,24,25,26,27,28</div> </td>
        <td><div style="width:45px">60,63,64,65,66,68,70,72</div></td>
        <td><div style="width:50px">21,22,24,25,26,27,28,30,32,34,36</div></td>
        <td><div style="width:50px">6,8,9,10,12,13,14,15,16,17,18,19,20,21,22</div></td>
    </tr>
    </table>
</div>

These examples are not unique; more examples in [`logs-geometric-mean`](https://github.com/swrlly/erdos393/tree/main/logs-geometric-mean).

# Ideas for improvement

## Brute force
The brute force method creates all partitions of a set, which grows exponentially with respect to the Bell numbers. Any improvement here would need to optimize `partition_list_generator` or use a faster programming language than Python. Generators should be used when $n \geq 10$, while calculating $f(10)$ with the in-memory partition creator my computer paged at least 30 GB of saved partitions to the hard disk before crashing.

## Geometric mean
I think the geometric mean method can be significantly sped up by finding a mathematical bound on the window size. The window used was $\left[\max(\sqrt[k]{n!} - n, 2), \sqrt[k]{n!} + n\right]$ Based on empirical data, the current windows seem to be too wide. For example, from the logs we see:
- For $n = 19$, best $m$ was found when $k = 15$. We have $\sqrt[15]{19!}\approx 13$ with window $\[2, 32\]$. But the minimum factor $a_1 = 6$ while the max $a_t = 22$. There's a wide space between $a_1, a_t$ and the edge of the window.
- For $n = 17$, best $m$ found when $k=8$. We have $\sqrt[8]{17!} \approx 65$ with window $\[48, 82\]$. But again, $a_1 = 60, a_t = 72$, far from the edge of the window. 

The logs show many such cases. If there exists a number-theoretic bound for how much $a_1, \dots, a_t$ may vary whilst near the geometric mean and minimizing $m$, this bound can significantly speed up the geometric mean method. The window cannot be too small otherwise potential results can be missed. This happened to me when I used other window sizes such as $\pm 6\log_8(\sqrt[k]{n!})$ where results on $n\geq21$ were completely missed.

# Caveats?


I didn't consider negative factors in bruteforcing. But Terence provided solid [reasoning](https://github.com/teorth/erdosproblems/issues/92#issuecomment-3293076473) on why negative numbers do not need to be considered. His reasoning is for $a_1 < 0$ and $a_t > 0$. In the case where $a_1 < 0$ and $a_t < 0$, these cases are accounted for by looking at positive factorizations with an even number of factors. So it is sufficient to consider only positive integers.
