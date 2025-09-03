import collections
import functools

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        # [9,9,4]
        # [5,6,8]
        # [2,1,1]
        # O(N4^N)
        
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        m, n = len(matrix), len(matrix[0])

        @functools.cache
        def _dfs(x, y):
            max_path = 0

            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and matrix[x][y] < matrix[nx][ny]:
                    max_path = max(max_path, _dfs(nx, ny))

            return max_path + 1
        
        res = 1
        for x, row in enumerate(matrix):
            for y, _ in enumerate(row):
                res = max(res, _dfs(x, y))

        return res
