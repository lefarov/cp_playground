
from typing import List
from collections import defaultdict


def max_value(items: List[List[int]], capacity: int):
    # DP memory for storing partial solutions.
    subsolutions = defaultdict(lambda: defaultdict(int))
    # sort by size
    for current_capa in range(items[0][-1], capacity + 1):
        for i, item in enumerate(items):
            if item[-1] > current_capa:
                subsolutions[current_capa][i] = subsolutions[current_capa][i - 1]
            else:
                subsolutions[current_capa][i] = max(
                    item[0] + subsolutions[current_capa - item[-1]][i - 1],
                    subsolutions[current_capa][i - 1],
                )

    return [
        subsolutions[capacity][len(items) - 1],
        backtrack_subsolutions(subsolutions, items, capacity)
    ]

def backtrack_subsolutions(subsolutions, items, capacity):
    sequence = []
    i = len(items) - 1
    capa = capacity
    while i >= 0 and capa > 0:
        if subsolutions[capa][i] == subsolutions[capa][i - 1]:
            i -= 1
        else:
            sequence.append(i)
            capa = capa - items[i][-1]
            i -= 1

    return sequence[::-1]
            

if __name__ == "__main__":
    print(max_value([[1, 2], [4, 3], [5, 6], [6, 7]], 10))
