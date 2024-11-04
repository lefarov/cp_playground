from typing import List
# Write any import statements here
from collections import defaultdict, Counter

def getMaxCollectableCoins(R: int, C: int, G: List[List[str]]) -> int:
    # Write your code here
    subsolutions = defaultdict(int)

    for inverse_ind, row in enumerate(G[::-1]):
        ind = R - inverse_ind - 1

        row_chars = Counter(row)
        max_coins_between_turns = getNumCoinsBetweenTurns(row, C)

        coins_enter, coins_skip = 0, 0
        if row_chars[">"] > 0:
            if row_chars["v"] > 0:
                coins_enter = subsolutions[ind + 1] + max_coins_between_turns
            else:
                coins_enter = row_chars["*"]

        if row_chars["."] > 0 or row_chars["*"] > 0:
            coins_skip = subsolutions[ind + 1] + 1 if row_chars["*"] > 0 else 0

        subsolutions[ind] = max(coins_skip, coins_enter)

    return subsolutions[0]


def getNumCoinsBetweenTurns(row, C):
    i, j = 0, 0
    max_coins = 0
    while i < C:
        if row[i] == ">":
            coins = 0
            j = (i + 1) % C
            while row[j] != "v" and j != i:
                if row[j] == "*":
                    coins += 1

                j = (j + 1) % C

            if row[j] == "v":
                max_coins = max(coins, max_coins)

            if j > i:
                i = j + 1
                continue
            else:
                break

        i += 1

    return max_coins


if __name__ == "__main__":
    # print(getMaxCollectableCoins(2, 4, [[".", ">", "v", "*"], [">", "*", ".", "*"]]))
    # print(getMaxCollectableCoins(3, 3, [[">", "*", "*"], ["*", ">", "*"], ["*", "*", ">",]]))
    # print(getMaxCollectableCoins(2, 2, [[">", ">"], ["*", "*"]]))
    # print(getMaxCollectableCoins(3, 4, [[".", "*", "*", "*"], ["*", "*", "v", ">"], [".", "*", ".", "."]]))

    # print(getNumCoinsBetweenTurns(["*", "v", "*", "v", ">", "*"], 6))
    print(getNumCoinsBetweenTurns(["*", ">", "*", ">", ">", ">"], 6))
