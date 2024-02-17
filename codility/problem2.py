
from collections import deque
from heapq import heapify, heappush, heappop


def solution(A, X, Y, Z):
    # write your code in Python 3.6
    # Occupancy and capacity arrays. Occupancy is defined as followes
    # <= 0: free, > 0: number of seconds until free
    occupancy = [0, 0, 0]
    capacity = [X, Y, Z]

    max_wait_time = 0

    # Car queue
    fuel_queue = deque(A)
    time = 0

    while fuel_queue:
        # Step 1: check if we're in deadlock situation
        if (
            all([tank == 0 for tank in occupancy]) and 
            all([capa < fuel_queue[0] for capa in capacity])
        ):
            return -1

        # Step 2: check if first car can start refueling
        for i in range(len(occupancy)):
            if occupancy[i] <= 0 and fuel_queue and capacity[i] >= fuel_queue[0]:
                # Take first car from the queue
                current_car = fuel_queue.popleft()
                # Update occupancy and capacity
                occupancy[i] = current_car
                capacity[i] -= current_car
                # Check if car waiting time for the car was the maximum so fat
                max_wait_time = max(max_wait_time, time)
            
        # Step 3: step forward in time and decrease occupancy
        time_delta = min([oc for oc in occupancy if oc > 0])
        time += time_delta
        for i in range(len(occupancy)):
            occupancy[i] -= time_delta

    return max_wait_time


if __name__ == "__main__":
    # print(solution([2, 8, 4, 3, 2], 7, 11, 3))
    print(solution([5], 4, 0, 3))