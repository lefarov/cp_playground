
def solution(A):
    # write your code in Python 3.6
    a_sorted = sorted(A, reverse=True)
    diffs = min((abs(a1 - a2) for a1, a2 in zip(a_sorted[1:], a_sorted[:-1])))

    return max(diffs, int(10e8))