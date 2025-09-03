import heapq
import collections

from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = collections.defaultdict(list)
        for dep, dest in sorted(tickets, reverse=True):
            graph[dep].append(dest)

        itinerary = []
        def _dfs(airport):
            while graph[airport]:
                dest = graph[airport].pop()
                _dfs(dest)

            itinerary.append(airport)

        _dfs("JFK")

        return reversed(itinerary)
    
    def findItineraryDijkstra(self, tickets: List[List[str]]) -> List[str]:
        graph = collections.defaultdict(list)
        for dep, dest in tickets:
            graph[dep].append(dest)

        itinerary = []
        heap = ["JFK"]
        while heap:
            airport = heapq.heappop()
            while graph[airport]:
                dest = graph[airport].pop()
                heapq.heappush(heap, dest)
            
            itinerary.append(airport)

        return reversed(itinerary)

    

if __name__ == "__main__":
    print(Solution().findItinerary([["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]))