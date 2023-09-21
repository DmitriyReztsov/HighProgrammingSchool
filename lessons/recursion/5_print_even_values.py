from typing import List


def print_even_values(input_list: List[int]) -> None:
    if len(input_list) == 0:
        return
    if input_list[0] % 2 == 0:
        print(input_list.pop(0))
    else:
        input_list.pop(0)
    print_even_values(input_list)
