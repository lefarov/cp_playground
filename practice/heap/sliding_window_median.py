import collections
import heapq
from typing import List


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        removed_elements = collections.defaultdict(int)
        max_heap = []
        min_heap = []
        res = []

        for i in range(k):
            heapq.heappush(max_heap, -nums[i])
            heapq.heappush(min_heap, -heapq.heappop(max_heap))

            if len(min_heap) > len(max_heap):
                heapq.heappush(max_heap, -heapq.heappop(min_heap))

        def _median():
            return (max_heap[0] + min_heap[0]) / 2 if k % 2 == 0 else -max_heap[0]

        for i in range(k, len(nums)):
            added = nums[i]
            removed = nums[i - k]
            removed_elements[removed] += 1

            balance = -1 if removed <= _median() else 1

            if added <= _median():
                balance += 1
                heapq.heappush(max_heap, -added)
            else:
                balance -= 1
                heapq.heappush(min_heap, added)

            if balance > 0:
                heapq.heappush(min_heap, -heapq.heappop(max_heap))

            if balance < 0:
                heapq.heappush(max_heap, -heapq.heappop(min_heap))

            while max_heap and removed_elements[-max_heap[0]] > 0:
                removed_elements[-max_heap[0]] -= 1
                heapq.heappop(max_heap)

            while min_heap and removed_elements[min_heap[0]] > 0:
                removed_elements[min_heap[0]] -= 1
                heapq.heappop(min_heap)

            res.append(_median())

        return res


if __name__ == "__main__":
    print(Solution().medianSlidingWindow([1,2,3,4,2,3,1,4,2], 3))
