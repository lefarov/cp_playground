from typing import List

import collections


class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        # ["This", "is", "an", "example", "of", "text", "justification."]

        # [this_is_an_o]

        text = []
        row = collections.deque()
        current_len = 0

        for word in words:
            if current_len + len(word) <= maxWidth:
                row.append(word)
                current_len += len(word) + 1
            else:
                occupied_len = current_len - len(row)
                free_len = maxWidth - occupied_len

                just_row = self.justify_row(row, free_len)

                text.append(just_row)
                row = collections.deque([word])
                current_len = len(word) + 1

        occupied_len = current_len - len(row)
        free_len = maxWidth - occupied_len
        just_row = self.justify_row(row, free_len, True)

        text.append(just_row)

        return text
    
    @staticmethod
    def justify_row(row, free_len, is_last=False):
        # [test, " ", my, pow]
        n_words = len(row)

        if n_words > 1:
            n_equal_spaces = free_len // (n_words - 1)
            n_left_spaces = free_len % (n_words - 1)

            if is_last:
                i_word = 0
                while i_word < len(row) - 1:
                    row.insert(i_word + 1, " ")
                    free_len -= 1
                    i_word += 2

                row.append(" " * free_len)

            else:
                i_word = 0
                while i_word < len(row) - 1:
                    row.insert(i_word + 1, " " * (n_equal_spaces + int(n_left_spaces > 0)))
                    n_left_spaces -= 1
                    i_word += 2
                
            return "".join(row)

        else:
            word = row.pop()
            return word + " " * free_len

    

if __name__ == "__main__":
    print(Solution().fullJustify(["ask","not","what","your","country","can","do","for","you","ask","what","you","can","do","for","your","country"], 16))