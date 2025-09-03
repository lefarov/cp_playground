from typing import List

import collections

class Solution:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        graph = collections.defaultdict(list)
        for i in range(len(bombs)):
            for j in range(len(bombs)):
                if i == j:
                    continue

                b1, b2 = tuple(bombs[i]), tuple(bombs[j])
                dist = (b1[0] - b2[0]) ** 2 + (b1[1] - b2[1]) ** 2
                if dist <= b1[2] ** 2:
                    graph[i].append(j)

        res = 0
        chains = {}
        chain_i = 0
        for i in range(len(bombs)):
            if i in chains:
                continue

            queue = collections.deque([i])
            detonated = {i}
            triggered_chains = set()

            count = 0
            while queue:
                i = queue.popleft()
                count += 1

                for j in graph[i]:
                    if j not in detonated:
                        if j not in chains:
                            queue.append(j)
                            detonated.add(j)
                        elif chains[j][0] not in triggered_chains:
                            count += chains[j][1]
                            triggered_chains.add(chains[j][0])
                            detonated.add(j)

            for di in detonated:
                chains[di] = (chain_i, count)

            chain_i += 1
            res = max(res, count)

        return res
    

if __name__ == "__main__":
    Solution().maximumDetonation(
        [
            [855,82,158],
            [17,719,430],
            [90,756,164],
            [376,17,340],
            [691,636,152],
            [565,776,5],
            [464,154,271],
            [53,361,162],
            [278,609,82],
            [202,927,219],
            [542,865,377],
            [330,402,270],
            [720,199,10],
            [986,697,443],
            [471,296,69],
            [393,81,404],
            [127,405,177]]
    )