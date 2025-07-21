from typing import Optional


# Definition for a Node.
class Node:
    def __init__(
        self,
        val: int = 0,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
        next: Optional["Node"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    def height(self, node):
        if not node:
            return 0
        l_height = self.height(node.left)
        r_height = self.height(node.right)

        return max(l_height, r_height) + 1

    def process_level(self, root, level, right_node=None):
        if not root:
            return
        if level == 0:
            root.next = right_node
            return root
        elif level > 0:
            right_node = self.process_level(root.right, level - 1, right_node)
            return self.process_level(root.left, level - 1, right_node)

    def connect(self, root: Node | None) -> Node | None:
        h = self.height(root)
        for i in range(h):
            self.process_level(root, i)

    def _connect(self, root):
        if not root:
            return None
        left, right, next = root.left, root.right, root.next
        if left:
            left.next = right
            if next:
                right.next = next.left
            self.connect(left)
            self.connect(right)
        return root


if __name__ == "__main__":
    root = [1, 2, 3, 4, 5, 6, 7]

    nodes_list = []
    for val in root:
        nodes_list.append(Node(val))

    for ind, node in enumerate(nodes_list):
        left_ind = 2 * ind + 1
        if left_ind < len(nodes_list):
            node.left = nodes_list[left_ind]

        right_ind = 2 * ind + 2
        if right_ind < len(nodes_list):
            node.right = nodes_list[right_ind]

    Solution().connect(nodes_list[0])
    ...
