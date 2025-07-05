from functools import reduce


def compare_and_store(stored_t: tuple[int, int], scnd: int) -> tuple[int, int]:
    if stored_t[0] is None or stored_t[0] < scnd:
        stored_t = (scnd, stored_t[0])
    elif stored_t[1] is None or stored_t[1] < scnd:
        stored_t = (stored_t[0], scnd)
    return stored_t


def second_max(l: list[int]) -> int | None:
    return reduce(compare_and_store, l, (None, None))[1]


if __name__ == "__main__":
    assert second_max([5, 4, 3, 2, 5]) == 5
    assert second_max([1, 3, 2, 6, 4, 4, 5, 5, 5, 7]) == 6
    assert second_max([1, 2, 3, 4, 5, 6, 7]) == 6
    assert second_max([7, 6, 5, 4, 3, 2, 1]) == 6
