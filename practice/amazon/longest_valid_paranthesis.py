class Solution:
    def longestValidParentheses(self, s: str) -> int:
        # )()())
        # ())()
        # (()(()

        # [()]
        # [(2(2]
        # [)4)]

        #
        # if balance == 0: res = max(curr_len, res)
        # when invalid: restart the running len
        # end of string:
        #   if positive balance

        # )()())
        # ()
        res = 0

        lp = 0
        balance = 0
        for rp, ch in enumerate(s):
            if not balance:
                res = max(res, rp - lp)

            if ch == "(":
                balance += 1
            else:
                if balance > 0:
                    balance -= 1
                else:
                    lp = rp + 1

        if not balance and lp < rp:
            res = max(res, rp-lp + 1)


        # going from other direction
        rp = len(s) - 1
        balance = 0
        # (((()
        for lp, ch in reversed(list(enumerate(s))):
            if not balance:
                res = max(res, rp - lp)

            if ch == ")":
                balance += 1
            else:
                if balance > 0:
                    balance -= 1
                else:
                    rp = lp - 1

        if not balance and lp < rp:
            res = max(res, rp - lp + 1)

        return res


if __name__ == "__main__":
    print(Solution().longestValidParentheses("((()"))
