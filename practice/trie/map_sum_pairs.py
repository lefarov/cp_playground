class MapSum:

    def __init__(self):
        self.trie = {}

    def insert(self, key: str, val: int) -> None:
        head = self.trie
        for ch in key:
            head.setdefault(ch, {})
            head = head[ch]

        head["$"] = val

    def sum(self, prefix: str) -> int:
        # skip through prefix:
        head = self.trie
        for ch in prefix:
            if ch not in head:
                return 0
            head = head[ch]

        # do dfs and accumulate
        return self.recursiveSumInTrie(head)

    def recursiveSumInTrie(self, head):
        current_sum = 0
        for key, next_head in head.items():
            if key == "$":
                current_sum += next_head
            else:
                current_sum += self.recursiveSumInTrie(next_head)

        return current_sum


if __name__ == "__main__":
    map = MapSum()
    map.insert("apple",3)
    map.sum("ap")
    map.insert("app", 2)
    print(map.sum("ap"))