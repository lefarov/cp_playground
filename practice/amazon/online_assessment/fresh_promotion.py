class Solution:

    def code_in_chart(self, code, chart):
        for i in range(len(chart)):
            found = True
            for j, code_item in enumerate(code):
                if (i + j) == len(chart) or code_item not in ("anything", chart[i + j]):
                    found = False
                    break

            if found:
                return True, (i + j) + 1

        return False, (i + 1)

    def promotion(self, code_list, chart) -> int:
        start = 0
        match = [False] * len(code_list)
        for ci, code in enumerate(code_list):
            found, stop = self.code_in_chart(code, chart[start:])
            
            match[ci] = found
            start += stop
            if stop >= len(chart):
                break
            
        return all(match)

if __name__ == "__main__":
    solution = Solution()
    code_list = [['anything', 'anything', 'apple'], ['banana', 'anything', 'banana']]
    shopping_cart = ['orange', 'grapes', 'orange', 'apple', 'orange', 'orange', 'banana', 'apple', 'banana', 'banana']
    assert solution.promotion(code_list, shopping_cart) == 1

    code_list = [['apple', 'apple'], ['banana', 'anything', 'banana']]
    shopping_cart = ['orange', 'apple', 'apple', 'banana', 'orange', 'banana']
    assert solution.promotion(code_list, shopping_cart) == 1

    code_list = [['apple', 'apple'], ['banana', 'anything', 'banana']]
    shopping_cart = ['banana', 'orange', 'banana', 'apple', 'apple']
    assert solution.promotion(code_list, shopping_cart) == 0

    code_list = [['apple', 'apple'], ['banana', 'anything', 'banana']]
    shopping_cart = ['apple', 'banana', 'apple', 'banana', 'orange', 'banana']
    assert solution.promotion(code_list, shopping_cart) == 0

    code_list = [['apple', 'apple'], ['apple', 'apple', 'banana']]
    shopping_cart = ['apple', 'apple', 'apple', 'banana']
    assert solution.promotion(code_list, shopping_cart) == 0