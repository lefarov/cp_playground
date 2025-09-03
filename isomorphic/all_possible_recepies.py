import collections
import functools

from typing import List


class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        # build the graph [rec] -> [ing2]
        #                       |-> [ing2]

        alchemy_tree = collections.defaultdict(list)
        for i, rep in enumerate(recipes):
            alchemy_tree[rep].extend(ingredients[i])

        suppliers_set = set(supplies)

        def _dfs(rep):
            # can we have recepies that are ingredients of itself?
            # can we have recepies with 0 ingredients?
            if rep in trace:
                return False
            
            trace.add(rep)

            if rep not in alchemy_tree:
                trace.remove(rep)
                return rep in suppliers_set

            synthesizable = True
            for ing in alchemy_tree[rep]:
                synthesizable = synthesizable and _dfs(ing)

            trace.remove(rep)

            return synthesizable

        res = []
        for rep in recipes:
            trace = set()
            if _dfs(rep):
                res.append(rep)

        return res
    

if __name__ == "__main__":
    Solution().findAllRecipes(
        ["bread","sandwich","burger"],
        [["yeast","flour"],["bread","meat"],["sandwich","meat","bread"]],
        ["yeast","flour","meat"],
    )