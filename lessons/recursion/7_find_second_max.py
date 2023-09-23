from typing import List, Tuple


def first_two_max(array: List[int], current_index, first_max, second_max, array_length) -> Tuple:
    if current_index == array_length:
        return first_max, second_max

    current_elem = array[current_index]
    first_max, second_max = first_two_max(array, current_index + 1, first_max, second_max, array_length)
    if current_elem >= first_max:
        first_max, second_max = current_elem, first_max
    elif first_max > current_elem >= second_max:
        first_max, second_max = first_max, current_elem
    return first_max, second_max


def find_second_max(array: List[int]) -> int:
    array_length = len(array)
    if array_length <= 1:
        return
    
    if array[0] >= array[1]:
        first_max, second_max = array[0], array[1]
    else:
        first_max, second_max = array[1], array[0]
    return first_two_max(array, 2, first_max, second_max, array_length)[1]
