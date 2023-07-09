from typing import Any, List


class RoundQueue:
    def __init__(self, num_slots: int, filled_queue: List) -> None:
        self.num_slots = num_slots
        self.slots = filled_queue[:self.num_slots]
        self.start = 0
        self.end = len(self.slots) - 1
        self.slots.extend([None] * (num_slots - len(self.slots)))

    def enqueue(self, value: Any) -> None:
        self.end = (self.end + 1) % self.num_slots
        self.slots[self.end] = value

    def dequeue(self) -> Any:
        value = self.slots[self.start]
        self.slots[self.start] = None
        self.start = (self.start + 1) % self.num_slots
        return value
    

def rotate_queue() -> None:
    r_queue = RoundQueue(num_slots=10, filled_queue=[0, 1, 2, 3, 4, 5])
    for _ in range(11):
        elem = r_queue.dequeue()
        r_queue.enqueue(elem)
        print(r_queue.slots)
