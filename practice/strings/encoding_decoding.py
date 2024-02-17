
# %%
from itertools import combinations
from collections import Counter


_INT_2_STR = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]


def decode(code, number):
    code_counts = Counter(code)
    res = []

    candidates = combinations(_INT_2_STR, 2)
    candidate_inds = list(combinations(list(range(10)), 2))

    for i, candidate in enumerate(candidates):
        candidate_counts = Counter("".join(candidate))

        if code_counts == candidate_counts:
            res.append(candidate_inds[i])

    return res


print(decode(["S", "O", "I", "X", "E", "N"], 2))