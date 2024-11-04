class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        # Write your code here.
        # Do not edit the return statement of this method.
        if value < self.value:
            if self.left is None:
                self.left = BST(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = BST(value)
            else:
                self.right.insert(value)

        return self

    def contains(self, value):
        # Write your code here.
        if value == self.value:
            return True

        if value < self.value and self.left is not None:
            return self.left.contains(value)

        if value > self.value and self.right is not None:
            return self.right.contains(value)

        return False

    def remove(self, value):
        # Write your code here.
        # Do not edit the return statement of this method.

        if value == self.value:
            if self.left is None and self.right is None:
                return None

            elif self.left is None:
                self.swap_node = self.right
                self.value = self.swap_node.value
                self.right = self.swap_node.right
                self.left = self.swap_node.left

            elif self.right is None:
                self.swap_node = self.left
                self.value = self.swap_node.value
                self.right = self.swap_node.right
                self.left = self.swap_node.left

            else:
                right_leaf = self.get_most_right_leaf(self.right)
                self.value = right_leaf.value
                self.right = self.right.remove(self.value)

        elif value < self.value and self.left is not None:
            self.left = self.left.remove(value)

        elif value > self.value and self.right is not None:
            self.right = self.right.remove(value)

        return self

    @staticmethod
    def get_most_right_leaf(node):
        if node.left is None:
            return node
        else:
            return BST.get_most_right_leaf(node.left)


if __name__ == "__main__":
    tree = BST(1)
    tree.insert(-2)
    tree.insert(-3)
    tree.insert(-4)
    tree.remove(1)

    pass
