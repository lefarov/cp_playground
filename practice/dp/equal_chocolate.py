"""
[Equal Chocolate Problem](https://www.hackerrank.com/challenges/equal/problem)
"""

import math
import os
import random
import re
import sys

from itertools import combinations, product


# Complete the equal function below.
def equal(arr):
    memory = {}
    visited = set()
    diff = tuple(map(lambda a: a - max(arr), arr))
    return recursive_solve(diff, 0, memory, visited)


def recursive_solve(diff, count, memory, visited):
    visited.add(diff)

    if not any(diff):
        return count

    sub_count_min = float("inf")
    for updated_diff in get_updated_diff(diff, visited):
        if updated_diff not in memory:
            sub_count_min = min(
                sub_count_min, 
                recursive_solve(updated_diff, count + 1, memory, visited)
            )
        else:
            sub_count_min = min(sub_count_min, memory[diff])

    memory[diff] = sub_count_min
    return sub_count_min


def get_updated_diff(diff, visited):
    indices = combinations(range(len(diff)), len(diff) - 1)
    actions = [1, 2, 5]
    
    for inds, act in product(indices, actions):
        candidate = tuple(sorted(d + act if i in inds else d for i, d in enumerate(diff)))
        if candidate not in visited:
            yield candidate
    


if __name__ == '__main__':
    print(equal([2, 2, 3, 7]))
