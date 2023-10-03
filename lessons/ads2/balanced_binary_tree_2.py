from math import ceil
from typing import Any, List, Tuple


class BSTNode:
    def __init__(self, key: Any, parent: "BSTNode" = None) -> None:
        self.NodeKey = key  # ключ узла
        self.Parent = parent  # родитель или None для корня
        self.LeftChild: BSTNode = None  # левый потомок
        self.RightChild: BSTNode = None  # правый потомок
        self.Level: int = 0  # уровень узла


class BalancedBST:
    def __init__(self) -> None:
        self.Root: BSTNode = None  # корень дерева

    def _generate_tree(
        self,
        input_array: List,
        left_index: int,
        right_index: int,
        parent_node: BSTNode = None,
        level_counter: int = 0,
    ) -> BSTNode:
        pivot_index = ceil((right_index - left_index) / 2) + left_index
        if left_index > right_index:
            return

        subtree_root = BSTNode(input_array[pivot_index], parent_node)
        subtree_root.Level = level_counter
        if left_index == right_index:
            return subtree_root

        subtree_root.LeftChild = self._generate_tree(
            input_array, left_index, pivot_index - 1, subtree_root, level_counter + 1
        )

        subtree_root.RightChild = self._generate_tree(
            input_array, pivot_index + 1, right_index, subtree_root, level_counter + 1
        )
        return subtree_root

    def GenerateTree(self, a: List) -> BSTNode:
        # создаём дерево с нуля из неотсортированного массива a
        a.sort()
        self.Root = self._generate_tree(a, 0, len(a) - 1)
        return self.Root

    def _is_balanced(self, root_node: BSTNode) -> Tuple[int, bool]:
        if root_node is None:
            return 0, True

        left_balanced, left_height = self._is_balanced(root_node.LeftChild)
        right_balanced, right_height = self._is_balanced(root_node.RightChild)
        height_diff_ok = abs(left_height - right_height) <= 1

        if left_balanced and right_balanced and height_diff_ok:
            return max(left_height, right_height) + 1, True
        return max(left_height, right_height) + 1, False

    def IsBalanced(self, root_node: BSTNode) -> bool:
        _, is_balanced = self._is_balanced(root_node)
        return is_balanced
