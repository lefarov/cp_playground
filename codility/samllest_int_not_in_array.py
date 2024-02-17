

def solution(A):
    # write your code in Python 3.6
    a_set = set(A)

    for i in range(1, len(a_set) + 1):
        if i not in a_set:
            return i

    return len(a_set) + 1



if __name__ == "__main__":
    print(f"input {list(range(10))} solution {solution(list(range(10)))}")