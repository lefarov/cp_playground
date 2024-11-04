import functools


def ambiguousMeasurements(measuringCups, low, high):
    # Write your code here.

    @functools.lru_cache(maxsize=None)
    def _recursive_search(current_low, current_high, cup_idx):
        if cup_idx >= 0:
            cup_low, cup_high = measuringCups[cup_idx]
            if cup_low <= current_low <= current_high <= cup_high:
                return True
        else:
            cup_low, cup_high = 0, 0

        if current_low <= current_high < 0:
            return False

        can_measure = False
        for i in range(len(measuringCups)):
            can_measure = can_measure or _recursive_search(
                current_low - cup_low, current_high - cup_high, i
            )

        return can_measure

    return _recursive_search(low, high, -1)


if __name__ == "__main__":
    print(ambiguousMeasurements([[200, 210],[450, 465],[800, 850]], 2100, 2300))
