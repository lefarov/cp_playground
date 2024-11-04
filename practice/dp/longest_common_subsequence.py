from collections import defaultdict


def longestCommonSubsequence(str1, str2):
    # Write your code here.
    # "ZXVV YZW"
    # "X  KYKZPW"
    # ...ZXVX
    #    X

    # ACBD
    #   AB

    #   "" A  C  B  D
    # ""0  0  0  0  0
    # A 0  1  1  1  1
    # B 0  1  1  2  2
    # C 0  1  2  2  3
    # K []
    # Z []
    # P []
    # W []

    #  A C B D
    # [0]

    sublengths = defaultdict(lambda: defaultdict(int))
    lcs_trajectory = defaultdict(lambda: defaultdict(lambda: (False, (-1, -1))))

    for i, char1 in enumerate(str1):
        for j, char2 in enumerate(str2):
            # not adding char2 to sequence
            length_skip, prev_i, prev_j = max_and_argmax(sublengths, i, j)
            if char1 == char2:
                # add char2 to sequence:
                length_add = 1 + sublengths[i][j]

                if length_add > length_skip:
                    sublengths[i + 1][j + 1] = length_add
                    lcs_trajectory[i + 1][j + 1] = (True, (i, j))
                    continue

            sublengths[i + 1][j + 1] = length_skip
            lcs_trajectory[i + 1][j + 1] = (False, (prev_i, prev_j))

    return backtrack_lcs_trajectory(lcs_trajectory, str2, len(str1), len(str2))


def backtrack_lcs_trajectory(lcs_trajectory, str2, i, j):
    subsequence = []
    while True:
        bool_take, (prev_i, prev_j) = lcs_trajectory[i][j]
        if bool_take:
            subsequence = [str2[j - 1]] + subsequence

        if prev_i == -1 and prev_j == -1:
            break

        i, j = prev_i, prev_j

    return subsequence


def max_and_argmax(sublengths, i, j):
    if sublengths[i+1][j] > sublengths[i][j+1]:
        return sublengths[i+1][j], i+1, j
    else:
        return sublengths[i][j+1], i, j+1


if __name__ == "__main__":
    longestCommonSubsequence("abc", "acbd")