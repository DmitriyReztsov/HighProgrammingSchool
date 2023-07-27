from typing import Any, Optional


class NativeCache:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size
        self.hits = [0] * self.size

    def hash_fun(self, key: str) -> int:
        # в качестве key поступают строки!
        # всегда возвращает корректный индекс слота
        return (
            sum([v * (i + 1) for i, v in enumerate(bytearray(key, encoding="utf-8"))])
            % self.size
        )

    def _seek_slot(self, key: str) -> Optional[int]:
        # находит индекс пустого слота для значения, или None
        slot = self.hash_fun(key)
        first_slot = slot
        minor_slot = slot
        while self.slots[slot] is not None and self.slots[slot] != key:
            minor_slot = slot if self.hits[minor_slot] > self.hits[slot] else minor_slot
            slot = (slot + 1) % self.size
            if slot == first_slot:
                return minor_slot
        return slot

    def _find(self, key: str) -> Optional[int]:
        # находит индекс слота со значением, или None
        slot = self.hash_fun(key)
        first_slot = slot
        while self.slots[slot] != key:
            slot = (slot + 1) % self.size
            if slot == first_slot:
                return None
        return slot

    def put(self, key: str, value: Any) -> None:
        # гарантированно записываем
        # значение value по ключу key
        index = self._seek_slot(key)
        self.slots[index] = key
        self.values[index] = value
        self.hits[index] += 1

    def get(self, key: str) -> Optional[Any]:
        # возвращает value для key,
        # или None если ключ не найден
        index = self._find(key)
        if index is None or self.slots[index] != key:
            return None
        return self.values[index]
