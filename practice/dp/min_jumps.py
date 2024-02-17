class Solution:

    def get_min_jumps(self, jumps_array):
        min_jumps = [int(10e6)] * len(jumps_array)
        min_jumps[-1] = 0
        
        # Iterate over elements in reverse order starting from the pre-last elemnet
        for i, jumps in reversed(list(enumerate(jumps_array[:-1]))):
            
            # If 0 jumps are available
            if not jumps:
                # Go to the next iteration
                continue
            
            # If we can jump to the end from this point
            elif jumps >= len(jumps_array[i:]):
                min_jumps[i] = 1

            # Else
            else :
                # Find a spot with minimum jumps within the range
                min_jumps[i] = min(min_jumps[i:(i + jumps + 1)]) + 1

        return min_jumps[0]


if __name__ == "__main__":
    solution = Solution()
    print(solution.get_min_jumps([1, 1, 3, 6, 9, 3, 0, 1, 3]))