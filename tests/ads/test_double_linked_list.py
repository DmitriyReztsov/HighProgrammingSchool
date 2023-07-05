def _collect_python_list(l_list):
    values_list = []
    current_node = l_list.head
    while current_node:
        values_list.append(current_node.value)
        current_node = current_node.next
    return values_list


def test_find(setup_instances_to_find):
    instances_list = setup_instances_to_find
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


def test_find_all(setup_instances_to_find_all_2):
    instances_list = setup_instances_to_find_all_2
    for data, find_value, check_result in instances_list:
        test_result = data.find_all(val=find_value)

        assert test_result == check_result
        for test_value, check_value in zip(test_result, check_result):
            assert test_value == check_value
            assert test_value is check_value
            assert test_value.value == check_value.value


def test_delete(setup_instances_to_delete_2):
    instances_list = setup_instances_to_delete_2
    for data, find_value, head, tail in instances_list:
        check_values_list = _collect_python_list(data)

        data.delete(val=find_value)
        test_values_list = _collect_python_list(data)

        try:
            check_values_list.remove(find_value)
            assert check_values_list == test_values_list
        except ValueError:
            assert check_values_list == test_values_list
        assert data.head is head
        assert data.tail is tail


def test_delete_all(setup_instances_to_delete_all_2):
    instances_list = setup_instances_to_delete_all_2
    for data, find_value, head, tail in instances_list:
        check_values_list = _collect_python_list(data)

        data.delete(val=find_value, all=True)
        test_values_list = _collect_python_list(data)

        try:
            check_values_list = [
                elem for elem in check_values_list if elem != find_value
            ]
            assert check_values_list == test_values_list
        except ValueError:
            assert check_values_list == test_values_list
        assert data.head is head
        assert data.tail is tail


def test_insert(setup_instances_to_insert_2):
    instances_list = setup_instances_to_insert_2
    for data, after_node, new_node, head, tail in instances_list:
        check_values_list = _collect_python_list(data)
        check_prev = after_node or data.tail
        check_next = after_node.next if after_node else None

        data.insert(after_node, new_node)
        test_values_list = _collect_python_list(data)

        assert len(check_values_list) + 1 == len(test_values_list)
        assert data.head is head
        assert data.tail is tail
        assert new_node.prev is check_prev
        assert new_node.next is check_next

        for index, elem in enumerate(test_values_list):
            assert index == elem


def test_add_in_head(setup_instances_to_add_in_head):
    instances_list = setup_instances_to_add_in_head
    for data, new_node, head, tail in instances_list:
        check_values_list = _collect_python_list(data)
        check_prev = None
        check_next = data.head

        data.add_in_head(new_node)
        test_values_list = _collect_python_list(data)

        assert len(check_values_list) + 1 == len(test_values_list)
        assert data.head is head
        assert data.tail is tail
        assert new_node.prev is check_prev
        assert new_node.next is check_next


def test_clean(setup_instances_to_clean_2):
    instances_list = setup_instances_to_clean_2
    for data, head, tail, length in instances_list:
        data.clean()
        test_values_list = _collect_python_list(data)

        assert len(test_values_list) == length
        assert data.head is None
        assert data.tail is None


def test_len(setup_instances_to_len):
    instances_list = setup_instances_to_len
    for data, length in instances_list:
        data.len()
        test_values_list = _collect_python_list(data)

        assert len(test_values_list) == length
