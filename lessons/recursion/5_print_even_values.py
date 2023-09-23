from typing import List


def print_even_by_index(input_list: List[int], index: int, list_length: int) -> None:
    if index == list_length:
        return
    if input_list[index] % 2 == 0:
        print(input_list[index])
    print_even_by_index(input_list, index + 1, list_length)


def print_even_values(input_list: List[int]) -> None:
    print_even_by_index(input_list, 0, len(input_list))
