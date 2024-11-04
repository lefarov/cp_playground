class MinHeap:
    def __init__(self, array):
        # Do not edit the line below.
        self.heap = self.buildHeap(array)

    def buildHeap(self, array):
        # Write your code here.
        for i in range(len(array) - 1, -1, -2):
            parent_i = int((i - 1) / 2)
            if parent_i >= 0:
                self.siftDown(array, parent_i)
            else:
                break

        return array

    def siftDown(self, array, i):
        # Write your code here.
        parent_i = i

        while True:
            lchild_i = 2 * parent_i + 1
            rchild_i = 2 * parent_i + 2

            min_child, min_child_i = min(
                (float("inf") if lchild_i >= len(array) else array[lchild_i], lchild_i),
                (float("inf") if rchild_i >= len(array) else array[rchild_i], rchild_i),
            )

            if array[parent_i] > min_child < float("inf"):
                array[parent_i], array[min_child_i] = array[min_child_i], array[parent_i]
                parent_i = min_child_i
            else:
                break

    def siftUp(self, array, i):
        # Write your code here.
        child_i = i

        while True:
            parent_i = (child_i - 1) // 2

            if parent_i >= 0 and array[parent_i] > array[child_i]:
                array[parent_i], array[child_i] = array[child_i], array[parent_i]
                child_i = parent_i
            else:
                break

    def peek(self):
        # Write your code here.
        return self.heap[0]

    def remove(self):
        # Write your code here.
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        removed_val = self.heap.pop(-1)
        self.siftDown(self.heap, 0)
        return removed_val

    def insert(self, value):
        # Write your code here.
        self.heap.append(value)
        self.siftUp(self.heap, len(self.heap) - 1)


if __name__ == "__main__":
    heap = MinHeap([48, 12, 24, 7, 8, -5, 24, 391, 24, 56, 2, 6, 8, 41])
    heap.insert(76)
    heap.peek()
