from typing import List


def cut_ribbons(ribbons: List[int], k: int):

    def _can_cut_k(length):
        for r in ribbons:
            k -= r // length

        return k <= 0

    # 3 4 5 6 7 8 9

    lp, rp = min(ribbons), max(ribbons)
    while lp <= rp:
        mp = (lp + rp) // 2
        
        if _can_cut_k(mp):
            mp = lp + 1
        else:
            rp = mp - 1

    return rp