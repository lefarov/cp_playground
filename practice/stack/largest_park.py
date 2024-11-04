
from collections import deque


def max_rectangle_in_histogram(heights):
    max_area = 0
    stack = deque()
    for i, height in enumerate(heights):
        while stack and height < heights[stack[-1]]:
            possible_height = heights[stack.pop()]
            possible_width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, possible_width * possible_height)

        stack.append(i)

    while stack:
        possible_height = heights[stack.pop()]
        possible_width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, possible_width * possible_height)

    return max_area


if __name__ == "__main__":
    print(max_rectangle_in_histogram([2, 1, 2]))