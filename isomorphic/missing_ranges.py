from typing import List



def missing_ranges(nums: List[int], lower: int, upper: int):
    # [0, 1, 3, 50, 75]
    # 0 99
    
    res = []

    if nums[0] - lower > 1:
        res.append([lower, nums[0] - 1])

    for i in range(len(nums) - 1):
        if nums[i + 1] - nums[i] > 1:
            res.append([nums[i] + 1, nums[i + 1] - 1])

    if upper - nums[-1] > 1:
        res.append([nums[-1] + 1, upper])

    return res


if __name__ == "__main__":
    
    print(missing_ranges([0, 1, 3, 50, 75], 0, 99))