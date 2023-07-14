def _collect_python_list(l_list):
    values_list = []
    current_node = l_list.head
    while current_node:
        values_list.append(current_node.value)
        current_node = current_node.next
    return values_list


def test_find(setup_instances_to_oredered_list_find):
    instances_list = setup_instances_to_oredered_list_find
    for data, find_value, check_result in instances_list:
        check_values_list = _collect_python_list(data)

        test_result = data.find(val=find_value)

        if check_result is None:
            assert test_result is None
        else:
            assert test_result.value == check_result.value
            assert test_result is check_result
            assert check_result.value in check_values_list
            assert test_result.value in check_values_list


def test_delete(setup_instances_to_oredered_list_delete):
    instances_list = setup_instances_to_oredered_list_delete
    for (data,) in instances_list:
        check_values_list = _collect_python_list(data)

        data.delete(55)
        test_values_list = _collect_python_list(data)
        sorted_values_list = sorted(test_values_list)

        for expected, actual in zip(sorted_values_list, test_values_list):
            assert expected == actual


def test_add(setup_instances_to_oredered_list_add):
    instances_list = setup_instances_to_oredered_list_add
    for (data,) in instances_list:
        check_values_list = _collect_python_list(data)
        check_head = data.head
        check_tail = data.tail

        data.add(20)
        test_values_list = _collect_python_list(data)
        test_head = data.head
        test_tail = data.tail
        sorted_values_list = sorted(test_values_list)

        assert len(check_values_list) + 1 == len(test_values_list)

        for expected, actual in zip(sorted_values_list, test_values_list):
            assert expected == actual


def test_find_desc(setup_instances_to_oredered_list_find_desc):
    instances_list = setup_instances_to_oredered_list_find_desc
    for data, find_value, check_result in instances_list:
        check_values_list = _collect_python_list(data)

        test_result = data.find(val=find_value)

        if check_result is None:
            assert test_result is None
        else:
            assert test_result.value == check_result.value
            assert test_result is check_result
            assert check_result.value in check_values_list
            assert test_result.value in check_values_list


def test_add_desc(setup_instances_to_oredered_list_add_desc):
    instances_list = setup_instances_to_oredered_list_add_desc
    for (data,) in instances_list:
        check_values_list = _collect_python_list(data)
        check_head = data.head
        check_tail = data.tail

        data.add("20")
        test_values_list = _collect_python_list(data)
        test_head = data.head
        test_tail = data.tail
        sorted_values_list = sorted(test_values_list, reverse=True)

        assert len(check_values_list) + 1 == len(test_values_list)

        for expected, actual in zip(sorted_values_list, test_values_list):
            assert expected == actual
