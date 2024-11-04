import collections

def dailyTemperatures(temperatures):
    stack = collections.deque()

    res = [0] * len(temperatures)
    for i, temp in enumerate(temperatures):
        while stack and temp > stack[-1][1]:
            prev_i, prev_temp = stack.pop()
            res[prev_i] = i - prev_i

        stack.append((i, temp))

    return res


if __name__ == '__main__':
    print(dailyTemperatures([73,74,75,71,69,72,76,73]))
