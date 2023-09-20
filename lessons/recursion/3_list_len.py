from typing import List


def length_list_recursively(incoming_list: List) -> int:
    if not incoming_list:
        return 0
    incoming_list.pop(0)
    return 1 + length_list_recursively(incoming_list)
