from typing import Any, List, Optional, Tuple


class Node:
    def __init__(self, v: Any) -> None:
        self.value = v
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_in_tail(self, item: None) -> None:
        if self.head is None:
            self.head = item
        else:
            self.tail.next = item
        self.tail = item

    def print_all_nodes(self):
        node = self.head
        while node != None:
            print(node.value)
            node = node.next

    def find(self, val: Any, from_node: Node = None) -> Optional[Node]:
        node = self.head if from_node is None else from_node
        while node is not None:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val: Any) -> List[Node]:
        result_list = []
        node = self.find(val)
        if node is None:
            return result_list

        result_list.append(node)
        find_more = not (node.next is None)

        while find_more:
            node = self.find(val, node.next)
            if node is None:
                break
            result_list.append(node)
            find_more = not (node.next is None)

        return result_list

    def _find_with_previous(
        self, val: Any, from_node: Node = None
    ) -> Tuple[Optional[Node]]:
        node = self.head if from_node is None else from_node
        if node is None:
            return None, None

        if node.value == val:
            return None, node

        next_node = node.next
        while next_node is not None:
            if next_node.value == val:
                return node, next_node
            node = next_node
            next_node = next_node.next

        return None, None

    def _delete(self, prev_node: Node, node: Node) -> Optional[Node]:
        if prev_node is None and node is None:
            return None
        if prev_node is None:
            self.head = node.next
        else:
            prev_node.next = node.next
            if prev_node.next is None:
                self.tail = prev_node
        node.next = None
        return prev_node.next if prev_node else self.head

    def delete(self, val: Any, all: bool = False) -> None:
        prev_node, node = self._find_with_previous(val)
        next_node = self._delete(prev_node, node)

        while all:
            prev_node, node = self._find_with_previous(val, next_node)
            next_node = self._delete(prev_node, node)
            all = not (next_node is None)

    def clean(self) -> None:
        while self.head:
            new_head = self.head.next
            self.head.next = None
            self.head = new_head

    def len(self) -> int:
        count = 0
        node = self.head
        while node:
            count += 1
            node = node.next
        return count

    def insert(self, after_node: Node, new_node: Node) -> None:
        new_node.next = after_node.next if after_node is not None else self.head
        if after_node is None:
            self.head = new_node
        else:
            after_node.next = new_node
