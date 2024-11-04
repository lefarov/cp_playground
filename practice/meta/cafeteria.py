from typing import List


# Write any import statements here

def vectorSub(vec1: List[int], vec2: List[int]):
    assert len(vec1) == len(vec2)

    return [v1 - v2 - 1 for v1, v2 in zip(vec1, vec2)]


def getMaxAdditionalDinersCount(N: int, K: int, M: int, S: List[int]) -> int:
    # Write your code here
    # N = 15
    # K = 2
    # M = 3
    # S = [11, 6, 14]
    # [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
    # [6, 11, 14]
    # [5, 4, 2, 1]

    # N = 10
    # K = 1
    # M = 2
    # S = [1, 10]
    # [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    #
    # [, 0, 1, 0, 0, 0, 0, 0, 0]
    # [0, 8, 0]
    S.sort()
    empty_spaces = vectorSub(S[1:], S[:-1])
    empty_spaces = [S[0] - 1, *empty_spaces, N - S[-1]]

    if K == 0:
        return sum(empty_spaces)

    total_additional_number = 0
    for subrow_ind, num_empty_spaces in enumerate(empty_spaces):
        num_neighbors = 2 if 0 < subrow_ind < len(empty_spaces) - 1 else 1
        total_additional_number += -(-max(0, num_empty_spaces - K * num_neighbors) // (K + 1))

    return total_additional_number


if __name__ == "__main__":
    print(getMaxAdditionalDinersCount(10, 1, 2, [1, 10]))
