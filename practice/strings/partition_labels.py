from collections import deque
from typing import List


class Solution:
    def partitionLabels(self, S: str) -> List[int]:
        # Deque will hold current partitions of a form (set({letters}), length)
        partitions = []
        # partitions_stack.append((set(S[0]), 1))
        
        # Iterate over the string characters
        for i, ch in enumerate(S):
            in_partition = False
            # Go over partitions in reverse
            for pi in range(len(partitions) - 1, -1, -1):
                if ch in partitions[pi][0]:
                    # Join everything to the right in one partition
                    joined_set = set()
                    for partition in partitions[pi:]:
                        joined_set.update(partition[0])

                    partitions = partitions[:pi] + [(joined_set, partitions[pi][1], i + 1)]
                    in_partition = True
                    break
            
            if not in_partition:
                partitions.append((set(ch), i, i + 1))

        return list(map(lambda p: p[2] - p[1], partitions))


if __name__ == "__main__":
    print(Solution().partitionLabels("ababcbacadefegdehijhklij"))