from heapq import heappop, heappush
from collections import defaultdict


import math
import os
import random
import re
import sys


# Complete the shortestReach function below.
def shortestReach(n, edges, s):
    # graph = defaultdict(list)
    # for u, v, w in edges:
    #     graph[u].append((v, w))
    #     if u not in graph[v]:
    #         graph[v].append((u, w))
    graph = defaultdict(dict)
    for u, v, w in edges:
        if u in graph:
            if v not in graph[u] or w < graph[u][v]:
                graph[u].update({v: w})
        else:
            graph[u].update({v: w})
        
        if v in graph:
            if u not in graph[v] or w < graph[v][u]:
                graph[v].update({u: w})
        else:
            graph[v].update({u: w})

    dist = defaultdict(lambda: float("inf"))
    
    heap = []
    heappush(heap, (0, s))

    while heap and len(dist) < n:
        current_dist, current_node = heappop(heap)
        if current_dist < dist[current_node]:
            dist[current_node] = current_dist
        
        for neighbor_node, neighbor_dist in graph[current_node].items():
            if neighbor_node not in dist:
                heappush(heap, (neighbor_dist + current_dist, neighbor_node))

    return [(dist[i] if dist[i] != float("inf") else -1) for i in range(1, n + 1) if i != s]   


if __name__ == '__main__':

    t = int(input())

    for t_itr in range(t):
        nm = input().split()
        n = int(nm[0])
        m = int(nm[1])

        edges = []
        for _ in range(m):
            edges.append(list(map(int, input().rstrip().split())))

        s = int(input())

        # 1
        # 4 4
        # 1 2 24
        # 1 4 20
        # 1 3 3
        # 3 4 12
        # 1
        print(shortestReach(n, edges, s))
