def waterArea(heights):
    # Write your code here.
    # [0, 8, 0, 0, 5, 0, 0, 10, 0, 0, 1, 1, 0, 3]
    # []
    if not heights:
        return 0

    left_pointer, right_pointer = 0, len(heights) - 1
    left_max, right_max = heights[0], heights[-1]
    total_water = 0

    while left_pointer < right_pointer:

        if heights[left_pointer] < heights[right_pointer]:
            total_water += left_max - heights[left_pointer]
            left_pointer += 1
            left_max = max(left_max, heights[left_pointer])

        else:
            total_water += right_max - heights[right_pointer]
            right_pointer -= 1
            right_max = max(right_max, heights[right_pointer])

    return total_water


if __name__ == "__main__":
    waterArea([0, 1, 1, 0, 0])
