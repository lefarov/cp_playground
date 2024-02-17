from heapq import heappush, heappop, heapify

class Solution:

    @staticmethod
    def connectRopes(ropes):
        ropes_heap = ropes.copy()
        heapify(ropes_heap)
        
        cost = 0
        while True:
            print(ropes_heap)
            first_rope = heappop(ropes_heap)

            if ropes_heap:
                second_rope = heappop(ropes_heap)
                cost += first_rope + second_rope
                heappush(ropes_heap, first_rope + second_rope)
            else:
                return cost


if __name__ == "__main__":
    print(Solution.connectRopes([1, 2, 5, 10, 35, 89]))
