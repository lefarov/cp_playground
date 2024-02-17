class Solution:
    def num_items(self, string, start_inds, stop_inds):
        res = [0] * len(start_inds)
        for i, (start, stop) in enumerate(zip(start_inds, stop_inds)):
            count = 0

            # Skip till the first wall
            mostleft_wall = start - 1
            while string[mostleft_wall] != "|":
                mostleft_wall += 1

            # Go over the remaining string
            for symbol in string[mostleft_wall: stop]:
                if symbol == "|":
                    res[i] += count
                    count = 0
                else:
                    count += 1
        
        return res


if __name__ == "__main__":
    solution = Solution()
    print(solution.num_items("|**|*|*", [1, 1, 1], [5, 6, 2]))