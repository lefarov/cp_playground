from typing import List


class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        self.word_set = set(wordList)
        self.end_word = endWord
        self.sub_solution = {}
        pass

    def recursive_solve(self, current_word):
        if current_word == self.end_word:
            return [current_word]

        min_chains = []
        self.sub_solution[current_word] = min_chains

        for i in range(len(current_word)):
            new_word = current_word[:i] + self.end_word[i] + current_word[(i + 1):]
            
            if new_word in self.word_set:
                    min_chains.append([current_word, *self.recursive_solve(min_chains)])
                    
        


if __name__ == "__main__":
    print(Solution().findLadders("hit", "cog", ["hot","dot","dog","lot","log","cog"]))