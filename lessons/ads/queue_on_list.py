from typing import Any


class Queue:
    def __init__(self):
        # инициализация хранилища данных
        self.queue = []

    def enqueue(self, item: Any) -> None:
        # вставка в хвост
        self.queue.append(item)

    def dequeue(self) -> Any:
        # выдача из головы
        if self.size() == 0:
            return None  # если очередь пустая
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)  # размер очереди
