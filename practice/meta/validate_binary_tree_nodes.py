import collections
from typing import List


class Solution:
    def validateBinaryTreeNodes(self, n: int, leftChild: List[int], rightChild: List[int]) -> bool:
        roots = set()
        visited = set()

        for root in range(n):
            if root in visited:
                continue

            queue = collections.deque()
            queue.append(root)
            visited.add(root)

            while queue:
                node = queue.popleft()

                left = leftChild[node]
                right = rightChild[node]

                if left >= 0:
                    if self.validate_child(left, visited, roots):
                        queue.append(left)
                        visited.add(left)
                    else:
                        return False

                if right >= 0:
                    if self.validate_child(right, visited, roots):
                        queue.append(right)
                        visited.add(right)
                    else:
                        return False

            roots.add(root)

        return len(roots) == 1
    

    @staticmethod
    def validate_child(child, visited, roots):
        if child in visited:
            if child not in roots:
                return False
            else:
                roots.remove(child)

        return True

        

if __name__ == "__main__":
    print(Solution().validateBinaryTreeNodes(n = 2, leftChild = [1,0], rightChild = [-1,-1]))
    # print(Solution().validateBinaryTreeNodes(n = 6, leftChild = [1,-1,-1,4,-1,-1], rightChild = [2,-1,-1,5,-1,-1]))