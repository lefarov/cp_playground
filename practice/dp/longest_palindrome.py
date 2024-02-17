
class Solution:
    def longestPalindrome(self, s: str) -> str:
        memory = {ch: ch for ch in s}
        memory[""] = ""

        for substr_len in range(2, len(s) + 1):
            for substr_start in range((len(s) - substr_len) + 1):

                # If result for this computation already in the memory
                current_substr = s[substr_start:(substr_start + substr_len)]
                if current_substr in memory:
                    continue

                # If last symbol equal to the first one
                if current_substr[0] == current_substr[-1]:
                    # If the middle is polindrome
                    if memory[current_substr[1:-1]] == current_substr[1:-1]:
                        memory[current_substr] = current_substr
                        continue

                # Save the longest palindrome from the left subsrting
                memory[current_substr] = memory[current_substr[:-1]]
                # If right substring has bigger palindrome
                if len(memory[current_substr[1:]]) > len(memory[current_substr]):
                    # Overwrite the memory
                    memory[current_substr] = memory[current_substr[1:]]
                    
        return memory[s]


if __name__ == "__main__":
    sol = Solution()
    print(sol.longestPalindrome("gphyvqruxjmwhonjjrgumxjhfyupajxbjgthzdvrdqmdouuukeaxhjumkmmhdglqrrohydrmbvtuwstgkobyzjjtdtjroqpyusfsbjlusekghtfbdctvgmqzeybnwzlhdnhwzptgkzmujfldoiejmvxnorvbiubfflygrkedyirienybosqzrkbpcfidvkkafftgzwrcitqizelhfsruwmtrgaocjcyxdkovtdennrkmxwpdsxpxuarhgusizmwakrmhdwcgvfljhzcskclgrvvbrkesojyhofwqiwhiupujmkcvlywjtmbncurxxmpdskupyvvweuhbsnanzfioirecfxvmgcpwrpmbhmkdtckhvbxnsbcifhqwjjczfokovpqyjmbywtpaqcfjowxnmtirdsfeujyogbzjnjcmqyzciwjqxxgrxblvqbutqittroqadqlsdzihngpfpjovbkpeveidjpfjktavvwurqrgqdomiibfgqxwybcyovysydxyyymmiuwovnevzsjisdwgkcbsookbarezbhnwyqthcvzyodbcwjptvigcphawzxouixhbpezzirbhvomqhxkfdbokblqmrhhioyqubpyqhjrnwhjxsrodtblqxkhezubprqftrqcyrzwywqrgockioqdmzuqjkpmsyohtlcnesbgzqhkalwixfcgyeqdzhnnlzawrdgskurcxfbekbspupbduxqxjeczpmdvssikbivjhinaopbabrmvscthvoqqbkgekcgyrelxkwoawpbrcbszelnxlyikbulgmlwyffurimlfxurjsbzgddxbgqpcdsuutfiivjbyqzhprdqhahpgenjkbiukurvdwapuewrbehczrtswubthodv"))