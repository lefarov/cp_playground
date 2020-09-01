from collections import deque
from heapq import heappush, heappop


class Meeting:

    def __init__(self, start, stop):
        self.start, self.stop = start, stop
    
    def __lt__(self, other):
        return self.stop < other.stop



class Solution:
    
    def __init__(self):
        pass

    @staticmethod
    def computeMaxLoad(meetings):
        meetings = [Meeting(*meeting) for meeting in meetings]
        meetings.sort(key=lambda meeting: meeting.start)
        max_n_rooms, current_n_rooms = 0, 0
        min_heap = []

        for meeting in meetings:

            while len(min_heap) > 0 and meeting.start >= min_heap[0].stop:
                current_n_rooms -= 1
                heappop(min_heap)

            heappush(min_heap, meeting)
            current_n_rooms += 1
            max_n_rooms = max(current_n_rooms, max_n_rooms)


        return max_n_rooms



if __name__ == "__main__":
    print(Solution.computeMaxLoad([[1, 4], [2, 5], [7, 9], [10, 11], [8, 10], [8, 10]]))