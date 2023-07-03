from lessons.ADS.linked_list_star import sum_list_values


def _collect_python_list(l_list):
    values_list = []
    current_node = l_list.head
    while current_node:
        values_list.append(current_node.value)
        current_node = current_node.next
    return values_list


def test_sum_lists_values_positive(setup_instances_to_sum_positive):
    instances_list = setup_instances_to_sum_positive
    for list_1, list_2 in instances_list:
        values_list_1 = _collect_python_list(list_1)
        values_list_2 = _collect_python_list(list_2)
        check_values_list = [
            elem_1 + elem_2 for elem_1, elem_2 in zip(values_list_1, values_list_2)
        ]

        new_list = sum_list_values(list_1, list_2)
        new_values_list = _collect_python_list(new_list)

        for new_value, check_value in zip(new_values_list, check_values_list):
            assert new_value == check_value

        if check_values_list:
            assert new_list.head.value == check_values_list[0]
            assert new_list.tail.value == list_1.tail.value + list_2.tail.value
        else:
            assert new_list.head is None
            assert new_list.tail is None


def test_sum_lists_values_negative(setup_instances_to_sum_negative):
    instances_list = setup_instances_to_sum_negative
    for list_1, list_2 in instances_list:
        new_list = sum_list_values(list_1, list_2)

        assert new_list is None
