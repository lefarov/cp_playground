
from collections import defaultdict


def fourNumberSum(array, targetSum):
    result = []

    sum_index = defaultdict(list)
    for i, item1 in enumerate(array):
        for item2 in array[i + 1:]:
            sum_index[item1 + item2].append([item1, item2])

    for sum, pairs in sum_index.items():
        for pair1 in pairs:
            for pair2 in sum_index[targetSum - sum]:
                concatenation = pair1 + pair2
                if len(set(concatenation)) == 4:
                    result.append(concatenation)

        sum_index[targetSum - sum] = []

    return result


if __name__ == "__main__":
    print(fourNumberSum([7, 6, 4, -1, 1, 2], 16))
