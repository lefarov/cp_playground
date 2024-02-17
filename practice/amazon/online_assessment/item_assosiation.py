from collections import defaultdict, deque

class Solution:
    def item_associations(self, associations_list):
        associations = defaultdict(list)
        for source, target in associations_list:
            associations[source].append(target)

        groups = {}
        for association_pair in associations_list:
            visited = set()
            self.dfs(association_pair[0], associations, visited, groups)
        
        return groups

    def dfs(self, item, associations, visited, groups):
        visited.add(item)
        sub_group = []
        for associated_item in associations[item]:    
            
            if associated_item not in visited:
                if associated_item not in groups:
                    candidate = self.dfs(associated_item, associations, visited, groups)
                else:
                    candidate = groups[associated_item]
                
                if len(candidate) > len(sub_group):
                    sub_group = candidate

        groups[item] = [item, *sub_group]
        return [item, *sub_group]
        

if __name__ == "__main__":
    solution = Solution()
    print(solution.item_associations([["a", "d"], ["d", "z"], ["z", "a"], ["b", "c"], ["c", "d"]]))