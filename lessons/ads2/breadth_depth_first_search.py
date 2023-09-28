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

    def _find_node_by_key(self, key: Any, start_node: BSTNode) -> BSTNode:
        if start_node is None:
            return None, False, False
        if key == start_node.NodeKey:
            return start_node, True, False
        if key < start_node.NodeKey and not start_node.LeftChild:
            return start_node, False, True
        if key >= start_node.NodeKey and not start_node.RightChild:
            return start_node, False, False
        if key < start_node.NodeKey:
            return self._find_node_by_key(key, start_node.LeftChild)
        else:
            return self._find_node_by_key(key, start_node.RightChild)

    def FindNodeByKey(self, key: Any) -> BSTFind:
        # ищем в дереве узел и сопутствующую информацию по ключу
        search_result = BSTFind()
        (
            search_result.Node,
            search_result.NodeHasKey,
            search_result.ToLeft,
        ) = self._find_node_by_key(key, self.Root)
        return search_result

    def AddKeyValue(self, key: Any, val: Any) -> bool:
        # добавляем ключ-значение в дерево
        search_result = self.FindNodeByKey(key)
        if search_result.Node is None:
            self.Root = BSTNode(key, val)
            return True
        if search_result.NodeHasKey:
            return False  # если ключ уже есть
        if search_result.ToLeft:
            search_result.Node.LeftChild = BSTNode(key, val, search_result.Node)
        else:
            search_result.Node.RightChild = BSTNode(key, val, search_result.Node)
        return True

    def FinMinMax(self, FromNode: BSTNode, FindMax: bool) -> BSTNode:
        # ищем максимальный/минимальный ключ в поддереве
        # возвращается объект типа BSTNode
        direction = {True: "RightChild", False: "LeftChild"}[FindMax]
        if FromNode is None:
            return None
        while True:
            if getattr(FromNode, direction) is not None:
                FromNode = getattr(FromNode, direction)
            else:
                return FromNode

    def _delete_leaf(self, node: BSTNode) -> None:
        parent_node = node.Parent
        if parent_node and parent_node.LeftChild is node:
            parent_node.LeftChild = None
        elif parent_node:
            parent_node.RightChild = None
        node.Parent = None
        node.RightChild = None
        node.LeftChild = None

    def _delete_node_with_right_xor_left_child(self, node: BSTNode) -> BSTNode:
        substitutor = node.LeftChild if node.LeftChild is not None else node.RightChild
        parent = node.Parent

        if parent and parent.LeftChild is node:
            parent.LeftChild = None
        elif parent:
            parent.RightChild = None
        node.Parent = None
        node.RightChild = None
        node.LeftChild = None

        if parent and substitutor.NodeKey < parent.NodeKey and parent.LeftChild is None:
            parent.LeftChild = substitutor
        elif (
            parent
            and substitutor.NodeKey >= parent.NodeKey
            and parent.RightChild is None
        ):
            parent.RightChild = substitutor
        else:
            raise ValueError
        substitutor.Parent = parent
        return substitutor

    def _delete_node_with_both_children(self, node: BSTNode) -> BSTNode:
        substitutor = self.FinMinMax(node.RightChild, False)
        parent = node.Parent

        if substitutor.RightChild is not None:
            substitutor.RightChild.Parent = substitutor.Parent
        if substitutor is not node.RightChild:
            substitutor.Parent.LeftChild = substitutor.RightChild
            substitutor.Parent = parent

        if parent and parent.LeftChild is node:
            parent.LeftChild = substitutor
        elif parent and parent.RightChild is node:
            parent.RightChild = substitutor

        substitutor.LeftChild = node.LeftChild
        substitutor.RightChild = node.RightChild
        substitutor.LeftChild.Parent = substitutor.RightChild.Parent = substitutor

        parent = node.LeftChild = node.RightChild = None
        return substitutor

    def _proceed_with_root(self, old_root: BSTNode, new_root: BSTNode = None) -> None:
        if self.Root is old_root:
            self.Root = new_root

    def DeleteNodeByKey(self, key: Any) -> bool:
        # удаляем узел по ключу
        search_result = self.FindNodeByKey(key)
        substitutor = None
        if not search_result.NodeHasKey:
            return False  # если узел не найден
        if (
            search_result.Node.LeftChild is None
            and search_result.Node.RightChild is None
        ):
            self._delete_leaf(search_result.Node)
        elif (search_result.Node.LeftChild is None) ^ (
            search_result.Node.RightChild is None
        ):
            substitutor = self._delete_node_with_right_xor_left_child(
                search_result.Node
            )
        else:
            substitutor = self._delete_node_with_both_children(search_result.Node)
        self._proceed_with_root(search_result.Node, substitutor)
        return True

    def _nodes_count(self, start_node: BSTNode) -> int:
        counter = 1
        if start_node.LeftChild:
            counter += self._nodes_count(start_node.LeftChild)
        if start_node.RightChild:
            counter += self._nodes_count(start_node.RightChild)
        return counter

    def Count(self) -> int:
        if self.Root is None:
            return 0
        return self._nodes_count(self.Root)

    def WideAllNodes(self) -> Tuple[BSTNode]:
        if self.Root is None:
            return []
        nodes_list = [
            self.Root,
        ]
        current_level_list = [self.Root]
        while current_level_list:
            aux_list = []
            for node in current_level_list:
                if node.LeftChild is not None:
                    aux_list.append(node.LeftChild)
                if node.RightChild is not None:
                    aux_list.append(node.RightChild)
            nodes_list.extend(aux_list)
            current_level_list = aux_list
        return nodes_list

    def DeepAllNodes(self, order_type: int) -> Tuple[BSTNode]:
        nodes_list = []
        self._depth_first_search(self.Root, nodes_list, order_type)
        return nodes_list

    def _depth_first_search(
        self, start_node: BSTNode, nodes_list: List, order_type: int
    ) -> List[BSTNode]:
        if order_type == 0:
            self.__step_to_child(start_node.LeftChild, nodes_list, order_type)
            nodes_list.append(start_node)
            self.__step_to_child(start_node.RightChild, nodes_list, order_type)
        if order_type == 1:
            self.__step_to_child(start_node.LeftChild, nodes_list, order_type)
            self.__step_to_child(start_node.RightChild, nodes_list, order_type)
            nodes_list.append(start_node)
        if order_type == 2:
            nodes_list.append(start_node)
            self.__step_to_child(start_node.LeftChild, nodes_list, order_type)
            self.__step_to_child(start_node.RightChild, nodes_list, order_type)

    def __step_to_child(self, node, nodes_list, order_type):
        if node is not None:
            self._depth_first_search(node, nodes_list, order_type)
