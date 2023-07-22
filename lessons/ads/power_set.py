from typing import List, Optional


class PowerSet():
    def __init__(self) -> None:
        self.step = 1
        self.slots = {}

    def size(self) -> int:
        return len(self.slots)

    def hash_fun(self, value: str) -> int:
        # в качестве value поступают строки!
        # всегда возвращает корректный индекс слота
        return hash(value)

    def seek_slot(self, value: str) -> Optional[int]:
        # находит индекс пустого слота для значения, проверяя уникальность, или None
        slot = self.hash_fun(value)
        while slot in self.slots.keys():
            if self.slots[slot] == value:
                return None
            slot = slot + self.step
        return slot

    def put(self, value: str) -> Optional[int]:
        slot = self.seek_slot(value)
        if slot is None:
            return None
        self.slots[slot] = value
        return slot

    def find(self, value: str) -> Optional[int]:
        # находит индекс слота со значением, или None
        slot = self.hash_fun(value)
        while slot in self.slots.keys():
            if self.slots[slot] == value:
                return slot
            slot = slot + self.step
        return None

    def get(self, value: str) -> bool:
        # возвращает True если value имеется в множестве,
        # иначе False
        return self.find(value) is not None

    def remove(self, value: str) -> bool:
        # возвращает True если value удалено
        # иначе False
        slot = self.find(value)
        if slot is not None:
            self.slots.pop(slot)
            return True
        return False

    def intersection(self, set2: "PowerSet") -> "PowerSet":
        # пересечение текущего множества и set2
        intersection_set = PowerSet()
        for value in set2.slots.values():
            if self.get(value):
                intersection_set.put(value)
        return intersection_set

    def union(self, set2: "PowerSet") -> "PowerSet":
        # объединение текущего множества и set2
        union_set = PowerSet()
        for value in self.slots.values():
            union_set.put(value)
        for value in set2.slots.values():
            if not self.get(value):
                union_set.put(value)
        return union_set

    def difference(self, set2: "PowerSet") -> "PowerSet":
        # разница текущего множества и set2
        difference_set = PowerSet()
        if self.size() == 0:
            return difference_set
        for value in self.slots.values():
            difference_set.put(value)
        for value in set2.slots.values():
            difference_set.remove(value)
        return difference_set

    def issubset(self, set2: "PowerSet") -> bool:
        # возвращает True, если set2 есть
        # подмножество текущего множества,
        # иначе False
        if self.size() < set2.size():
            return False
        for value in set2.slots.values():
            if not self.get(value):
                return False
        return True
