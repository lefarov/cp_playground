from typing import List


def nextPermutation(nums: List[int]) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    # [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]

    # [2,      3,       1]
    # (1 2 3) (1, 3)   (1)
    #    *        *     *

    sorted_nums = sorted(nums)
    num_to_ind = {num: ind for ind, num in enumerate(sorted_nums)}
    inds = [num_to_ind[num] for num in nums]

    # numbers: [1, 2, 3]
    # inds: [1, 2, 0]
    def _rec_permutation(numbers, progress_inds):
        if not numbers:
            yield []

        start_ind = progress_inds[0]
        for i, n in zip(range(start_ind, len(numbers)), numbers[start_ind:]):
            for rest in _rec_permutation(numbers[:i] + numbers[i + 1:], progress_inds[1:]):
                yield [n] + [rest]

    generator = _rec_permutation(sorted_nums, inds)
    return next(generator)


if __name__ == "__main__":
    print(nextPermutation([2, 3, 1]))
