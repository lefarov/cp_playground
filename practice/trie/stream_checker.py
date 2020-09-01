from typing import List
from collections import deque


class StreamChecker:

    """
    1) Maximum lengthg of word = Maximum size of qeury mem
    2) Reverse the words on and reverse the query mem -> DFS search in Trie
    """

    def __init__(self, words: List[str]):
        self.trie = {}
        self.q = deque()
        self.maxqsize = 0
        for word in words: 
            self.maxqsize = max(self.maxqsize, len(word))
            self._construct(word[::-1])
            
    def _construct(self, word):
        trie = self.trie
        for ch in word:
            if ch not in trie:
                trie[ch] = {}
            trie = trie[ch]
        trie['#'] = None
    
    def _DFSWordSearch(self, word):
        trie = self.trie
        for ch in word:
            if '#' in trie: 
                return True
            if ch not in trie: 
                break
            trie = trie[ch] 
        
        return '#' in trie

    def query(self, letter: str) -> bool:
        self.q.append(letter)
        if len(self.q) > self.maxqsize: self.q.popleft()
        if letter in self.trie:
            tocheck = list(self.q)
            tocheck.reverse()
            return self._DFSWordSearch(tocheck)
        return False


if __name__ == "__main__":
    st = StreamChecker(["cd","f","kl"])
    query = "abcdefghijkl"
    for char in query:
        print(f"{char}: {st.query(char)}")
