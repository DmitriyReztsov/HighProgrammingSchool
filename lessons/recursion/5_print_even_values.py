from typing import List


def print_even_values(input_list: List[int]) -> None:
    if len(input_list) == 0:
        return
    if (elem := input_list[0]) % 2 == 0:
        print(elem)
    print_even_values(input_list[1:])
