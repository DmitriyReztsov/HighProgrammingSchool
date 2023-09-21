from typing import List


def print_even_values(input_list: List) -> None:
    if len(input_list) < 2:
        return
    print(input_list[1])
    print_even_values(input_list[2:])
