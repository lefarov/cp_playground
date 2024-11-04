from typing import List
from collections import defaultdict, deque

def getSecondsRequired(R: int, C: int, G: List[List[str]]) -> int:
    portals = defaultdict(list)
    start = None
    for i, row in enumerate(G):
        for j, square in enumerate(row):
            if square == "S":
                start = (i, j)
            elif square.islower():
                portals[square].append((i, j))

    visited_squares = set()
    visited_portals = set()
    queue = deque()
    queue.append((start, 0))

    while queue:
        (ci, cj), path = queue.popleft()
        if (ci, cj) in visited_squares:
            continue

        visited_squares.add((ci, cj))

        if G[ci][cj] == "E":
            return path

        # Check all 4 directions
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = ci + di, cj + dj
            if 0 <= ni < R and 0 <= nj < C and G[ni][nj] != "#" and (ni, nj) not in visited_squares:
                queue.append(((ni, nj), path + 1))

        # Check portals
        if G[ci][cj].islower() and G[ci][cj] not in visited_portals:
            visited_portals.add(G[ci][cj])
            for pi, pj in portals[G[ci][cj]]:
                if (pi, pj) not in visited_squares:
                    queue.append(((pi, pj), path + 1))

    return -1

if __name__ == "__main__":
    print(getSecondsRequired(3, 4, [["a", "S", ".", "b"], ["#", "#", "#", "#"], ["E", "b", ".", "a"]]))
