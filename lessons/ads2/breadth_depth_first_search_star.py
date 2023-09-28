from typing import Any, List, Tuple


class BSTNode:
    def __init__(self, key: Any, val: Any, parent: "BSTNode" = None) -> None:
        self.NodeKey = key  # ключ узла
        self.NodeValue = val  # значение в узле
        self.Parent = parent  # родитель или None для корня
        self.LeftChild = None  # левый потомок
        self.RightChild = None  # правый потомок


class BSTFind:  # промежуточный результат поиска
    def __init__(self) -> None:
        self.Node: BSTNode = None  # None если в дереве вообще нету узлов
        self.NodeHasKey: bool = False  # True если узел найден
        self.ToLeft: bool = False  # True, если родительскому узлу надо добавить новый узел левым потомком


class BST:
    def __init__(self, node: BSTNode = None) -> None:
        self.Root = node  # корень дерева, или None

    def invert_tree(self) -> None:
        if self.Root is None:
            return []
        current_level_list = [self.Root]
        while current_level_list:
            aux_list = []
            for node in current_level_list:
                if node is None:
                    continue
                node.LeftChild, node.RightChild = node.RightChild, node.LeftChild
                aux_list.extend([node.LeftChild, node.RightChild])
            current_level_list = aux_list
