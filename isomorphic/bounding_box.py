from typing import List


def find_bb(grid: List[List[int]], input_i: int, input_j):
    bb_min_i, bb_max_i = input_i, input_i
    bb_min_j, bb_max_j = input_j, input_j

    # search upper part
    bottom_i, upper_i = input_i, 0
    while bottom_i >= upper_i:
        mid_i = (bottom_i + upper_i) // 2
        if any(grid[mid_i]):
            bb_min_i = mid_i
            bottom_i = mid_i - 1
        else:
            upper_i = mid_i + 1
    
    # search lower part
    bottom_i, upper_i = len(grid) - 1, input_i
    while bottom_i >= upper_i:
        mid_i = (bottom_i + upper_i) // 2
        if any(grid[mid_i]):
            bb_max_i = mid_i
            upper_i = mid_i + 1
        else:
            bottom_i = mid_i - 1

    # search left part
    left_j, right_j = 0, input_j
    while left_j <= right_j:
        mid_j = (left_j + right_j) // 2
        if scan_column(grid, mid_j, bb_min_i, bb_max_i):
            bb_min_j = mid_j
            right_j = mid_j - 1
        else:
            left_j = mid_j + 1

    # search right part
    left_j, right_j = input_j, len(grid[input_i]) - 1
    while left_j <= right_j:
        mid_j = (left_j + right_j) // 2
        if scan_column(grid, mid_j, bb_min_i, bb_max_i):
            bb_max_j = mid_j
            left_j = mid_j + 1
        else:
            right_j = right_j - 1

    
    return [bb_min_i, bb_min_j, bb_max_i, bb_max_j]


def scan_column(grid: List[List[int]], j: int, min_i: int, max_i: int):
    for i in range(min_i, max_i + 1):
        if grid[i][j] == 1:
            return True
        
    return False


def test_all_starting_positions(grid: List[List[int]], target: List[int]):
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == 1:
                assert find_bb(grid, i, j) == target


if __name__ == "__main__":
    input1 = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 1, 1, x, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]
    
    target1 = [1, 1, 4, 4]
    test_all_starting_positions(input1, target1)

    input2 = [[1]]
    target2 = [0, 0, 0, 0]
    test_all_starting_positions(input2, target2)