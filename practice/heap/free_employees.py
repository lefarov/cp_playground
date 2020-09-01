from collections import deque


class Solution:
    
    def __init__(self):
        pass

    @staticmethod
    def getCommonFreeInterval(working_hours):
        working_intervals = [
            working_interval
            for employee_workin_hours in working_hours 
            for working_interval in employee_workin_hours]

        working_intervals.sort(key=lambda interval: interval[0])

        interval_stack = deque()
        interval_stack.append(working_intervals[0])

        res = []

        for interval in working_intervals[1:]:
            if interval[0] <= interval_stack[-1][1]:
                last_interval = interval_stack.pop()
                interval_stack.append([last_interval[0], max(last_interval[1], interval[1])])
            else:
                res.append([interval_stack[-1][1], interval[0]])
                interval_stack.append(interval)


        return res


if __name__ == "__main__":
    print(Solution.getCommonFreeInterval([ [[1, 3], [5, 6]], [[2, 3], [6, 8]] ]))
    print(Solution.getCommonFreeInterval([ [[1, 3], [9, 12]], [[2, 4], [6, 8]] ]))
    print(Solution.getCommonFreeInterval([ [[1, 3], [2, 4]], [[3, 5], [7, 9]] ]))
