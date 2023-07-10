from lessons.ads.round_queue import rotate_queue


def test_equeue_rotate(setup_instances_to_queue_rotate):
    instances_list = setup_instances_to_queue_rotate
    for data, nuber_rotate in instances_list:
        rotate_queue(data, nuber_rotate)

        assert True
