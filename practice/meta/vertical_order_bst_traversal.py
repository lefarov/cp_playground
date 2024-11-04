import collections
import heapq


class RowVal:

    def __init__(self, row, val):
        self.row = row
        self.val = val

    def __repr__(self):
        return f"row: {self.row}, val: {self.val}"

    def __lt__(self, other):
        print(other)
        if self.row == other.row:
            print("I'm here")
            return self.val < other.val

        return self.row < other.row


if __name__ == "__main__":
    coords = collections.defaultdict(list)
    heapq.heappush(coords[0], RowVal(0, 0))
    heapq.heappush(coords[0], RowVal(2, 6))
    heapq.heappush(coords[0], RowVal(2, 5))

    pass
