def compute_lps(pattern):
    # Longest Proper Prefix that is suffix array
    lps = [0] * len(pattern)

    prefi = 0
    for i in range(1, len(pattern)):
        
        # Phase 3: roll the prefix pointer back until match or 
        # beginning of pattern is reached
        while prefi and pattern[i] != pattern[prefi]:
            prefi = lps[prefi - 1]

        # Phase 2: if match, record the LSP for the current `i`
        # and move prefix pointer
        if pattern[prefi] == pattern[i]:
            prefi += 1
            lps[i] = prefi

        # Phase 1: is implicit here because of the for loop and 
        # conditions considered above

    return lps


def underscorifySubstring(string, substring):
    #compute lps
    lps = compute_lps(substring)[-1]

    result = ""
    lp = 0
    while lp < len(string):
        while string[lp:lp + len(substring)] != substring and lp < len(string):
            result += string[lp]
            lp += 1

        pivot = lp
        while lp < len(string):
            rp = pivot + len(substring)

            # temp pointer
            tp = rp - lps
            while string[tp: tp + len(substring)] != substring and tp < rp + 1:
                tp += 1

            if tp == rp + 1:
                result += f"_{string[lp:rp]}_"
                lp = rp
                break

            pivot = tp

    return result


input_data = {
  "string": "testthis is a testtest to see if testestest it works",
  "substring": "test"
}


underscorifySubstring(**input_data)