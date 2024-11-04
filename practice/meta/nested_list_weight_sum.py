def flatten_list(l, level):
    for item in l:
        if isinstance(item, list):
            yield from flatten_list(item, level + 1)
        else:
            yield item * level


if __name__ == "__main__":
    print(sum(flatten_list([[1, 1], 2, [1, 1]], 1)))
