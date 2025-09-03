from random import randrange
from typing import List

class Solution:
    def __init__(self, n: int, blacklist: List[int]):
        # 0,   1,   2,   3,   4,   5,   6
        #           _    _         _ 

        self.mapping_range_limit = n - len(blacklist)  # 4
        self.mapping_dict = {}
        blacklist_set = set(blacklist)

        mapping_start_index = self.mapping_range_limit  # 4

        for black_number in blacklist:
            if black_number < self.mapping_range_limit:
                while mapping_start_index in blacklist_set:
                    mapping_start_index += 1

                self.mapping_dict[black_number] = mapping_start_index

                mapping_start_index += 1

    def pick(self) -> int:

        random_pick = randrange(self.mapping_range_limit)

        return self.mapping_dict.get(random_pick, random_pick)