from collections import defaultdict


def maxProfitWithKTransactions(prices, k):
    # Write your code here.
    # [5, 11, 3, 50, 60, 90]
    #
    # k = 2
    subsolutions = defaultdict(lambda: defaultdict(int))

    for prob_size in range(1, k + 1):
        buy_ind = len(prices) - 2 if prob_size % 2 == 0 else 0
        sell_ind = len(prices) - 1 if prob_size % 2 == 0 else 1
        first_ind = buy_ind if prob_size % 2 == 0 else sell_ind
        shift = 1 if prob_size % 2 == 0 else -1
        subsolutions[prob_size][first_ind] = prices[sell_ind] - prices[buy_ind]
        subsolutions[prob_size][first_ind] += get_prev_profit(subsolutions, first_ind, prob_size)

        for i in get_range(buy_ind, sell_ind, prices, prob_size):
            current_price = prices[i]
            subsolutions[prob_size][i] = subsolutions[prob_size][i + shift]

            max_profit, condition_ind = max(
                (current_price - prices[buy_ind] + get_prev_profit(subsolutions, i, prob_size), 0),
                (current_price - prices[i + shift] + get_prev_profit(subsolutions, i, prob_size), 1),
                (subsolutions[prob_size][i], 2)
            )

            if condition_ind == 0:
                subsolutions[prob_size][i] = max_profit
                subsolutions[prob_size][i] += get_prev_profit(subsolutions, i, prob_size)


            elif condition_ind == 1:
                subsolutions[prob_size][i] = max_profit
                subsolutions[prob_size][i] += get_prev_profit(subsolutions, i, prob_size)
                buy_ind = i + shift

    return subsolutions[k][0 if k % 2 == 0 else len(prices) - 1]


def get_range(buy_ind, sell_ind, prices, prob_size):
    if prob_size % 2 == 0:
        yield from range(buy_ind - 1, -1, -1)
    else:
        yield from range(sell_ind + 1, len(prices))


def get_prev_profit(subsolutions, i, prob_size):
    if prob_size % 2 == 0:
        return subsolutions[prob_size - 1][i - 1]
    else:
        return subsolutions[prob_size - 1][i + 1]


if __name__ == "__main__":
    print(maxProfitWithKTransactions([5, 11, 3, 50, 60, 90], 2))
