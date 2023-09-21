from typing import List


def print_even_indexes(input_list: List) -> None:
    if len(input_list) < 2:
        return
    print(input_list[1])
    input_list.pop(0)
    input_list.pop(0)
    print_even_indexes(input_list)
