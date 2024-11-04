from typing import List
import functools


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        if len(word) == 0:
            return True

        self.moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        @functools.cache
        def _dfs(word_i, row, col):
            if word_i == len(word) - 1:
                return True

            self.visited.add((row, col))

            for d_row, d_col in self.moves:
                row_next, col_next = row + d_row, col + d_col
                if (
                    0 <= row_next < len(board) and
                    0 <= col_next < len(board[0]) and
                    (row_next, col_next) not in self.visited and
                    board[row_next][col_next] == word[word_i + 1]
                ):
                    if _dfs(word_i + 1, row_next, col_next):
                        self.visited.remove((row, col))
                        return True

            self.visited.remove((row, col))
            return False

        for row_i, row in enumerate(board):
            for col_i, ch in enumerate(row):
                if ch == word[0]:
                    self.visited = set()
                    if _dfs(0, row_i, col_i):
                        return True

        return False


if __name__ == "__main__":
    print(Solution().exist([["A","B","C","E"],["S","F","E","S"],["A","D","E","E"]], "ABCESEEEFS"))
