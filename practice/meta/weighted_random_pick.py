import random
from typing import List


class Solution:

    def __init__(self, w: List[int]):
        # [3, 14, 1,  7 ]
        # [1, 17, 18, 25]
        self.cdf = [w[0]]
        for weight in w[1:]:
            self.cdf.append(self.cdf[-1] + weight)

    def pickIndex(self) -> int:
        rn = random.uniform(0, self.cdf[-1])

        sampled_ind = 0
        lp, rp = 0, len(self.cdf) - 1
        while lp <= rp:
            mp = (lp + rp) // 2

            if self.cdf[mp] < rn:
                lp = mp + 1
            else:
                sample_ind = mp
                rp = mp - 1

        return sampled_ind


if __name__ == "__main__":
    Solution([3, 14, 1, 7]).pickIndex()
