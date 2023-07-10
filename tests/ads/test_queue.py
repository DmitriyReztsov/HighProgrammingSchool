def _collect_python_list(q_list):
    values_list = []
    current_node = q_list.queue.head
    while current_node:
        values_list.append(current_node.value)
        current_node = current_node.next
    return values_list


def test_enqueue_1(setup_instances_to_queue_enqueue):
    instances_list = setup_instances_to_queue_enqueue
    for (data,) in instances_list:
        input_list = _collect_python_list(data)
        check_len = len(input_list)

        data.enqueue(100)

        test_list = _collect_python_list(data)

        assert check_len + 1 == len(test_list)
        assert test_list[-1] == 100


def test_dequeue(setup_instances_to_queue_dequeue):
    instances_list = setup_instances_to_queue_dequeue
    for data, expected in instances_list:
        input_list = _collect_python_list(data)
        check_len = len(input_list)

        actual = data.dequeue()

        test_list = _collect_python_list(data)
        actual_len = 0 if len(test_list) == 0 else len(test_list) + 1

        assert check_len == actual_len
        assert actual == expected


def test_enqueue_2(setup_instances_to_queue_enqueue_2):
    instances_list = setup_instances_to_queue_enqueue_2
    for (data,) in instances_list:
        input_list = data.queue
        check_len = len(input_list)

        data.enqueue(100)

        test_list = data.queue

        assert check_len + 1 == len(test_list)
        assert test_list[-1] == 100


def test_dequeue_2(setup_instances_to_queue_dequeue_2):
    instances_list = setup_instances_to_queue_dequeue_2
    for data, expected in instances_list:
        input_list = data.queue
        check_len = len(input_list)

        actual = data.dequeue()

        test_list = data.queue
        actual_len = 0 if len(test_list) == 0 else len(test_list) + 1

        assert check_len == actual_len
        assert actual == expected


def test_enqueue_3(setup_instances_to_queue_enqueue_3):
    instances_list = setup_instances_to_queue_enqueue_3
    for (data,) in instances_list:
        input_list = data.inbox.stack + data.outbox.stack
        check_len = len(input_list)

        data.enqueue(100)

        test_list = data.inbox.stack + data.outbox.stack

        assert check_len + 1 == len(test_list)
        assert test_list[-1] == 100
        assert data.size() == len(test_list)


def test_dequeue_3(setup_instances_to_queue_dequeue_3):
    instances_list = setup_instances_to_queue_dequeue_3
    for data, expected in instances_list:
        input_list = data.inbox.stack + data.outbox.stack
        check_len = len(input_list)

        actual = data.dequeue()

        test_list = data.inbox.stack + data.outbox.stack
        actual_len = 0 if len(test_list) == 0 else len(test_list) + 1

        assert check_len == actual_len
        assert actual == expected
