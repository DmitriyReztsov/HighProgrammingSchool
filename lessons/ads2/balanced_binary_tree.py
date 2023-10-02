from math import ceil, log2
from typing import List


def _make_balanced_tree(
    array: List, balanced_array: List, left_index: int, right_index: int, parent_index: int
) -> List:
    pivot_index = ceil((right_index - left_index) / 2) + left_index
    balanced_array[parent_index] = array[pivot_index]

    if left_index == right_index:
        return

    left_child_index = parent_index * 2 + 1
    _make_balanced_tree(
        array, balanced_array, left_index, pivot_index - 1, left_child_index
    )

    right_child_index = parent_index * 2 + 2
    _make_balanced_tree(
        array, balanced_array, pivot_index + 1, right_index, right_child_index
    )


def GenerateBBSTArray(a: List) -> List:
    depth = ceil(log2((len(a) + 1) / 2))
    balanced_array = [None] * (2 ** (depth + 1) - 1)
    a.sort()
    left_index = 0
    right_index = len(a) - 1

    _make_balanced_tree(a, balanced_array, left_index, right_index, 0)
    return balanced_array
