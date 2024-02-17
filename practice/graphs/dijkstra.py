from heapq import heappop, heappush
from collections import defaultdict


import math
import os
import random
import re
import sys


def shortestReach(n, edges, s):
    # Construct the graph representation
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  # If graph is bideractional

    # Dijkstra
    heap = []
    heappush(heap, (0, s))
    dist = defaultdict(lambda: float("inf"))

    # Here additional stop should be implemented
    while heap:
        current_dist, current_node = heappop(heap)
        # Make sure that leftovers from the Heap are not overwriting the results
        if current_dist < dist[current_node]:
            dist[current_node] = current_dist
        
        for neighbor_node, neighbor_dist in graph[current_node]:
            # Do not go back to the nodes you've already considered
            if neighbor_node not in dist:
                heappush(heap, (neighbor_dist + current_dist, neighbor_node))

    return dist   


if __name__ == '__main__':
    """
    Test Inputs
    -----------
    1
    4 4
    1 2 24
    1 4 10
    1 3 3
    3 4 12
    1

    """

    t = int(input())

    for t_itr in range(t):
        nm = input().split()
        n = int(nm[0])
        m = int(nm[1])

        edges = []
        for _ in range(m):
            edges.append(list(map(int, input().rstrip().split())))

        s = int(input())

        print(shortestReach(n, edges, s))
