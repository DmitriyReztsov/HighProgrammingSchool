from typing import Any

from lessons.ads.double_linked_list import LinkedList2


class NodeD:
    def __init__(self, v: Any) -> None:
        self.value = v
        self._next = None
        self._prev = None

    def __setattr__(self, __name: str, __value: "NodeD") -> None:
        if __name == "next":
            self._next = __value
        if __name == "prev":
            self._prev = __value
        else:
            return super().__setattr__(__name, __value)

    def __getattribute__(self, __name: str) -> Any:
        if __name == "next":
            return self._next if not isinstance(self._next, DummyNode) else None
        if __name == "prev":
            return self._prev if not isinstance(self._prev, DummyNode) else None
        return super().__getattribute__(__name)


class DummyNode(NodeD):
    def __init__(self) -> None:
        super().__init__("DUMMY")


class DummyLinkedList(LinkedList2):
    def __init__(self) -> None:
        self._head = DummyNode()
        self._tail = DummyNode()
        self._head._next = self._tail
        self._tail._prev = self._head
        self._head._prev = self._tail._next = None

    def __setattr__(self, __name: str, __value: NodeD) -> None:
        if __name == "head":
            __value._prev = self._head
            __value._prev._next = __value
        elif __name == "tail":
            __value._next = self._tail
            __value._next._prev = __value
        else:
            return super().__setattr__(__name, __value)

    def __getattribute__(self, __name: str) -> Any:
        if __name == "head":
            return self._head._next if self._head._next is not self._tail else None
        if __name == "tail":
            return self._tail._prev if self._tail._prev is not self._head else None
        return super().__getattribute__(__name)

    def add_in_tail(self, item: NodeD) -> None:
        item._next = self._tail
        item._prev = self._tail._prev
        item._prev._next = item
        item._next._prev = item

    def _delete(self, node: NodeD) -> None:
        node._next._prev = node._prev
        node._prev._next = node._next

    def clean(self) -> None:
        self._head._next = self._tail
        self._tail._prev = self._head
        self._head._prev = self._tail._next = None

    def insert(self, after_node: NodeD, new_node: NodeD) -> None:
        if after_node is None:
            self.add_in_tail(new_node)
        else:
            new_node._next = after_node._next
            new_node._prev = after_node
            new_node._prev._next = new_node
            new_node._next._prev = new_node

    def add_in_head(self, new_node: NodeD) -> None:
        new_node._prev = self._head
        new_node._next = self._head._next
        new_node._prev._next = new_node
        new_node._next._prev = new_node
