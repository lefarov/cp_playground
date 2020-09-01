from typing import List


class Node:
    
    def __init__(self, childrens, word_i):
        self.childrens = childrens
        self.word_i = word_i

class Solution:
    
    def __init__(self):
        self.trie = Node({}, None)
    
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        self._buildTrie(words)
        res = []
        for j, word in enumerate(words):
            res += self._findMatchingPairs(word[::-1], j)

        return res
    
    def _findMatchingPairs(self, word, word_i):
        # query words is reversed
        pairs = []
        current = self.trie
        
        # traverse the reversed query word 
        for i, char in enumerate(word):
            # query word's postfix is equal to one of the words 
            # and the rest of the query word is polindrom
            if current.word_i is not None and self._isPolindrome(word[i:]):
                pairs.append([current.word_i, word_i])

            # next char of the query word is not in the Trie
            if char not in current.childrens:
                return pairs

            current = current.childrens[char]

        # query word is the complete inverse of one of the words
        # and its not the same word (may happen in case of polindromic words)
        if current.word_i is not None and current.word_i != word_i:
            pairs.append([current.word_i, word_i])

        # query word is the postfix of one of the words
        if current.childrens:
            autocompleted_words = self._DFSSearchWord(current, "")
            # and the rest of the word is polindrome
            for autocompleted_word, i in autocompleted_words:
                if self._isPolindrome(autocompleted_word):
                    pairs.append([i, word_i])
        
        return pairs

    def _buildTrie(self, words):
        for i, word in enumerate(words):
            current = self.trie
            for char in word:
                if char not in current.childrens:
                    current.childrens[char] = Node({}, None)
                
                current = current.childrens[char]
            
            current.word_i = i
    
    def _isPolindrome(self, string):
        return string == string[::-1]
    
    def _DFSSearchWord(self, node, prefix):
        word = []
        
        if node.word_i is not None and prefix:
            word += [(prefix, node.word_i)]
        
        for child in node.childrens:
            word += self._DFSSearchWord(node.childrens[child], prefix + child)
        
        return word


if __name__ == "__main__":
    print(Solution().palindromePairs(["abcd","dcba","lls","s","sssll"]))
    print(Solution().palindromePairs(["a","abc","aba",""]))
    print(Solution().palindromePairs(["bat","tab","cat"]))
