class Solution:
    def maxJumps(self, arr, d: int) -> int:
        max_jumps_mem = [1] * len(arr)

        def _window_search(i):
            max_jumps = max_jumps_mem[i]

            offset = 1
            next_i = i + offset
            while next_i < len(arr) and offset <= d and arr[i] > arr[next_i]:
                max_jumps = max(max_jumps, max_jumps_mem[next_i] + 1)

                offset += 1
                next_i = i + offset

            offset = -1
            prev_i = i + offset
            while prev_i >= 0 and offset <= d and arr[i] > arr[prev_i]:
                max_jumps = max(max_jumps, max_jumps_mem[prev_i] + 1)

                offset -= 1
                prev_i = i + offset

            max_jumps_mem[i] = max_jumps

        for i, height in enumerate(arr):
            # window search
            _window_search(i)
            for j in range(i - 1, -1, -1):
                _window_search(j)

        return max(max_jumps_mem)


if __name__ == "__main__":
    Solution().maxJumps([40,98,14,22,45,71,20,19,26,9,29,64,76,66,32,79,14,83,62,39,69,25,92,79,70,34,22,19,41,26,5,82,38], 6)
