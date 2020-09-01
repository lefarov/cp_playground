import sys


class Node:

    def __init__(self, childrens, is_word):
        self.childrens = childrens
        self.is_word = is_word


class Solution:

    @staticmethod
    def isGoodSet(set_of_strings):
        trie = Node({}, False)
        for string in set_of_strings:
            current = trie
            for char in string:
                # current node is word
                if current.is_word:
                    return f"BAD SET\n{string}"

                if char not in current.childrens:
                    current.childrens[char] = Node({}, False)
                
                current = current.childrens[char]

            # traversed the entire stirng but there're still some childrens
            if current.childrens or current.is_word:
                return f"BAD SET\n{string}"

            current.is_word = True

        return "GOOD SET"

    
if __name__ == "__main__":
    print(Solution.isGoodSet([
        "aab", "defgab", "abcde", "aabcde", "cedaaa", "bbbbbbbbbb", "jabjjjad"]))
    print(Solution.isGoodSet(["aab", "aac", "aacghgh", "aabghgh"]))
    print(Solution.isGoodSet(["a", "a"]))
