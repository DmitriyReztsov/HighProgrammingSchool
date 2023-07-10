from typing import Any

from lessons.ads.stack import Stack


class Queue:
    def __init__(self):
        self.inbox = Stack()
        self.outbox = Stack()

    def _refil_outbox(self) -> None:
        while self.inbox.size() > 0:
            self.outbox.push(self.inbox.pop())

    def enqueue(self, item: Any) -> None:
        # вставка в хвост
        self.inbox.push(item)

    def dequeue(self) -> Any:
        # выдача из головы
        if self.outbox.size() == 0 and self.inbox.size() == 0:
            return None  # если очередь пустая
        if self.outbox.size() == 0:
            self._refil_outbox()
        return self.outbox.pop()

    def size(self):
        return self.outbox.size() + self.inbox.size()
