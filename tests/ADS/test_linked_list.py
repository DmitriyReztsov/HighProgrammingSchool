from lessons.ADS.linked_list import LinkedList, Node


def test_delete(setup_instances):
    instances_list = setup_instances
    for data, find_value in instances_list:
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        initial_len = len(values_list)

        data.delete(val=55)
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        if find_value is None or find_value == 12:
            assert len(values_list) == initial_len
        else:
            assert len(values_list) == (initial_len - 1)


def test_delete_multi(setup_instances_multi):
    instances_list = setup_instances_multi
    for data, find_value, multi_count in instances_list:
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        initial_len = len(values_list)

        data.delete(val=find_value, all=True)
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        assert len(values_list) == (initial_len - multi_count)


def test_clean(setup_instances_to_clean):
    instances_list = setup_instances_to_clean
    for data, list_len in instances_list:
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        assert len(values_list) == list_len

        data.clean()
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        assert len(values_list) == 0


def test_find_all(setup_instances_to_find_all):
    instances_list = setup_instances_to_find_all
    for data, find_val, find_count in instances_list:
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        return_list = data.find_all(find_val)
        found_values_list = []
        for node in return_list:
            found_values_list.append(node.value)

        assert len(return_list) == find_count
        assert values_list.count(find_val) == find_count
        if find_count == 0:
            assert len(set(found_values_list)) == 0
        else:
            assert len(set(found_values_list)) == 1


def test_len(setup_instances_to_len):
    instances_list = setup_instances_to_len
    for data, check_len in instances_list:
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        test_len = data.len()

        assert test_len == len(values_list)
        assert test_len == check_len


def test_insert(setup_instances_to_insert):
    instances_list = setup_instances_to_insert
    for data, after_node in instances_list:
        values_list = []
        current_node = data.head
        while current_node:
            values_list.append(current_node.value)
            current_node = current_node.next

        new_node = Node("new_node")
        data.insert(after_node, new_node)

        inserted_values_list = []
        current_node = data.head
        while current_node:
            inserted_values_list.append(current_node.value)
            current_node = current_node.next

        assert len(values_list) + 1 == len(inserted_values_list)
        if after_node is None:
            assert data.head == new_node
        else:
            assert after_node.next == new_node
