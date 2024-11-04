from collections import OrderedDict


def totalFruit(fruits):
    # find the longest subarray with at most 2 unique numbers
    # [3,3,3,1,2,1,1,2,3,3,4]
    # [                .   .]

    baskets = OrderedDict()
    maximum_amount = 0

    left_border = 0
    for right_border, fruit in enumerate(fruits):
        if fruit not in baskets:
            if len(baskets) == 2:
                # move the left_border until we remove all fruits of first type
                removed_fruit, amount = baskets.popitem(last=False)
                while amount > 0:
                    if fruits[left_border] == removed_fruit:
                        amount -= 1
                    else:
                        baskets[fruits[left_border]] -= 1

                    left_border += 1

            baskets[fruit] = 1
        else:
            baskets[fruit] += 1

        maximum_amount = max(maximum_amount, sum(baskets.values()))

    return maximum_amount


if __name__ == "__main__":
    print(totalFruit([1,0,1,4,1,4,1,2,3]))
