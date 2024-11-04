import collections


def add_bold_tag(str, words):
    trie = build_trie(words)
    bold_inds_stack = collections.deque()

    for i, _ in enumerate(str):
        curr = trie
        j = i
        while j < len(str) and str[j] in curr:
            curr = curr[str[j]]
            j += 1

        if "#" in curr:
            start = i
            end = j
            if bold_inds_stack and bold_inds_stack[-1][1] >= start:
                start, _ = bold_inds_stack.pop()

            bold_inds_stack.append([start, end])

    res = ""
    prev_end = 0
    for start, end in bold_inds_stack:
        res += str[prev_end: start] + "<b>" + str[start: end] + "</b>"
        prev_end = end

    res += str[prev_end:]

    return res


def build_trie(words):
    trie = {}
    for word in words:
        curr = trie
        for ch in word:
            curr.setdefault(ch, {})
            curr = curr[ch]

        curr["#"] = 1

    return trie


if __name__ == "__main__":
    print(add_bold_tag("aaabb", ["aa", "b"]))
