from typing import List


class Heap:
    def __init__(self) -> None:
        self.HeapArray = []  # хранит неотрицательные числа-ключи

    def _find_empty_slot(self) -> int:
        return self.HeapArray.index(None) if self.HeapArray[-1] is None else -1

    def _find_right_place_down_to_up(self, elem_index: int) -> None:
        if elem_index == 0:
            return
        parent_index = (elem_index - 1) // 2
        while (
            elem_index > 0 and self.HeapArray[parent_index] < self.HeapArray[elem_index]
        ):
            self.HeapArray[parent_index], self.HeapArray[elem_index] = (
                self.HeapArray[elem_index],
                self.HeapArray[parent_index],
            )
            elem_index = parent_index
            parent_index = (elem_index - 1) // 2

    def MakeHeap(self, a: List, depth: int) -> None:
        # создаём массив кучи HeapArray из заданного
        # размер массива выбираем на основе глубины depth
        self.heap_size = sum([2**x for x in range(depth + 1)])
        self.HeapArray = [None] * self.heap_size
        for elem in a:
            if not self.Add(elem):
                break

    def _find_right_place_up_to_down(self, parent_index: int) -> None:
        if self.HeapArray[parent_index] is None:
            return
        l_child_index = 2 * parent_index + 1
        r_child_index = 2 * parent_index + 2
        if (
            l_child_index >= self.heap_size
            or r_child_index >= self.heap_size  # r_child_index - just in case
        ) or (
            self.HeapArray[l_child_index] is None
            and self.HeapArray[r_child_index] is None
        ):
            return
        if self.HeapArray[l_child_index] is None or (
            self.HeapArray[r_child_index] is not None
            and self.HeapArray[l_child_index] < self.HeapArray[r_child_index]
        ):
            direction_index = r_child_index
        elif self.HeapArray[r_child_index] is None or (
            self.HeapArray[l_child_index] is not None
            and self.HeapArray[l_child_index] >= self.HeapArray[r_child_index]
        ):
            direction_index = l_child_index
        else:
            return

        if self.HeapArray[parent_index] < self.HeapArray[direction_index]:
            self.HeapArray[parent_index], self.HeapArray[direction_index] = (
                self.HeapArray[direction_index],
                self.HeapArray[parent_index],
            )
            return self._find_right_place_up_to_down(direction_index)
        return

    def GetMax(self) -> int:
        # вернуть значение корня и перестроить кучу
        if not self.HeapArray or self.HeapArray[0] is None:
            return -1  # если куча пуста
        empty_slot = self._find_empty_slot()
        last_index = empty_slot - 1 if empty_slot != -1 else empty_slot
        max_element = self.HeapArray[0]

        self.HeapArray[0], self.HeapArray[last_index] = self.HeapArray[last_index], None
        self._find_right_place_up_to_down(0)
        return max_element

    def Add(self, key: int) -> bool:
        # добавляем новый элемент key в кучу и перестраиваем её
        empty_slot = self._find_empty_slot()
        if empty_slot == -1:
            return False
        self.HeapArray[empty_slot] = key
        self._find_right_place_down_to_up(empty_slot)
        return True
