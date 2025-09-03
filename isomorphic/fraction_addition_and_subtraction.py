class Solution:
    def fractionAddition(self, expression: str) -> str:
        num = 0
        denom = 1
        
        i = 0
        while i < len(expression):
            sign = 1
            if expression[i] == "-":
                sign *= -1
                i += 1
            elif expression[i] == "+":
                i += 1

            new_num = 0
            while 48 <= ord(expression[i]) <= 57:
                new_num *= 10
                new_num += int(expression[i])
                i += 1

            i += 1

            new_denom = 0
            while i < len(expression) and 48 <= ord(expression[i]) <= 57:
                new_denom *= 10
                new_denom += int(expression[i])
                i += 1

            "1/3-1/2"
            num = num * new_denom + sign * new_num * denom  #  - 1 / 6
            denom *= new_denom

        gcd = abs(Solution._gcd(num, denom))
        num //= gcd
        denom //= gcd

        return f"{num}/{denom}"

    @staticmethod
    def _gcd(a, b):
        if a == 0: 
            return b

        return Solution._gcd(b % a, a)