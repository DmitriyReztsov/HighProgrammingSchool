from typing import Any, List


class Node:
    def __init__(self, v: Any) -> None:
        self.value = v
        self.prev = None
        self.next = None


class OrderedList:
    def __init__(self, asc: bool) -> None:
        self.head = None
        self.tail = None
        self.__ascending = asc

    def compare(self, v1: Node, v2: Node) -> int:
        if v1.value > v2.value:
            return 1
        if v1.value < v2.value:
            return -1
        return 0

    def _insert(self, after_node: Node, new_node: Node) -> None:
        if after_node is None and self.head is None:
            self.head = new_node
            self.tail = new_node
        elif after_node is None:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:
            new_node.prev, new_node.next = after_node, after_node.next
            if after_node.next is not None:
                after_node.next.prev = new_node
            after_node.next = new_node
            if self.tail is after_node:
                self.tail = new_node

    def _find(self, node: Node, exact: bool) -> Node:
        head_node = self.head
        prev_node = None
        mult_asc = {True: 1, False: -1}
        while (
            head_node
            and self.compare(node, head_node) * mult_asc[self.__ascending] == 1
        ):
            prev_node = head_node
            head_node = head_node.next
        return head_node if exact else prev_node

    def add(self, value: int) -> None:
        node = Node(value)
        head_node = self._find(node, False)
        self._insert(after_node=head_node, new_node=node)

    def find(self, val: int) -> Node:
        node = Node(val)
        place_node = self._find(node, True)
        if place_node and place_node.value == val:
            return place_node
        return None

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

    def delete(self, val: int) -> None:
        found_node = self.find(val)
        if found_node and found_node.value == val:
            self._delete(found_node)

    def clean(self, asc: bool):
        self.__ascending = asc
        self.head = None
        self.tail = None

    def len(self) -> int:
        counter = 0
        cur_node = self.head
        while cur_node:
            counter += 1
            cur_node = cur_node.next
        return counter

    def get_all(self) -> List:
        r = []
        node = self.head
        while node != None:
            r.append(node)
            node = node.next
        return r


class OrderedStringList(OrderedList):
    def __init__(self, asc: bool) -> None:
        super(OrderedStringList, self).__init__(asc)

    def compare(self, v1: Node, v2: Node) -> int:
        if v1.value.strip() > v2.value.strip():
            return 1
        if v1.value.strip() < v2.value.strip():
            return -1
        return 0
