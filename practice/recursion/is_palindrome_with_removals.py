import functools


def is_palindrome(s, k):

    @functools.cache
    def _recursive_check(lind, rind, remaining_k):
        while lind < rind and s[lind] == s[rind]:
            lind += 1
            rind -= 1

        if lind >= rind:
            # processing is complete
            return True
        else:
            if remaining_k <= 0:
                return False

            return any([
                _recursive_check(lind + 1, rind, remaining_k - 1),
                _recursive_check(lind, rind - 1, remaining_k - 1)
            ])

    return _recursive_check(0, len(s) - 1, k)


if __name__ == '__main__':
    print(is_palindrome('aba', 0))
