from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # construct trie from word dict
        # "applepenapple"
        # ["apple","pen", "applep", "ena"]
        memo = [0] * len(s)
        for i in range(len(s) - 1, -1, -1):
            for j in range(i + 1, len(s)):
                if memo[j] and s[i:j] in wordDict:
                    memo[i] = 1
                    break

            if not memo[i]:
                memo[i] = int(s[i:] in wordDict)

        return memo[0]

    def dp_search(self, s, trie):
        # "catsandog"
        # ["cats","dog","sand","and","cat"]
        memo = [0] * len(s)
        for i in range(len(s) - 1, -1, -1):
            node = trie
            for char_i in range(i, len(s)):
                if "$" in node:
                    if memo[char_i] == 1:
                        memo[i] = 1
                        break

                if s[char_i] in node:
                    node = node[s[char_i]]
                else:
                    memo[i] = 0
                    break

            if char_i == len(s) - 1:
                memo[i] = int("$" in node)

        return memo[0]

    def recursive_search(self, s, trie):
        if len(s) == 0:
            return True

        node = trie
        for i, char in enumerate(s):
            if "$" in node:
                if self.recursive_search(s[i:], trie):
                    return True

            if char in node:
                node = node[char]
            else:
                return False

        return "$" in node

    def construct_trie(self, wordDict):
        trie = {}
        for word in wordDict:
            root = trie
            for char in word:
                root.setdefault(char, {})
                root = root[char]

            root["$"] = 1

        return trie


if __name__ == "__main__":
    print(Solution().wordBreak("catsandog", ["cats","dog","sand","and","cat"]))
