from typing import List, Optional


class HashTable:
    def __init__(self, sz: int, stp: int) -> None:
        self._size = sz
        self.step = stp
        self.slots: List = [None] * self._size

    def hash_fun(self, value: str) -> int:
        # в качестве value поступают строки!
        # всегда возвращает корректный индекс слота
        return sum(bytearray(value, encoding="utf-8")) % self._size

    def seek_slot(self, value: str) -> Optional[int]:
        # находит индекс пустого слота для значения, или None
        slot = self.hash_fun(value)
        first_slot = slot
        while self.slots[slot] is not None:
            slot = (slot + self.step) % self._size
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
            slot = (slot + self.step) % self._size
            if slot == first_slot:
                return None
        return slot


class PowerSet(HashTable):
    def __init__(self, sz: int = 20000, stp: int = 3) -> None:
        super().__init__(sz, stp)

    def size(self) -> int:
        counter = 0
        for elem in self.slots:
            counter = counter + 1 if elem is not None else counter
        return counter

    def seek_slot(self, value: str) -> Optional[int]:
        # находит индекс пустого слота для значения, проверяя уникальность, или None
        slot = self.hash_fun(value)
        first_slot = slot
        while self.slots[slot] is not None:
            if self.slots[slot] == value:
                return None
            slot = (slot + self.step) % self._size
            if slot == first_slot:
                return None
        return slot

    def put(self, value: str) -> Optional[int]:
        slot = self.seek_slot(value)
        if slot is None:
            return None
        self.slots[slot] = value
        return slot

    def get(self, value: str) -> bool:
        # возвращает True если value имеется в множестве,
        # иначе False
        return self.find(value) is not None

    def remove(self, value: str) -> bool:
        # возвращает True если value удалено
        # иначе False
        slot = self.find(value)
        if slot is not None:
            self.slots[slot] = None
            return True
        return False

    def intersection(self, set2: "PowerSet") -> "PowerSet":
        # пересечение текущего множества и set2
        inter_size = max(self.size(), set2.size())
        intersection_set = PowerSet(inter_size)
        for elem in set2.slots:
            if elem is None:
                continue
            if self.get(elem):
                intersection_set.put(elem)
        return intersection_set

    def union(self, set2: "PowerSet") -> "PowerSet":
        # объединение текущего множества и set2
        union_size = self.size() + set2.size()
        union_set = PowerSet(union_size)
        for elem in self.slots:
            if elem is None:
                continue
            union_set.put(elem)
        for elem in set2.slots:
            if elem is None:
                continue
            if not self.get(elem):
                union_set.put(elem)
        return union_set

    def difference(self, set2: "PowerSet") -> "PowerSet":
        # разница текущего множества и set2
        difference_size = self.size()
        difference_set = PowerSet(difference_size)
        if self.size() == 0:
            return difference_set
        for elem in self.slots:
            if elem is None:
                continue
            difference_set.put(elem)
        for elem in set2.slots:
            if elem is None:
                continue
            difference_set.remove(elem)
        return difference_set

    def issubset(self, set2: "PowerSet") -> bool:
        # возвращает True, если set2 есть
        # подмножество текущего множества,
        # иначе False
        if self.size() < set2.size():
            return False
        for elem in set2.slots:
            if elem is None:
                continue
            if not self.get(elem):
                return False
        return True
