from typing import List


class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        cumsum = [nums[0]] * len(nums)
        for i, n in enumerate(nums[1:]):
            cumsum[i + 1] = n + cumsum[i]

        max_sum = 0

        lp = 0
        for ki in range(k, 1, -1):
            frac = cumsum[-1] / ki

            split = lp
            rp = len(cumsum) - 1
            while lp <= rp:
                mp = (lp + rp) // 2

                if cumsum[mp] <= frac:
                    split = mp
                    lp = mp + 1
                else:
                    rp = mp - 1

            segment_sum = cumsum[split]
            for i in range(split, len(cumsum)):
                cumsum[i] -= segment_sum

            max_sum = max(max_sum, segment_sum)

            lp = split + 1

        max_sum = max(max_sum, cumsum[-1])

        return max_sum


if __name__ == "__main__":
    print(Solution().splitArray([10,5,13,4,8,4,5,11,14,9,16,10,20,8], 8))
