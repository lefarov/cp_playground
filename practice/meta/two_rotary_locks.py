from typing import List

def getMinCodeEntryTime(N: int, M: int, C: List[int]) -> int:
    memo = {}
    return recursiveMinTime(N, M, C, 0, 1, 1, memo)


def recursiveMinTime(N, M, C, i, left_lock, right_lock, memo):
    if i == M:
        return 0

    if (left_lock, right_lock) not in memo:
        turn_left_time = getMinDistance1wheel(C[i], left_lock, N) + recursiveMinTime(N, M, C, i + 1, C[i], right_lock, memo)
        turn_right_time = getMinDistance1wheel(C[i], right_lock, N) + recursiveMinTime(N, M, C, i + 1, left_lock, C[i], memo)

        memo[(left_lock, right_lock)] = min(turn_left_time, turn_right_time)
        memo[(right_lock, left_lock)] = memo[(left_lock, right_lock)]

    return memo[(left_lock, right_lock)]


def getMinDistance1wheel(pos, target, N):
    return min(abs(target - pos), N - abs(target - pos))


def getMinDistance2wheels(pos, target, N):
    return min(
        getMinDistance1wheel(pos[0], target, N),
        getMinDistance1wheel(pos[1], target, N),
    )


if __name__ == "__main__":
    print(getMinCodeEntryTime(10, 10, [6, 5, 7, 5, 7, 5, 7, 5, 7, 5]))
    # print(getMinCodeEntryTime(10, 4, [9, 4, 4, 8]))
