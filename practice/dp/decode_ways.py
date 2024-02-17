class Solution:
    def numDecodings(self, s: str) -> int:
        code = str(int(s))
        num_decodings = [0] * len(code) + [1]

        for i in reversed(range(0, len(code))):
            if not int(code[i]):
                continue

            if i < (len(code) - 1) and int(code[i:i + 2]) <= 26:
                num_decodings[i] += num_decodings[i + 2]

            num_decodings[i] += num_decodings[i + 1]

        return num_decodings[0]


if __name__ == "__main__":
    sol = Solution()
    print(sol.numDecodings("0021021"))