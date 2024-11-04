import collections


def calculate(s: str) -> int:
    result, current = 0, 0
    sign = 1

    comp_stack = collections.deque()

    for char in s:
        if char.isdigit():
            current = current * 10 + int(char)

        elif char == "+":
            result += sign * current
            sign = 1
            current = 0
        elif char == "-":
            result += sign * current
            sign = -1
            current = 0

        elif char == "(":
            comp_stack.append((result, sign))
            result, current = 0, 0
            sign = 1

        elif char == ")":
            prev_result, prev_sign = comp_stack.pop()
            result = prev_result + prev_sign * (result + sign * current)
            current = 0
            sign = 1

        else:
            # whitespace
            result += sign * current
            current = 0

    return result + sign * current


if __name__ == "__main__":
    print(calculate(" 2-1 + 2 "))
