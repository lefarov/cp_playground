import heapq
import collections
from typing import List

class Solution():
    
    def earliest_ts_of_distpoia(self, logs: List[List[int]], n: int):
        graph = collections.defaultdict(list)
        for ts, source, dest in logs:
            graph[source].append((ts, dest))
            graph[dest].append((ts, source))


        ffriend = next(iter(graph.keys()))
        heap = [(0, ffriend)]

        acquinted = set()
        max_ts = 0
        while heap:
            ts, person = heapq.heappop(heap)
            if person in acquinted:
                continue

            acquinted.add(person)
            max_ts = max(ts, max_ts)

            for meeting_ts, friend in graph[person]:
                if friend not in acquinted:
                    heapq.heappush(heap, (max(max_ts, meeting_ts), friend))

        return -1 if len(acquinted) < n else max_ts


if __name__ == "__main__":
    Solution().earliest_ts_of_distpoia(
        [
            [2, "a", "c"],
            [30, "a", "b"],
            [11, "c", "d"],
            # [1, "c", "e"],
            [10, "e", "f"],
            [2, "e", "b"],
        ],
        6
    )