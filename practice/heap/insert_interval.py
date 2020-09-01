from collections import deque

class Solution:

    def __init__(self):
        pass

    @staticmethod
    def insertInterval(intervals, interval_to_insert):
        interval_stack = deque()
        
        # go until the correct insertion point
        for i, interval in enumerate(intervals):
            if interval_to_insert[0] <= interval[1]:
                interval_stack.append([
                    min(interval[0], interval_to_insert[0]), 
                    max(interval[1], interval_to_insert[1])])
                break
            else:
                interval_stack.append(interval)

        # continue merging with the rest of the list
        for interval in intervals[i + 1:]:
            if interval[0] <= interval_stack[-1][1]:
                last_interval = interval_stack.pop()
                interval_stack.append([last_interval[0], max(interval[1], last_interval[1])])

            else:
                interval_stack.append(interval)

        return interval_stack


if __name__ == "__main__":
    print(Solution.insertInterval([ [1, 3], [5, 7], [8, 12] ], [4, 6]))
    print(Solution.insertInterval([ [1, 3], [5, 7], [8, 12] ], [4, 10]))
    print(Solution.insertInterval([ [2, 3], [5, 7] ], [1, 4]))
