import heapq


class Solution:

    def __init__(self):
        pass
    
    @staticmethod
    def runningMedian(stream):
        res = []
        lower_heap = []
        upper_heap = []

        for i in stream:
            # push to the lower heap
            if not len(lower_heap) or i < - lower_heap[0]:
                heapq.heappush(lower_heap, - i)
            
            # push to the upper heap
            else:
                heapq.heappush(upper_heap, i)

            # rebalance heaps
            if len(lower_heap) > len(upper_heap) + 1:
                heapq.heappush(upper_heap, - heapq.heappop(lower_heap))
            elif len(upper_heap) > len(lower_heap) + 1:
                heapq.heappush(lower_heap, - heapq.heappop(upper_heap))
            
            # computer current median
            if (len(upper_heap) + len(lower_heap)) & 1:
                # pick from the biggest heap
                if len(upper_heap) > len(lower_heap):
                    res.append(upper_heap[0])
                else:
                    res.append(- lower_heap[0])
            else:
                # calulate the mean between two heads
                res.append((upper_heap[0] - lower_heap[0]) / 2)

        return res


if __name__ == "__main__":
    print(Solution.runningMedian([12, 4, 5, 3, 8, 7]))
