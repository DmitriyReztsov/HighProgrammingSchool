from lessons.ads.dynamic_array import DynArray


def _collect_python_list(d_array):
    values_list = []
    i = 0
    while True:
        try:
            values_list.append(d_array.array[i])
        except IndexError:
            break
        except ValueError:
            break
        i += 1
    return values_list


def test_insert(setup_instances_to_dynamic_array_insert):
    instances_list = setup_instances_to_dynamic_array_insert
    for data, i, check_capacity in instances_list:
        check_array = _collect_python_list(data)

        data.insert(i, 100)
        test_array = _collect_python_list(data)
        i = i if len(test_array) > i else len(test_array) - 1
        i = i if i >= 0 else len(test_array) + i - 1
        i = i if i >= 0 else 0

        assert len(check_array) + 1 == len(test_array)
        assert test_array[i] == 100
        assert len(test_array) == data.count
        assert data.capacity == check_capacity


def test_delete_resize(setup_instances_to_dynamic_array_delete):
    instances_list = setup_instances_to_dynamic_array_delete
    for data, i, check_capacity in instances_list:
        check_array = _collect_python_list(data)

        deletion_number = int(data.count / 2)
        for _ in range(deletion_number + 1):
            data.delete(i)
        test_array = _collect_python_list(data)
        check_len = len(check_array) - deletion_number - 1
        check_len = 0 if check_len < 0 else check_len

        assert check_len == len(test_array)
        assert len(test_array) == data.count
        assert data.capacity == check_capacity


def test_delete_no_resize(setup_instances_to_dynamic_array_delete_no_resize):
    instances_list = setup_instances_to_dynamic_array_delete_no_resize
    for data, i, check_element in instances_list:
        check_array = _collect_python_list(data)

        data.delete(i)
        test_array = _collect_python_list(data)
        # i = i if len(test_array) > i else len(test_array) - 1
        # i = i if i >=0 else len(test_array) + i - 1
        # i = i if i >=0 else 0

        assert set(check_array).difference(set(test_array)) == {check_element}
