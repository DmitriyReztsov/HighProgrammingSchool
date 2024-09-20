from abc import ABC, abstractmethod
from typing import Self, TypeVar

Node = TypeVar("Node")


class HashTableABC(ABC):
    NEXT_SLOT_STEP = 1
    NOT_IN_TABLE_IND = -1

    ADD_NIL: int = 0
    ADD_OK: int = 1
    ADD_ERR: int = 2

    REMOVE_NIL: int = 0
    REMOVE_OK: int = 1
    REMOVE_ERR: int = 2

    # конструктор
    @abstractmethod
    def HashTable(self, table_size: int) -> Self:
        """
        предусловия: нет
        постусловия: создана новая таблица заданного размера

        """
        pass

    # команды
    @abstractmethod
    def add(self, node: Node) -> None:
        """
        предусловия: в таблице найден свободный слот
        постусловие: элемент добавлен в таблицу

        """

    @abstractmethod
    def remove(self, node: Node) -> None:
        """
        предусловие: элемент присутствует в таблице
        постусловие: элемент удален таблицы

        """
        pass

    # запросы
    @abstractmethod
    def is_in_table(self, node: Node) -> bool:
        """
        предусловия: нет
        постусловия: нет

        """
        pass

    @abstractmethod
    def get_add_status(self) -> int:
        pass

    @abstractmethod
    def get_remove_status(self) -> int:
        pass


class HashTable(HashTableABC):
    # конструктор
    def HashTable(self, table_size: int) -> Self:
        self._table_size = table_size
        self.clear()
        return self

    def clear(self) -> None:
        self._slots: list = [None] * self._table_size
        self._step: int = self.NEXT_SLOT_STEP
        self._add_status: int = self.ADD_NIL
        self._remove_status: int = self.REMOVE_NIL

    # команды
    def add(self, node: Node) -> None:
        slot = self._seek_empty_slot(node)
        if slot == self.NOT_IN_TABLE_IND:
            self._add_status = self.ADD_ERR
        self._slots[slot] = node
        self._add_status = self.ADD_OK

    def remove(self, node: Node) -> None:
        slot = self._find_node_slot(node)
        if slot == self.NOT_IN_TABLE_IND:
            self._remove_status = self.REMOVE_ERR
        self._slots[slot] = None
        self._remove_status = self.REMOVE_OK

    # запросы
    def _hash(self, node: Node) -> int:
        """сам тип Node должен, видимо, содержать метод hash"""
        raise NotImplementedError

    def _seek_empty_slot(self, node: Node) -> int:
        # находит индекс пустого слота для значения, или -1
        slot = self._hash(node)
        first_slot = slot
        while self.slots[slot] is not None:
            slot = (slot + self._step) % self._table_size
            if slot == first_slot:
                return self.NOT_IN_TABLE_IND
        return slot

    def _find_node_slot(self, node: Node) -> int:
        # находит индекс слота со значением, или -1
        slot = self._hash(node)
        first_slot = slot
        while self._slots[slot] != node:
            slot = (slot + self._step) % self._table_size
            if slot == first_slot:
                return self.NOT_IN_TABLE_IND
        return slot

    def is_in_table(self, node: Node) -> bool:
        return self._find_node_slot(node) > self.NOT_IN_TABLE_IND

    def get_add_status(self) -> int:
        return self._add_status

    def get_remove_status(self) -> int:
        return self._remove_status
