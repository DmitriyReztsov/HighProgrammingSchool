from typing import List, Optional


class HashTable:
    def __init__(self, sz: int, stp: int) -> None:
        self.size = sz
        self.step = stp
        self.slots: List = [None] * self.size

    def hash_fun(self, value: str) -> int:
        # в качестве value поступают строки!
        # всегда возвращает корректный индекс слота
        return sum(bytearray(value, encoding='utf-8')) % self.size

    def seek_slot(self, value: str) -> Optional[int]:
        # находит индекс пустого слота для значения, или None
        slot = self.hash_fun(value)
        first_slot = slot
        while self.slots[slot] is not None:
            slot = (slot + self.step) % self.size
            if slot == first_slot:
                return None
        return slot

    def put(self, value: str) -> Optional[int]:
        # записываем значение по хэш-функции
        # возвращается индекс слота или None,
        # если из-за коллизий элемент не удаётся
        # разместить
        slot = self.seek_slot(value)
        if slot is None:
            return None
        self.slots[slot] = value
        return slot

    def find(self, value: str) -> Optional[int]:
        # находит индекс слота со значением, или None
        slot = self.hash_fun(value)
        first_slot = slot
        while self.slots[slot] != value:
            slot = (slot + self.step) % self.size
            if slot == first_slot:
                return None
        return slot
