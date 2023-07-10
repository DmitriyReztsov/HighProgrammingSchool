from typing import Any, List

from lessons.ads.queue_on_list import Queue


def rotate_queue(queue: Queue, rotate_num: int) -> None:
    if rotate_num > queue.size():
        queue.queue.extend([None] * (rotate_num - queue.size()))

    for _ in range(rotate_num):
        queue.enqueue(queue.dequeue())
