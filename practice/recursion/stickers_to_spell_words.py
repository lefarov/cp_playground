import collections
import functools
from typing import List


class Solution:
    def minStickers(self, stickers: List[str], target: str) -> int:
        # stickers = ["with","example","science"], target = "thehat"
        stickers_counts = [collections.Counter(sticker) for sticker in stickers]

        self.num_used = float("inf")

        @functools.cache
        def _recursive_search(remaining_target, num_used):
            if remaining_target == "":
                # empty counts
                self.num_used = min(self.num_used, num_used)
                return

            target_counts = collections.Counter(remaining_target)

            for sticker_counts in stickers_counts:
                if remaining_target[0] not in sticker_counts:
                    continue

                ramining_counts = target_counts - sticker_counts
                _recursive_search("".join(k * n for k, n in ramining_counts.items()), num_used + 1)

            return

        _recursive_search(target, 0)
        return self.num_used


if __name__ == "__main__":
    solution = Solution()
    print(solution.minStickers(stickers=["with", "example", "science"], target="thehat"))
