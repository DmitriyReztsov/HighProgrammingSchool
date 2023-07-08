import ctypes
from typing import Any, List


class DynArray:
    DOWN_RESIZE_CAPACITY_CONDITION = 0.5
    DOWN_RESIZE_CAPACITY_RATE = 1.5
    MINIMUM_CAPACITY = 16

    def __init__(self) -> None:
        self.count = 0
        self.capacity = self.MINIMUM_CAPACITY
        self.array = self.make_array(self.capacity)

    def __len__(self) -> None:
        return self.count

    def make_array(self, new_capacity: int) -> List:
        ar = (new_capacity * ctypes.py_object)()
        return ar

    def __getitem__(self, i: int) -> Any:
        if i < 0 or i >= self.count:
            raise IndexError("Index is out of bounds")
        return self.array[i]

    def resize(self, new_capacity: int) -> None:
        if new_capacity < 16:
            new_capacity = self.MINIMUM_CAPACITY
        new_array = self.make_array(new_capacity)
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def append(self, itm: Any) -> None:
        if self.count == self.capacity:
            self.resize(2 * self.capacity)
        self.array[self.count] = itm
        self.count += 1

    def _validate_index(self, i: int, from_insert: bool = False) -> int:
        if i < 0 or i > self.count or (not from_insert and i == self.count):
            raise IndexError
        return i

    def insert(self, i: int, itm: Any) -> None:
        i = self._validate_index(i, True)
        if self.count == self.capacity:
            self.resize(2 * self.capacity)
        for index in range(self.count, i, -1):
            self.array[index] = self.array[index - 1]
        self.array[i] = itm
        self.count += 1

    def delete(self, i: int) -> None:
        # удаляем объект в позиции i
        # В тестах используется схема, когда увеличение буфера происходит в два раза, а уменьшение в полтора раза
        # (текущее значение размера буфера делится на 1.5, и результат приводится к целому типу, никаких округлений!).
        # При этом сохраняем минимальную ёмкость 16 элементов.
        # Увеличение буфера выполняем, когда он весь полностью заполнен, и выполняется попытка добавления.
        # Сокращение буфера выполняем, когда его заполненность после операции удаления станет строго меньше,
        # чем заданный процент заполнения. В тестах используйте этот процент равным 50%.
        i = self._validate_index(i)
        if self.count == 0:
            return
        for index in range(i, self.count - 1):
            self.array[index] = self.array[index + 1]
        self.array[self.count - 1] = ctypes.py_object()
        self.count -= 1

        if self.count < int(self.capacity * self.DOWN_RESIZE_CAPACITY_CONDITION):
            self.resize(int(self.capacity / self.DOWN_RESIZE_CAPACITY_RATE))
