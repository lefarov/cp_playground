from heapq import heapify, heappop, heappush


class Solution:

    def __init__(self):
        pass
    
    @staticmethod
    def getMaximalProfit(seats, n):
        neg_seats = [-seat for seat in seats]
        heapify(neg_seats)
        res = 0
        for _ in range(n):
            n_seats = heappop(neg_seats)
            res -= n_seats
            if n_seats != 0:
                heappush(neg_seats, n_seats + 1)

        return res


if __name__ == "__main__":
    print(Solution.getMaximalProfit([2, 1, 1], 3))
    print(Solution.getMaximalProfit([2, 3, 4, 5, 1], 6))
