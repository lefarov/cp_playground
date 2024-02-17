"""
Can be solved using Divide and conqure by merging pairs of lists:
time complexity is O(Nlogk) and space complexity is O(1)
"""

from heapq import heappush, heappop
from typing import List


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class ListNodeHeapifyable(ListNode):
    @classmethod
    def from_list_node(cls, list_node):
        return cls(list_node.val, list_node.next)
    
    def __lt__(self, other):
        return self.val < other.val


class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        elements_heap = []
        for l in lists:
            heappush(elements_heap, ListNodeHeapifyable.from_list_node(l))
            
        res_head = ListNode(0)
        res_current = res_head
        
        # While not empty heap
        while elements_heap:
            # Pop element and add it to the result
            current_min = heappop(elements_heap)
            res_current.next = ListNode(current_min.val)
            res_current = res_current.next
            
            # If not the end, push next element to the heap
            if current_min.next is not None:
                heappush(elements_heap, ListNodeHeapifyable.from_list_node(current_min.next))
                
        return res_head.next