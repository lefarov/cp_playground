from typing import List


class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        result, trie = 0, {}
        length = max(nums).bit_length()

        for num in nums:
            curr = opposite = trie
            for digit in map(int, f'{num:b}'.zfill(length)):
                curr = curr.setdefault(digit, {})
                opposite = opposite.get(1 - digit) or opposite.get(digit)
            
            curr['$'] = num
            result = max(result, opposite['$'] ^ num)
        
        return result


if __name__ == "__main__":
    print(Solution().findMaximumXOR([3, 10, 5, 25, 2, 8]))