from abc import ABC, abstractmethod
from typing import Self, TypeVar

Node = TypeVar("Node")


class BloomFilterABC(ABC):
    # конструктор
    @abstractmethod
    def BloomFilter(self, f_len: int) -> Self:
        """
        предусловия: нет
        постусловия: создан новый фильтр заданного размера

        """
        pass

    # команды
    @abstractmethod
    def add(self, node: Node) -> None:
        """
        предусловия: нет (ограничения на тип входных данных - строки в задании - это детали
        реализации, которые можно учесть в дочерних типах даных или при реализации)
        постусловие: хеш-функции расчитали и поставили биты в нужных разрядах

        """

    # запросы
    @abstractmethod
    def is_value(self, node: Node) -> bool:
        """
        предусловия: нет
        постусловия: нет

        """
        pass


class BloomFilter(BloomFilterABC):
    # конструктор
    def PowerSet(self, f_len: int) -> "BloomFilter":
        self.filter_len = f_len
        # создаём битовый массив длиной f_len = 32
        # количество значений для фильтра n=10
        self.bit_array = int("0", 2)
        return self

    # команды
    def add(self, str1: str) -> None:
        # добавляем строку str1 в фильтр
        self.bit_array = self._hash1(str1) | self.bit_array
        self.bit_array = self._hash2(str1) | self.bit_array

    # запросы
    def _hash1(self, str1: str) -> int:
        # 17
        code = 0
        for c in str1:
            code = code * 17 + ord(c)
        bit_position = code % self.filter_len
        bit_mask = "0" * bit_position + "1" + "0" * (self.filter_len - bit_position - 1)
        return int(bit_mask, 2)

    def _hash2(self, str1: str) -> int:
        # 223
        code = 0
        for c in str1:
            code = code * 223 + ord(c)
        bit_position = code % self.filter_len
        bit_mask = "0" * bit_position + "1" + "0" * (self.filter_len - bit_position - 1)
        return int(bit_mask, 2)

    def is_value(self, str1: str) -> bool:
        # проверка, имеется ли строка str1 в фильтре
        mask_1 = self._hash1(str1)
        mask_2 = self._hash2(str1)
        if mask_1 & self.bit_array == mask_1 and mask_2 & self.bit_array == mask_2:
            return True
        return False
