from typing import Any


class Queue:
    def __init__(self):
        # инициализация хранилища данных
        self.queue = []
        self.counter = 0

    def enqueue(self, item: Any) -> None:
        # вставка в хвост
        self.queue.append(item)
        self.counter += 1

    def dequeue(self) -> Any:
        # выдача из головы
        if self.counter == 0:
            return None # если очередь пустая
        self.counter -= 1
        return self.queue.pop(0)

    def size(self):
        return self.counter # размер очереди
