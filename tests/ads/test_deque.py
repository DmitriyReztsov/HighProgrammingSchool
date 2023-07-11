def test_add_front(setup_instances_to_deque_add_front):
    instances_list = setup_instances_to_deque_add_front
    for (data,) in instances_list:
        input_list = data.deque
        check_len = len(input_list)

        data.addFront(100)

        test_list = data.deque

        assert check_len + 1 == len(test_list)
        assert test_list[0] == 100


def test_add_tail(setup_instances_to_deque_add_tail):
    instances_list = setup_instances_to_deque_add_tail
    for (data,) in instances_list:
        input_list = data.deque
        check_len = len(input_list)

        data.addTail(100)

        test_list = data.deque

        assert check_len + 1 == len(test_list)
        assert test_list[-1] == 100


def test_remove_front(setup_instances_to_deque_remove_front):
    instances_list = setup_instances_to_deque_remove_front
    for data, expected in instances_list:
        input_list = data.deque
        check_len = len(input_list) if input_list else 1

        actual = data.removeFront()

        test_list = data.deque

        assert check_len - 1 == len(test_list)
        assert actual == expected


def test_remove_tail(setup_instances_to_deque_remove_tail):
    instances_list = setup_instances_to_deque_remove_tail
    for data, expected in instances_list:
        input_list = data.deque
        check_len = len(input_list) if input_list else 1

        actual = data.removeTail()

        test_list = data.deque

        assert check_len - 1 == len(test_list)
        assert actual == expected
