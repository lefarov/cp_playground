
from typing import List
from collections import defaultdict


def max_value(values: List[int], weights: List[int], capacity: int):
    # DP memory for storing partial solutions.
    memory = defaultdict(lambda: defaultdict(int))
    # Min weight
    mw = min(weights)

    # Iterate over the "packages" subproblems.
    for i, (value, weight) in enumerate(zip(values, weights)):
        
        # Iterate over the "capacity" subproblmes.
        for capa in range(mw, capacity + mw, mw):
            
            # If current item doesn't fit into the current capacity
            if capa < weight:
                # Leave it and use the result of a subproblme with the same capacity
                # and item set / current item
                memory[i][capa] = memory[i - 1][capa]
            
            else:
                # Choose the maximum between two options:
                # 1. Put current item into the backpack and add its value to the result of a 
                #    subproblem with capacity - item's weight and items set / current item.
                # 2. Leave current item and take the result of a subproblem with the same capacity
                #    and item set / current item
                memory[i][capa] = max(
                    value + memory[i - 1][capa - weight],  # Put item into backpack
                    memory[i - 1][capa],  # Leave item
                )

    return memory[len(values) - 1][capacity]
            


if __name__ == "__main__":
    print(max_value([60, 120, 100], [10, 20, 30], 50))