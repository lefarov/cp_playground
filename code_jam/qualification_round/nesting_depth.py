import sys

def solve(input_str, t):
    parentheses_count = 0
    output_str = ""
    for c in input_str:
        parentheses_diff = int(c) - parentheses_count
        if parentheses_diff > 0:
            output_str += "(" * parentheses_diff
            parentheses_count += parentheses_diff

        elif parentheses_diff < 0:
            output_str += ")" * (- parentheses_diff)
            parentheses_count += parentheses_diff
        
        output_str += c
    
    if parentheses_count > 0:
        output_str += ")" * parentheses_count

    return "Case #{}: {}".format(t + 1, output_str)
        
        
if __name__ == "__main__":
    T = int(input())
    for t in range(T):
        print(solve(input(), t))

    sys.stdout.flush()
