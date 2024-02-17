
from typing import List


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        min_next_distance = [0] * len(triangle[-1])

        for row in reversed(triangle):
            updated_row = [a + md for a, md in zip(row, min_next_distance)]
            min_next_distance = [min(a1, a2) for a1, a2 in zip(updated_row[:-1], updated_row[1:])]

        return updated_row[0]


if __name__ == "__main__":
    sol = Solution()
    print(sol.minimumTotal(
        [
            [2],
            [3,4],
            [6,5,7],
            [4,1,8,3]
        ]
    ))