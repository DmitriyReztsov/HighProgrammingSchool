from typing import List, Tuple


def first_two_max(array: List[int]) -> Tuple:
    if len(array) == 2:
        if array[0] >= array[1]:
            first_max, second_max = array
        else:
            second_max, first_max = array
        return first_max, second_max

    current_elem = array[0]
    first_two_array = first_two_max(array[1:])
    if current_elem >= first_two_array[0]:
        first_max, second_max = current_elem, first_two_array[0]
    elif first_two_array[0] > current_elem >= first_two_array[1]:
        first_max, second_max = first_two_array[0], current_elem
    else:
        first_max, second_max = first_two_array
    return first_max, second_max


def find_second_max(array: List[int]) -> int:
    return first_two_max(array)[1]
