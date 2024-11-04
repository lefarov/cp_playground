def permutations(elements, k):
    if k == 1:
        return [[e] for e in elements]

    result = []
    for i, el in enumerate(elements):
        for sub_permutation in permutations(elements[:i] + elements[i+1:], k-1):
            result.append([el, *sub_permutation])

    return result


if __name__ == "__main__":
    res = permutations([1, 2, 3], 3)
    print(res)
