import collections


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # ADOBECODEBANC
        # ABC
        t_counts = collections.Counter(t)
        counts = collections.defaultdict(int)
        lp = 0

        result = s

        for rp, r_char in enumerate(s):
            while self._cond_satisfied(counts, t_counts):
                if len(s[lp:rp]) < len(result):
                    result = s[lp:rp]

                l_char = s[lp]
                counts[l_char] = counts[l_char] - 1

                lp += 1

            while lp < len(s) and s[lp] not in t_counts:
                lp += 1

            if r_char in t_counts:
                counts[r_char] += 1

        if self._cond_satisfied(counts, t_counts):
            if len(s[lp:]) < len(result):
                result = s[lp:]

        return result

    def _cond_satisfied(self, current, target):
        for key, val in target.items():
            if val > current[key]:
                return False
        return True


if __name__ == "__main__":
    print(Solution().minWindow("ADOBECODEBANC", "ABC"))
