from typing import Any, List, Optional


class NativeDictionary:
    def __init__(self, sz: int) -> None:
        self.size = sz
        self.slots: List = [None] * self.size
        self.values: List = [None] * self.size

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
        while self.slots[slot] is not None:
            slot = (slot + 1) % self.size
            if slot == first_slot:
                return None
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

    def is_key(self, key: str) -> bool:
        # возвращает True если ключ имеется,
        # иначе False
        index = self._find(key)
        return index is not None and self.slots[index] is not None and self.slots[index] == key

    def put(self, key: str, value: Any) -> None:
        # гарантированно записываем
        # значение value по ключу key
        index = self._find(key) or self._seek_slot(key)
        self.slots[index] = key
        self.values[index] = value

    def get(self, key: str) -> Optional[Any]:
        # возвращает value для key,
        # или None если ключ не найден
        index = self._find(key)
        if index is None or self.slots[index] != key:
            return None
        return self.values[index]
