from collections import defaultdict


def maximumSumSubmatrix(matrix, size):
    # Write your code here.
    # [ 2, 4, -1]
    # [ 5, 6, 10]
    # [-3, 2,  0]

    sub_sums = defaultdict(lambda: defaultdict(int))
    for i, row in enumerate(matrix):
        sum = 0
        for j, val in enumerate(row):
            sum += val
            sub_sums[i][j] = sum + sub_sums[i - 1][j]

    max_sum = -float("inf")
    for row_i in range(size - 1, len(matrix)):
        for col_i in range(size - 1, len(matrix[0])):
            sum = (
                sub_sums[row_i][col_i]
                - sub_sums[row_i - size][col_i]
                - sub_sums[row_i][col_i - size]
                + sub_sums[row_i - size][col_i - size]
            )
            max_sum = max(sum, max_sum)

    return max_sum


if __name__ == "__main__":
    maximumSumSubmatrix([[2, 4, -1], [5, 6, 10], [-3, 2, 0]], 2)
