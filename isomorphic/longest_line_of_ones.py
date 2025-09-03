import functools
from typing import List

DIRS = [
    ( 0,  1),
    ( 1,  1),
    ( 1,  0),
    ( 1, -1),
    ( 0, -1),
    (-1, -1),
    (-1,  0),
]

class Solution:
    def longest_line(self, matrix: List[List[int]]):
        # check if empty

        m, n = len(matrix), len(matrix[0])
        
        @functools.cache
        def check_line(i, j, _dir):

            path = 1
            ni, nj = i + _dir[0], j + _dir[1]
            if (
                0 <= ni < m and
                0 <= nj < n and
                matrix[ni][nj] == 1
            ):
                path += check_line(ni, nj, _dir)

            return path

        res = 0
        for i, row in enumerate(matrix):
            for j, e in enumerate(row):
                if e == 1:
                    for _dir in DIRS:
                        res = max(check_line(i, j, _dir), res)

        return res


if __name__ == "__main__":
    # 1 1 1 1
    # 0 1 1 0
    # 1 0 1 1

    # [1 1 1 1] [0 1 1 0] [0 0  0  1]
    #  0 1 2 3   4 5 6 7   8 9 10 11

    # [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (2, 3)]

    Solution().longest_line([[1, 1, 1, 1], [0, 1, 1, 0], [0, 0, 0, 1]])