from typing import List
# Write any import statements here
from collections import defaultdict


def getMinProblemCount(N: int, S: List[int]) -> int:
    problem_nums = defaultdict(int)
    for s in sorted(S):
        # split with 3p problem
        num_3p_probs = s // 3
        remainder_3p = s % 3

        num_additional_3p_probs = num_3p_probs - problem_nums[3]
        num_remainder_3p_probs = 1 - problem_nums[remainder_3p]

        num_2p_probs = s // 2
        remainder_2p = s % 2

        num_additional_2p_probs = num_2p_probs - problem_nums[2]
        num_remainder_2p_probs = remainder_2p - problem_nums[remainder_2p]

        if num_remainder_3p_probs <= num_additional_2p_probs:
            problem_nums[3] += num_additional_3p_probs
            problem_nums[remainder_3p] += num_remainder_3p_probs
        else:
            problem_nums[2] += num_remainder_2p_probs
            problem_nums[remainder_2p] += num_remainder_2p_probs

    if 0 in problem_nums:
        del problem_nums[0]

    return sum(problem_nums.values())


def getMinProblemCountv2(N: int, S: List[int]) -> int:
    problem_nums = defaultdict(int)
    for s in sorted(S):
        # problems when splitting with 3p
        num_3p_probs = s // 3
        remainder_3p = s % 3

        # option1: take 3p problems and don't split the remainder
        additional_probs_3p_remainder = max(num_3p_probs - problem_nums[3], 0) + problem_nums[remainder_3p]
        # option2: take 3p problems and split the remainder into 1 and 1 if possible
        additional_probs_3p_1p = num_3p_probs - problem_nums[3] + (remainder_3p // 1) - problem_nums[1]

        # problems when splitting with 2p
        num_2p_probs = s // 2
        remainder_2p = s % 2

        # option3:
        additional_probs_2p_remainder = num_2p_probs - problem_nums[2] + (1 - problem_nums[1] if remainder_2p else 0)

        comparison_case = min(
            (additional_probs_3p_remainder, 0),
            (additional_probs_3p_1p, 1),
            (additional_probs_2p_remainder, 2)
        )

        if comparison_case == 0:
            problem_nums[3] = max(num_3p_probs, problem_nums[3])
            problem_nums[remainder_3p] = max(1, problem_nums[remainder_3p])
        elif comparison_case == 1:
            problem_nums[3] = max(num_3p_probs, problem_nums[3])
            problem_nums[1] += remainder_3p // 1
        else:
            problem_nums[2] += num_2p_probs - problem_nums[2]
            problem_nums[1] =

    if 0 in problem_nums:
        del problem_nums[0]

    return sum(problem_nums.values())


def getMinProblemCountv3(N: int, S: List[int]) -> int:
    max_score = max(S)

    if max_score % 3 == 0:
        return max_score // 3 + int(any(s % 3 != 0 for s in S))

    if max_score % 3 == 1 and 1 not in S and max_score - 1 not in S:
        return max_score // 3 + 1

    return max_score // 3 + int(any(s % 3 == 1 for s in S)) + int(any(s % 3 == 2 for s in S))


if __name__ == "__main__":
    print(getMinProblemCount(5, [2, 4, 6]))
