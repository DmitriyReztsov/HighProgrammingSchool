from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    values_list = []

    def _get_node(self, root):
        if root.left:
            self._get_node(root.left)

        self.values_list.append(root.val)

        if root.right:
            self._get_node(root.right)

    def inorderTraversal(self, root: Optional[TreeNode]) -> list[int]:
        self._get_node(root)
        return self.values_list
        

if __name__ == "__main__":
    root = [1, 2, 3, 4, 5, None, 8, None, None, 6, 7, None, None, 9]
    # root = [1, None, 2, None, None, 3]
    nodes_list = []
    for val in root:
        if val is not None:
            nodes_list.append(TreeNode(val))
        else:
            nodes_list.append(None)

    for ind, node in enumerate(nodes_list):
        if not node:
            continue

        left_ind = 2 * ind + 1
        if left_ind < len(nodes_list):
            node.left = nodes_list[left_ind]

        right_ind = 2 * ind + 2
        if right_ind < len(nodes_list):
            node.right = nodes_list[right_ind]

    print(Solution().inorderTraversal(nodes_list[0]))