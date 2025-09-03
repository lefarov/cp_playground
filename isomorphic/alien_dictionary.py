import collections
from typing import List

class Solution:
    def validate_dictionary(self, words: List[str]):
        # go over pairs
        # t -> f, w -> e, r -> t, e -> r, t -> f

        # ["wa", "wc", "wrt", "wrf", "wrfx", "wrfz", "er", "ett", "rftt", "rfttx", "rfttm" "rfttmp"]

        # buil graph
        graph = {char: [] for word in words for char in word}

        for word1, word2 in zip(words, words[1:]):
            for i in range(min(len(word1), len(word2))):
                if word1[i] != word2[i]:
                    graph[word1[i]].append(word2[i])
                    break

            else:
                if len(word1) > len(word2):
                    return ""


        self.valid = True

        white = set(graph.keys())
        grey = set()
        black = {}
        
        def _dfs(char):
            white.remove(char)
            grey.add(char)

            res = char
            for next_char in graph[char]:
                if next_char in grey:
                    # think what to return here
                    self.valid = False
                    return ""
                
                if next_char in black:
                    return res
                
                res += _dfs(next_char)

            grey.remove(char)
            black[char] = res

            return black[char]

        chars = []
        while white:
            char = next(iter(white))
            chars.append(_dfs(char))

        return "".join(reversed(chars)) if self.valid else ""


if __name__ == "__main__":

    # w -> e -> r -> t -> f
    #   a -> c -^
    #                x -> z
    #                | -> m
    #      p

    # abcd
    # ez

    Solution().validate_dictionary(
        ["wa", "wc", "wrt", "wrf", "wrfx", "wrfz", "er", "ett", "rftt", "rfttx", "rfttm", "rfttmp"]
    )