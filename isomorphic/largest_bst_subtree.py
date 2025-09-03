
class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


#           10
#      5           15
#  1     8              7


class Solution:
    def max_sub_bst(self, root):
        self.result = None
        self.max_size = 0

        def _dfs(node):
            
            min_val = node.val
            max_val = node.val

            min_val_l, max_val_l, num_l = float("inf"), float("-inf"), 0
            if node.left:
                min_val_l, max_val_l, num_l = _dfs(node.left)
                min_val = min(min_val_l, min_val)  # 1
                max_val = max(max_val_l, max_val)  # 8
            
            min_val_r, max_val_r, num_r = float("inf"), float("-inf"), 0
            if node.right:
                min_val_r, max_val_r, num_r = _dfs(node.right)
                min_val = min(min_val_r, min_val)  # 1
                max_val = max(max_val_r, max_val)  # 8

            total_num = num_l + 1 + num_r
            if max_val_l < node.val < min_val_r:
                if total_num > self.max_size:
                    self.max_size = total_num
                    self.result = node


            return min_val, max_val, total_num
    

        _dfs(root)
        
        return(self.result)