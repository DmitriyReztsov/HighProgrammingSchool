from functools import reduce
from typing import Callable

from pymonad.tools import curry


@curry(4)
def curried_distance(
    cumulative_distance: int, previous_time: int, current_speed: int, current_time: int
) -> tuple[int, int]:
    return cumulative_distance + current_speed * (current_time - previous_time), current_time


def calculate(value_in: tuple[int, int] | Callable, current_value: int) -> tuple[int, int] | Callable:
    match value_in:
        case tuple():
            return curried_distance(*value_in)(current_value)
        case Callable:
            return value_in(current_value)


def calculate_distance(speed_log: list) -> int:
    distance, _ = reduce(calculate, speed_log, curried_distance(0, 0))
    return distance


if __name__ == "__main__":
    speed_log = [10, 1, 20, 2, 30, 3, 20, 5]
    assert calculate_distance(speed_log) == 100
