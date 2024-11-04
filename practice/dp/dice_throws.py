from collections import defaultdict


def diceThrows(numDice, numSides, target):
    # Write your code here.
    # ndice = 2
    # nsides = 6
    # target = 7

    subsolutions = defaultdict(lambda: defaultdict(int))
    for i in range(1, numSides + 1):
        subsolutions[1][i] = 1

    for n in range(2, numDice + 1):
        for v in range(1, target + 1):
            if v <= numSides:
                subsolutions[n][v] = subsolutions[n][v - 1] + subsolutions[n - 1][target - v]
            else:
                subsolutions[n][v] = subsolutions[n][v - 1]

    return subsolutions[numDice][target]


if __name__ == "__main__":
    print(diceThrows(12, 9, 108))
