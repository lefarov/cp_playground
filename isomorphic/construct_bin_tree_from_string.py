
import collections

class Node:

    def __init__(self):
        self.val: int = None
        self.left: Node = None
        self.right: Node = None

    def to_array(self):
        res = []

        queue = collections.deque();
        queue.append(self)

        while queue:
            for _ in range(len(queue)):
                node = queue.popleft()
                res.append(node.val)
                
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)

        return res


def parse_string_to_tree(s: str, pos: int, head: Node) -> int:
    if s == "":
        return pos

    lp = pos
    while lp < len(s) and s[lp] not in {"(", ")"}:
        lp += 1

    head.val = int(s[pos:lp])
    if s[lp] == "(":
        head.left = Node()
        lp = parse_string_to_tree(s, lp + 1, head.left)
        lp += 1
    else:
        # ')' or eol
        return lp
    
    if s[lp] == "(":
        head.right = Node()
        lp = parse_string_to_tree(s, lp + 1, head.right)
        lp += 1
    
    return lp

if __name__ == "__main__":

    # input: 4(2(3)(1))(6(5))
    # output: [4, 2, 6, 3, 1, 5]
    head = Node()
    parse_string_to_tree("4(2(3)(1))(6(5))", 0, head)
    
    print(head.to_array())