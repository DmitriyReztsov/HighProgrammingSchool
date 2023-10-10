from typing import Any, Optional, List
from copy import deepcopy, copy


class SimpleTreeNode:
    def __init__(self, val: Any, parent: Optional["SimpleTreeNode"] = None) -> None:
        self.NodeValue = val  # значение в узле
        self.Parent = parent  # родитель или None для корня
        self.Children = []  # список дочерних узлов

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if __name == "Parent" and __value is None:
            self.level = 0
        elif __name == "Parent" and __value is not None:
            self.level = self.Parent.level + 1
        if hasattr(self, "Children"):
            self._set_levels()

    def _set_levels(self):
        if not self.Children:
            return

        for child in self.Children:
            child.level = self.level + 1
            child._set_levels()


class SimpleTree:
    def __init__(self, root: Optional[SimpleTreeNode] = None):
        self.Root = root  # корень, может быть None

    def AddChild(self, ParentNode: SimpleTreeNode, NewChild: SimpleTreeNode) -> None:
        ParentNode.Children.append(NewChild)
        NewChild.Parent = ParentNode

    def DeleteNode(self, NodeToDelete: SimpleTreeNode) -> None:
        if NodeToDelete is not self.Root:
            NodeToDelete.Parent.Children.remove(NodeToDelete)
            NodeToDelete.Parent = None
        else:
            self.Root = None

    def _get_all_nodes(self, start_node: SimpleTreeNode, nodes_list: List) -> None:
        if not start_node.Children:
            return nodes_list.append(start_node)
        nodes_list.append(start_node)
        for node in start_node.Children:
            self._get_all_nodes(node, nodes_list)

    def GetAllNodes(self, root: SimpleTreeNode = None) -> List[SimpleTreeNode]:
        if root is None:
            root = self.Root
        nodes_list = []
        self._get_all_nodes(root, nodes_list)
        return nodes_list

    def FindNodesByValue(self, val: Any) -> List[SimpleTreeNode]:
        return [node for node in self.GetAllNodes() if node.NodeValue == val]

    def MoveNode(self, OriginalNode: SimpleTreeNode, NewParent: SimpleTreeNode) -> None:
        # ваш код перемещения узла вместе с его поддеревом --
        # в качестве дочернего для узла NewParent
        self.DeleteNode(OriginalNode)
        self.AddChild(NewParent, OriginalNode)

    def Count(self, root: SimpleTreeNode = None) -> int:
        # количество всех узлов в дереве
        if root is None:
            root = self.Root
        a = len(self.GetAllNodes(root))
        return a

    def LeafCount(self) -> int:
        # количество листьев в дереве
        count_leaves = 0
        all_nodes = self.GetAllNodes()
        for node in all_nodes:
            if not node.Children:
                count_leaves += 1
        return count_leaves

    def set_level(self) -> None:
        nodes_list = self.GetAllNodes()
        for node in nodes_list:
            if node.Parent:
                node.level = node.Parent.level + 1
            else:
                node.level = 0
            node._set_levels()

    def _trim_the_forest(
        self, nodes_to_break: List[SimpleTreeNode], root: SimpleTreeNode = None
    ) -> None:
        if root is None:
            root = self.Root
        if not root.Children:
            return
        for child in root.Children:
            sub_root = SimpleTreeNode(root.NodeValue)
            sub_root.Children = copy(root.Children)
            sub_root.Children.remove(child)
            if (self.Count(child) % 2 == 1) or (self.Count(sub_root) % 2 == 1):
                continue
            nodes_to_break.extend([root, child])
            self._trim_the_forest(nodes_to_break, child)

    def EvenTrees(self) -> List[SimpleTreeNode]:
        if self.Count() % 2 != 0:
            return []
        nodes_to_break = []
        self._trim_the_forest(nodes_to_break)
        return nodes_to_break
