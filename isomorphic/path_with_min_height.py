import collections
import heapq
from typing import List, Set, Tuple


DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def find_min_max_path(grid: List[List[int]]) -> int:
    min_height = min(min(row) for row in grid)
    max_height = max(max(row) for row in grid)

    lp, rp = min_height, max_height
    while lp < rp:
        # find min possible height such as condition is still true
        mp = (lp + rp) // 2
        if bfs_traversal_with_max_height(grid, mp):
            rp = mp
        else:
            lp = mp + 1
    
    return rp


def bfs_traversal_with_max_height(grid: List[List[int]], max_height: int) -> bool:
    queue = collections.deque()
    queue.append((0, 0))
    
    visited = {(0, 0)}

    while queue:
        i, j = queue.popleft()
        for di, dj in DIRS:
            ni, nj = i + di, j + dj
            if (
                0 <= ni < len(grid) and
                0 <= nj < len(grid[0]) and
                (ni, nj) not in visited and
                grid[ni][nj] <= max_height
            ):
                if ni == len(grid) - 1 and nj == len(grid[0]) - 1:
                    return True

                visited.add((ni, nj))
                queue.append((ni, nj))

    return False


def find_min_max_path_dijksra(grid: List[List[int]]):
    heap = []
    heapq.heappush(heap, (grid[0][0], (0, 0)))
    visited = set()

    while heap:
        max_height, (i, j) = heapq.heappop(heap)

        if i == len(grid) - 1 and j == len(grid[0]) - 1:
            return max_height

        visited.add((i, j))

        for di, dj in DIRS:
            ni, nj = i + di, j + dj
            if (
                0 <= ni < len(grid) and
                0 <= nj < len(grid[0]) and
                (ni, nj) not in visited
            ):
                heapq.heappush(heap, (max(grid[ni][nj], max_height), (ni, nj)))

    return 0


def find_min_max_path_dp(grid: List[List[int]]):
    m, n = len(grid), len(grid[0])
    max_num_so_far = [[0 for _ in range(n)] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                max_num_so_far[i][j] = grid[i][j]
            elif i == 0 and j > 0:
                max_num_so_far[i][j] = max(max_num_so_far[i][j - 1], grid[i][j])
            elif i > 0 and j == 0:
                max_num_so_far[i][j] = max(max_num_so_far[i - 1][j], grid[i][j])
            else:
                max_num_so_far[i][j] = max(min(max_num_so_far[i - 1][j], max_num_so_far[i][j - 1]), grid[i][j])
    return max_num_so_far[m-1][n-1]


def find_min_max_path_dp_anna(grid: List[List[int]]):
    # Assume there is at least one element
    r, c = len(grid), len(grid[0])
    dp = [[0] * c for _ in range(r)]
    
    # Init
    dp[0][0] = float('inf')  # first entry is not considered
    for i in range(1, r):
        dp[i][0] = min(dp[i - 1][0], grid[i][0])
    for j in range(1, c):
        dp[0][j] = min(dp[0][j - 1], grid[0][j])
    
    # DP
    for i in range(1, r):  # row by row
        for j in range(1, c):
            if i == r - 1 and j == c - 1:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # last entry is not considered
            else:
                score1 = min(dp[i][j - 1], grid[i][j])  # left
                score2 = min(dp[i - 1][j], grid[i][j])  # up
                dp[i][j] = max(score1, score2)
    
    return dp[r - 1][c - 1]


if __name__ == "__main__":

    input = [
        [2, 9, 3, 6, 6],
        [0, 1, 4, 8, 7],
        [2, 3, 1, 9, 1],
    ]

    # [2, 9, 3, 6, 6],
    # [0, 1, 4, 8, 7],
    # [2, 3, 1, 9, 1],

    # [1, 9, 3, 3, 3]
    # [2, 2, 4, 8, 1]
    # [2]

    # input = [
    #     [1, 10],
    #     [1, 5],
    #     [9, 1]
    # ]


    input = [
        [7, 1, 8, 6, 5],
        [5, 5, 4, 2, 7],
    ]
    
    print(find_min_max_path_dp_anna(input))
