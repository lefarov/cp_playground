def twoColorable(edges):
    # Write your code here.
    # *---*---*---*
    #  \
    #    \
    # *---*
    # [[1, 3], [0], [3], [1, 2]]
    # if not colored, go to all adjacent vertices and color them in oposit color
    # -> if you ever face t

    # *---*
    #  \ /
    #   *
    # [[1, 2], [0, 2], [1, 0]]

    colors = {}

    for starting_i, neighbors in enumerate(edges):
        color = colors.get(starting_i, 0)
        neighbor_color = (color + 1) % 2

        for neighbor_i in neighbors:
            if neighbor_i == starting_i:
                return False

            if neighbor_i not in colors:
                colors[neighbor_i] = neighbor_color
            elif neighbor_color != colors[neighbor_i]:
                return False

    return True


if __name__ == "__main__":
    print(twoColorable([[0]]))
