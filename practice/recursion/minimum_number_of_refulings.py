from typing import List
import functools

class Solution:
    def minRefuelStops(self, target: int, startFuel: int, stations: List[List[int]]) -> int:

        self.res = float("inf")

        @functools.cache
        def _recursive_search(fuel, pos, si):
            if fuel >= target - pos:
                return 0

            # can't make it to the next station
            res = float("inf")
            if si == len(stations) or fuel < stations[si][0] - pos:
                return res

            diff = stations[si][0] - pos
            res = min(res,
                      _recursive_search(
                          fuel - diff,
                          stations[si][0],
                          si + 1,
                      )
                      )

            res = min(res,
                      _recursive_search(
                          fuel - diff + stations[si][1],
                          stations[si][0],
                          si + 1,
                      ) + 1
                      )

            return res

        res = _recursive_search(startFuel, 0, 0)

        return self.res if self.res < float("inf") else -1


if __name__ == "__main__":
    print(Solution().minRefuelStops(100, 25, [[25,25],[50,25],[75,25]]))
