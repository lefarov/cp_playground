""" Implemenation of the KMP algorithm.
"""
from typing import List


def compute_lps(pattern: str) -> List[int]:
    """ Compute the longest proper prefix which is suffix array.

    Function computes the LPS array. Every position `i` in the
    array contains the LPS for a substring of a pattern from 
    the beginning till the `i` inclusively.

    Algorithm maintaince two pointers (indices):
    prefi - index of a current considered prefix.
    i - index of a current char in the pattern.

    Algorithm can be devided into three phases:
    Phase 1: when prefix index is zero, move current char index 
    until a match.
    Phase 2: if symbols at prefix index and current index match, 
    save prefix index + 1 to the LSP array for current index and 
    move both indices.
    Phase 3: when prefix index is not zero and mismatch is found, 
    rollback prefix index using the data in LSP array. 

    Parameters
    ----------
    pattern: str
        Pattern sting.
    
    Returns
    -------
    List[int]:
        LSP array.
    """
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


def kmp(pattern: str, text: str) -> List[int]:
    """ Find occurrences of a pattern in a text with KMP.

    Algorithm maintaince two pointers (indices):
    patterni - index of a current symbol in a pattern.
    i - index of a current symboll in a target text.

    Algorithm can be devided into two phases:
    Phase 1: when pattern index is zero, move the current
    text index until the first match.
    Phase 2: if symbols in a pattern and a text are mathing,
    move both forward. If the end of a pattern is reached,
    save the result and use LSP array to move the pattern 
    index back to the correct position.
    Phase 3: when pattern index is not zero and a mismatch
    is found, rollback the pattern index.

    Parameters
    ----------
    pattern: str
        Pattern.
    text: str
        Target text.

    Returns
    -------
    List[int]:
        Indices of occurrence for a pattern in a text

    """
    match_indices = []
    pattern_lps = compute_lps(pattern)

    patterni = 0
    for i, ch in enumerate(text):
        
        # Phase 3: if a mismatch was found, roll back the pattern
        # index using the information in LPS
        while patterni and pattern[patterni] != ch:
            patterni = pattern_lps[patterni - 1]

        # Phase 2: if match
        if pattern[patterni] == ch:
            # If the end of a pattern is reached, record a result
            # and use infromation in LSP array to shift the index
            if patterni == len(pattern) - 1:
                match_indices.append(i - patterni)
                patterni = pattern_lps[patterni]
            
            else:
                # Move the pattern index forward
                patterni += 1

        # Phase 1: is implicit here because of the for loop and 
        # conditions considered above

    return match_indices

if __name__ == "__main__":
    print(compute_lps("ACA"))
    print(kmp("AABA", "AABAAABACAADAABAABA"))