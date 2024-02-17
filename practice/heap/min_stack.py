"""
Write a MinStack class. Class should support:
- Pushing and poping values
- Peeking top value
- Getting minimum value in any given poing of time

All classes methods when considered independently, should run in constant time and with constant space.
"""

from collections import deque, defaultdict
from heapq import heappush, heappop


class MinStack:
    
    def __init__(self):
        self._counts = defaultdict(int)
        self._min_heap = []
        self.stack = deque()

    def push(self, value):
        self._counts[value] += 1
        heappush(self._min_heap, value)

        self.stack.append(value)

    def peek(self):
        return self.stack[0]

    def pop(self):
        el = self.stack.pop()
        self._counts[el] = max(0, self._counts[el] - 1)

        return el

    def min(self):
        while not self._counts[self._min_heap[0]]:
            heappop(self._min_heap)

        return self._min_heap[0]


if __name__ == "__main__":
    stack = MinStack()
    stack.push(5)
    print(f"{stack.min()}")
    print(f"{stack.peek()}")
    stack.push(2)
    stack.push(7)
    stack.push(2)
    stack.push(3)
    print(f"{stack.min()}")
    print(f"{stack.pop()}")
    print(f"{stack.pop()}")
    print(f"{stack.min()}")

