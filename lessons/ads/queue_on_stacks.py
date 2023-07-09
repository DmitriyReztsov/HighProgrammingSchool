from typing import Any


class Queue:
    def __init__(self):
        self.inbox = []
        self.outbox = []
        self.counter_in = 0
        self.counter_out = 0

    def _refil_outbox(self) -> None:
        while self.counter_in > 0:
            self.outbox.append(self.inbox.pop())
            self.counter_in -= 1
            self.counter_out += 1

    def enqueue(self, item: Any) -> None:
        # вставка в хвост
        self.inbox.append(item)
        self.counter_in += 1

    def dequeue(self) -> Any:
        # выдача из головы
        if self.counter_out == 0 and self.counter_in == 0:
            return None # если очередь пустая
        if self.counter_out == 0:
            self._refil_outbox()
        self.counter_out -= 1
        return self.outbox.pop()

    def size(self):
        return self.counter_out + self.counter_in
