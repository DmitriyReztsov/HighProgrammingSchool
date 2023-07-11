from typing import Any, List


class Deque:
    def __init__(self):
        # инициализация внутреннего хранилища
        # лучше использовать collections.deque как оптимизированную
        # для извлечение и добавления элементов в начало очереди
        self.deque: List = []

    def addFront(self, item: Any):
        # добавление в голову
        self.deque.insert(0, item)

    def addTail(self, item: Any):
        # добавление в хвост
        self.deque.append(item)

    def removeFront(self):
        # удаление из головы
        if self.size() == 0:
            return None  # если очередь пуста
        return self.deque.pop(0)

    def removeTail(self):
        # удаление из хвоста
        if self.size() == 0:
            return None  # если очередь пуста
        return self.deque.pop()

    def size(self):
        return len(self.deque)
