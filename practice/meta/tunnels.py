from typing import List


# Write any import statements here

def getSecondsElapsed(C: int, N: int, A: List[int], B: List[int], K: int) -> int:
    # Write your code here
    # ---[**]--[****]-----
    # 10/6 * Sum S_tunnel
    #
    #
    # K // Sum S_tunnel * C / Sum S_tunnel
    # K % Sum S_tunnel
    # -> A

    tunnel_lengths = [end - start for start, end in zip(A, B)]
    tunnel_total = sum(tunnel_lengths)

    num_completed_circles = K // tunnel_total
    total_tunnel_time = num_completed_circles * C

    remaining_tunnel_time = K % tunnel_total
    tunnel_pairs = sorted(zip(A, B))

    accumulated_tunnel_time = 0
    for start, end in tunnel_pairs:
        tunnel_length = end - start
        if remaining_tunnel_time <= accumulated_tunnel_time + tunnel_length:
            total_tunnel_time += start + (remaining_tunnel_time - accumulated_tunnel_time)
            break

        accumulated_tunnel_time += tunnel_length

    return total_tunnel_time


if __name__ == "__main__":
    print(getSecondsElapsed(10, 2, [6, 1], [7, 3], 7))
