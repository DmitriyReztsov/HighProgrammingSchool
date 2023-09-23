from typing import List


def print_even_by_index(input_list: List, print_index, list_length):
    if print_index < list_length:
        print(input_list[print_index])
        print_even_by_index(input_list, print_index + 2, list_length)


def print_even_indexes(input_list: List) -> None:
    list_length = len(input_list)
    if list_length > 1:
        print_even_by_index(input_list, 1, list_length)
