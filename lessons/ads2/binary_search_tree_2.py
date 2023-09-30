from typing import Any, Optional


class aBST:
    def __init__(self, depth: int = -1) -> None:
        # правильно рассчитайте размер массива для дерева глубины depth:
        self.tree_size = sum([2**x for x in range(depth + 1)])
        self.Tree = [None] * self.tree_size  # массив ключей

    def _find_node_by_key(self, key: Any, start_node_index: int) -> int:
        if start_node_index >= self.tree_size:
            return None
        if self.Tree[start_node_index] is None:
            return start_node_index * -1
        if key == self.Tree[start_node_index]:
            return start_node_index
        if key < self.Tree[start_node_index]:
            return self._find_node_by_key(key, start_node_index * 2 + 1)
        return self._find_node_by_key(key, start_node_index * 2 + 2)

    def FindKeyIndex(self, key: Any) -> Optional[int]:
        if not self.Tree:
            return None
        # ищем в массиве индекс ключа
        return self._find_node_by_key(key, 0)

    def AddKey(self, key: Any) -> int:
        # добавляем ключ в массив
        target_index = self.FindKeyIndex(key)
        if target_index is None:
            return -1
        if target_index <= 0:
            target_index *= -1
            self.Tree[target_index] = key
        return target_index
        # индекс добавленного/существующего ключа или -1 если не удалось
