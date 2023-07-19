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

    def is_key(self, key: str) -> bool:
        # возвращает True если ключ имеется,
        # иначе False
        return self.slots[self.hash_fun(key)] is not None and self.slots[self.hash_fun(key)] == key

    def put(self, key: str, value: Any) -> None:
        # гарантированно записываем
        # значение value по ключу key
        index = self.hash_fun(key)
        self.slots[index] = key
        self.values[index] = value

    def get(self, key: str) -> Optional[Any]:
        # возвращает value для key,
        # или None если ключ не найден
        index = self.hash_fun(key)
        if self.slots[index] != key:
            return None
        return self.values[index]
