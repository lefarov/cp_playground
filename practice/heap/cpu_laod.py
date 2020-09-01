
from collections import deque
from heapq import heappush, heappop


class Job:

    def __init__(self, start, stop, load):
        self.start, self.stop, self.load = start, stop, load
    
    def __lt__(self, other):
        return self.stop < other.stop



class Solution:
    
    def __init__(self):
        pass

    @staticmethod
    def computeMaxLoad(jobs):
        jobs = [Job(*job) for job in jobs]
        jobs.sort(key=lambda job: job.start)
        max_load, current_load = 0.0, 0.0

        min_heap = []

        for job in jobs:

            while len(min_heap) > 0 and job.start >= min_heap[0].stop:
                current_load -= min_heap[0].load
                heappop(min_heap)

            heappush(min_heap, job)
            current_load += job.load
            max_load = max(current_load, max_load)


        return max_load



if __name__ == "__main__":
    print(Solution.computeMaxLoad([[1, 4, 3], [2, 5, 4], [7, 9, 6]]))
