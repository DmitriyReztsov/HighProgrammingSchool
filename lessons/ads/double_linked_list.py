from typing import Any, List, Optional


class Node:
    def __init__(self, v: Any) -> None:
        self.value = v
        self.prev = None
        self.next = None


class LinkedList2:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_in_tail(self, item: Node) -> None:
        if self.head is None:
            self.head = item
            item.prev = None
            item.next = None
        else:
            self.tail.next = item
            item.prev = self.tail
        self.tail = item

    def find(self, val: Any, from_node: Node = None) -> Optional[Node]:
        node = self.head if from_node is None else from_node
        while node is not None:
            if node.value == val:
                return node
            node = node.next
        return None

    def find_all(self, val: Any) -> List[Node]:
        return_list = []
        node = self.head
        while node is not None:
            found_node = self.find(val, node)
            if found_node is None:
                break
            return_list.append(found_node)
            node = found_node.next
        return return_list

    def _delete(self, node: Node) -> None:
        if self.head == node and self.tail == node:
            self.head, self.tail = None, None
        elif self.head == node:
            self.head = node.next
            node.next.prev, node.next = None, None
        elif self.tail == node:
            self.tail = node.prev
            node.prev.next, node.prev = None, None
        else:
            node.next.prev, node.prev.next = node.prev, node.next
            node.prev, node.next = None, None

    def delete(self, val: Any, all: bool = False) -> None:
        if all:
            nodes = self.find_all(val)
        else:
            node = self.find(val)
            nodes = [node] if node is not None else []
        for node in nodes:
            self._delete(node)

    def clean(self):
        self.head = None
        self.tail = None

    def len(self):
        counter = 0
        cur_node = self.head
        while cur_node:
            counter += 1
            cur_node = cur_node.next
        return counter

    def insert(self, after_node: Node, new_node: Node) -> None:
        if after_node is None and self.head is None:
            self.head = new_node
            self.tail = new_node
        elif after_node is None:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        else:
            new_node.prev, new_node.next = after_node, after_node.next
            if after_node.next is not None:
                after_node.next.prev = new_node
            after_node.next = new_node
            if self.tail is after_node:
                self.tail = new_node

    def add_in_head(self, new_node):
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        if self.tail is None:
            self.tail = new_node
        self.head = new_node
