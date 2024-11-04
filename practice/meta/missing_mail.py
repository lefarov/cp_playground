from typing import List
from collections import defaultdict

def getMaxExpectedProfitV1(N: int, V: List[int], C: int, S: float) -> float:
    profit = 0
    prev_value = 0
    for i, value in enumerate(V[:-1]):
        value_take = prev_value + value + V[i + 1] - 2 * C
        value_leave = (1 - S) * (prev_value + value) + V[i + 1] - C

        if value_leave >= value_take:
            # leaving room without taking
            prev_value = (1 - S) * (prev_value + value)
        else:
            # take accumulated mail
            profit += (prev_value + value) - C
            prev_value = 0

    if prev_value + V[-1] > C:
        profit += (prev_value + V[-1]) - C

    return profit


def getMaxExpectedProfitV2(N: int, V: List[int], C: int, S: float) -> float:
    return recursive_compute_expected_profit(V, C, S, 0, 0, 0)


def recursive_compute_expected_profit(
    values: List[int],
    cost: int,
    stealing_prob: float,
    day_ind: int,
    profit: float,
    accumulated_value: float
) -> float:
    if day_ind == len(values) - 1:
        return profit + max(accumulated_value + values[day_ind] - cost, 0)

    value = max(
        # entering the room
        recursive_compute_expected_profit(
            values,
            cost,
            stealing_prob,
            day_ind + 1,
            profit + accumulated_value + values[day_ind] - cost,
            0
        ),
        # not entering room
        recursive_compute_expected_profit(
            values,
            cost,
            stealing_prob,
            day_ind + 1,
            profit,
            (accumulated_value + values[day_ind]) * (1 - stealing_prob)
        )
    )

    return value


def getMaxExpectedProfitV3(N: int, V: List[int], C: int, S: float) -> float:
    # [num_days, values] -> pairs of (realized profit, expected value)
    subproblems_profit = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))

    expected_value = 0.0
    for i, value in enumerate(V):
        subproblems_profit[1][i + 1][0] = expected_value + value - C
        subproblems_profit[1][i + 1][1] = 0.0
        expected_value = (1-S)*(expected_value + value)

    for day_i in range(2, N + 5):
        for i, value in enumerate(V):
            # if we enter the room -> we are adding maximal profit of solving subtask with n-1 days
            # and realize all remaining profit
            profit_enter = value - C + sum(subproblems_profit[day_i - 1][i])
            expected_value_enter = 0.0

            # if we don't enter -> we are adding maximal profit of solving subtask with n days
            # but do not realize all remaining profit
            profit_skip = subproblems_profit[day_i][i][0]
            expected_value_profit = (1-S)*(subproblems_profit[day_i][i][1] + value)

            if profit_enter > profit_skip:
                subproblems_profit[day_i][i+1] = [profit_enter, expected_value_enter]
            else:
                subproblems_profit[day_i][i+1] = [profit_skip, expected_value_profit]


    return None


def getMaxExpectedProfitV4(N: int, V: List[int], C: int, S: float) -> float:
    dp = [0] * (N + 1)
    V = [0] + V
    for i in range(1, N + 1):
        v, s = 0, 1
        dp[i] = -float('inf')
        for j in range(i - 1, -1, -1):
            dp[i] = max(dp[i], dp[j] + V[i] + v - C)
            s *= 1 - S
            v += V[j] * s

    return max(dp)


if __name__ == "__main__":
    print(getMaxExpectedProfitV4(5, [10, 2, 8, 6, 4], 5, 0.0))