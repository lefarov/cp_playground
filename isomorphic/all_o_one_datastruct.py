import collections


class Node:
    def __init__(self, key, freq):
        self.keys = {key}
        self.freq = freq
        self.prev = None
        self.next = None

# [{hello, world}: 2] -> [{"pussy"}: 3] <-> [{"shady"}, 5] <-> [{"slim"}: 6]


class AllOne:

    def __init__(self):
        self.key2node = {}
        self.head = None
        self.tail = None

    def inc(self, key: str) -> None:
        if key not in self.key2node:
            # insert new
            if self.head and self.head.freq == 1:
                # we have head with 1
                self.head.keys.add(key)
                self.key2node[key] = self.head
            else:
                new_head = Node(key, 1)
                self.insert(new_head, None)
                self.key2node[key] = new_head

                if not self.tail:
                    self.tail = self.head

        else:
            # increment existing
            # [{}, 3] <-> [{}, 4] ->
            # [{}, 3] <-> [{}, 5] ->
            # [{}, 3] ->
            cur = self.key2node[key]
            freq = cur.freq
            
            _next = cur.next
            if _next and _next.freq == freq + 1:
                _next.keys.add(key)
                self.key2node[key] = _next
            else:
                new_next = Node(key, freq + 1)
                self.insert(new_next, cur)
                self.key2node[key] = new_next
            
            cur.keys.remove(key)
            if not cur.keys:
                self.delete(cur)

    def dec(self, key: str) -> None:
        # don't forget to delete if we decrement to 0
        # [{}, 1] <-> [{}, 2] <-> [{}, 3] ->
        #             [{}, 3] -> 
        # [{}, 2] <-> [{}, 3] <->
        cur = self.key2node[key]
        freq = cur.freq

        prev = cur.prev
        if prev and prev.freq == freq - 1:
            prev.keys.add(key)
            self.key2node[key] = prev
        else:
            if freq > 1:
                new_prev = Node(key, freq - 1)
                self.insert(new_prev, prev)
                self.key2node[key] = new_prev
            else:
                del self.key2node[key]

        cur.keys.remove(key)
        if not cur.keys:
            self.delete(cur)
        
    def insert(self, new_node, node):
        # None - [] <-> [] <- *[] -> None
        _next = node.next if node else self.head

        new_node.next = _next
        new_node.prev = node

        if _next:
            _next.prev = new_node
        else:
            self.tail = new_node

        if node:
            node.next = new_node
        else:
            self.head = new_node

    def delete(self, node):
        # None - [] <-> [] <-> [] - None
        # None - [] - None
        prev = node.prev
        _next = node.next

        if prev:
            prev.next = _next
            if _next:
                _next.prev = prev
            else:
                self.tail = prev
        else:
            # remove from the head
            if _next:
                _next.prev = None
            else:
                self.tail = None

            self.head = _next

    def getMaxKey(self) -> str:
        if self.head:
            return next(iter(self.tail.keys))
        
        return ""

    def getMinKey(self) -> str:
        if self.tail:
            return next(iter(self.head.keys))

        return ""
    

"""
Input
["AllOne", "inc", "inc", "getMaxKey", "getMinKey", "inc", "getMaxKey", "getMinKey"]
[[], ["hello"], ["hello"], [], [], ["leet"], [], []]
Output
[null, null, null, "hello", "hello", null, "hello", "leet"]

Explanation
AllOne allOne = new AllOne();
allOne.inc("hello");
allOne.inc("hello");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "hello"
allOne.inc("leet");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "leet"
"""

if __name__ == "__main__":
    allOne = AllOne()
    allOne.inc("hello")
    allOne.inc("hello")
    allOne.getMaxKey()  # return "hello"
    allOne.getMinKey()  # return "hello"
    allOne.dec("hello")
    allOne.dec("hello")
    allOne.getMaxKey()  # return "hello"
    allOne.inc("hello")
    allOne.getMinKey()  # return "leet"    
    pass