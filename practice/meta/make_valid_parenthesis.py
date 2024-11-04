class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        # " ) ( "
        # " (  )  )  )  ( )  ) ( "
        # [ 1  0 -1 -2  1 0 -1 1 ]

        balance = 0
        result = 0
        for char in s:
            if s == "(":
                balance += 1
            elif s == ")":
                if balance == 0:
                    result += 1
                else:
                    balance -= 1

        return result + balance


if __name__ == '__main__':
    s = Solution()
    print(s.minAddToMakeValid("())"))
