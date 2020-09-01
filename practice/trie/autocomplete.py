
class Node:

    def __init__(self, children, is_word):
        self.children, self.is_word = children, is_word


class Solution:
    def __init__(self):
        self.trie = None

    def build(self, words):
        self.trie = Node({}, False)
        for word in words:
            current = self.trie
            for char in word:
                if char not in current.children:
                    current.children[char] = Node({}, False)
                
                current = current.children[char]
            
            current.is_word = True

    def autocomplete(self, words, prefix):
        self.build(words)

        current = self.trie
        for char in prefix:
            if char not in current.children:
                return []

            current = current.children[char]

        return self.DFSFindWords(current, prefix)

    def DFSFindWords(self, node, prefix):
        words = []

        if node.is_word:
            words += [prefix]

        for char in node.children:            
            words += self.DFSFindWords(node.children[char], prefix + char) 

        return words


if __name__ == "__main__":
    print(Solution().autocomplete(["dog", "dark", "cat", "door", "dodge"], "do"))
    pass