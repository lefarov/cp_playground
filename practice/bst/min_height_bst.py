def minHeightBst(array):
    i = len(array) // 2
    tree = BST(array[i])

    recursiveConstructBst(tree, array[:i])
    recursiveConstructBst(tree, array[i+1:])

    return tree


def recursiveConstructBst(tree, array):
    if not array:
        return

    i = len(array) // 2
    tree.insert(array[i])

    recursiveConstructBst(tree, array[:i])
    recursiveConstructBst(tree, array[i + 1:])


class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
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


if __name__ == "__main__":
    minHeightBst([1, 2, 5, 7, 10, 13, 14, 15, 22])
