from collections import defaultdict


def contacts(queries):
    trie = defaultdict(int)
    res = []
    for command, arg in queries:
        if command == "add":
            for i in range(1, len(arg) + 1):
                key = arg[0:i]
                trie[key] += 1
        if command == "find":
            res.append(trie[arg])
    
    return res


if __name__ == "__main__":
    print(contacts([["add", "hack"], ["add", "hackerrank"], ["find", "hac"], ["find", "hak"]]))
