from collections import defaultdict
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        task_counts = defaultdict(int)
        for task in tasks:
            task_counts[task] += 1
        
        counts = sorted(list(task_counts.values()), reverse=True)
        space = (counts[0] - 1) * n
        for count in counts[1:]:
            space -= min(count, (counts[0] - 1))
        
        return len(tasks) + max(0, space)


if __name__ == "__main__":
    solution = Solution()
    print(solution.leastInterval(["A","A","A","B","B","B","C","C","C","D","D","E"], 2))