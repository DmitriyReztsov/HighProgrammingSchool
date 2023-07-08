def test_push_1(setup_instances_to_stack_push):
    instances_list = setup_instances_to_stack_push
    for (data,) in instances_list:
        input_list = data.stack
        check_len = len(input_list)

        data.push(100)

        test_list = data.stack

        assert check_len + 1 == len(test_list)
        assert data.size() == len(test_list)
        assert test_list[-1] == 100


def test_pop_1(setup_instances_to_stack_pop):
    instances_list = setup_instances_to_stack_pop
    for data, expected in instances_list:
        input_list = data.stack
        check_len = len(input_list) - 1 if len(input_list) > 0 else 0

        actual = data.pop()

        test_list = data.stack

        assert check_len == len(test_list)
        assert data.size() == len(test_list)
        assert actual == expected


def test_size_1(setup_instances_to_stack_size):
    instances_list = setup_instances_to_stack_size
    for data, expected in instances_list:
        input_list = data.stack
        check_len = len(input_list)

        actual = data.size()

        assert actual == expected


def test_peek_1(setup_instances_to_stack_peek):
    instances_list = setup_instances_to_stack_peek
    for data, expected in instances_list:
        input_list = data.stack
        check_len = len(input_list)

        actual = data.peek()
        test_len = len(data.stack)

        assert actual == expected
        assert check_len == test_len


def test_push_2(setup_instances_to_stack_push_2):
    instances_list = setup_instances_to_stack_push_2
    for (data,) in instances_list:
        input_list = data.stack
        check_len = len(input_list)

        data.push(100)

        test_list = data.stack

        assert check_len + 1 == len(test_list)
        assert data.size() == len(test_list)
        assert test_list[-1] == 100


def test_pop_2(setup_instances_to_stack_pop_2):
    instances_list = setup_instances_to_stack_pop_2
    for data, expected in instances_list:
        input_list = data.stack
        check_len = len(input_list) - 1 if len(input_list) > 0 else 0

        actual = data.pop()

        test_list = data.stack

        assert check_len == len(test_list)
        assert data.size() == len(test_list)
        assert actual == expected


def test_size_2(setup_instances_to_stack_size_2):
    instances_list = setup_instances_to_stack_size_2
    for data, expected in instances_list:
        input_list = data.stack
        check_len = len(input_list)

        actual = data.size()

        assert actual == expected


def test_peek_2(setup_instances_to_stack_peek_2):
    instances_list = setup_instances_to_stack_peek_2
    for data, expected in instances_list:
        input_list = data.stack
        check_len = len(input_list)

        actual = data.peek()
        test_len = len(data.stack)

        assert actual == expected
        assert check_len == test_len
