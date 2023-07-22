import time

from lessons.ads.power_set import PowerSet


def test_put():
    test_set = PowerSet()
    put_1 = test_set.put("a")
    put_2 = test_set.put("a")
    assert put_1 is not None
    assert put_2 is None


def test_remove():
    test_set = PowerSet()
    test_set.put("a")
    test_set.put("b")
    test_set.put("bb")
    test_set.put("ab")
    test_set.put("ba")

    assert test_set.size() == 5

    del_1 = test_set.remove("b")
    del_2 = test_set.remove("bab")

    assert del_1 is True
    assert del_2 is False


def test_intersection():
    test_set_1 = PowerSet()
    test_set_1.put("a")
    test_set_1.put("aa")
    test_set_1.put("ab")
    test_set_1.put("ba")
    test_set_1.put("bab")
    test_set_1.put("aba")

    test_set_2 = PowerSet()
    test_set_2.put("a")
    test_set_2.put("aca")
    test_set_2.put("acb")
    test_set_2.put("ba")
    test_set_2.put("bacb")
    test_set_2.put("aba")

    test_set_3 = PowerSet()
    test_set_3.put("c")

    inter_1 = test_set_1.intersection(test_set_2)
    inter_2 = test_set_1.intersection(test_set_3)
    inter_3 = test_set_3.intersection(test_set_2)

    assert {"a", "ba", "aba"} == set(inter_1.slots.values())
    assert set(inter_2.slots.values()) == set()
    assert set(inter_3.slots.values()) == set()


def test_union():
    test_set_1 = PowerSet()
    test_set_1.put("a")
    test_set_1.put("aa")
    test_set_1.put("ab")
    test_set_1.put("ba")
    test_set_1.put("bab")
    test_set_1.put("aba")

    test_set_2 = PowerSet()
    test_set_2.put("a")
    test_set_2.put("aca")
    test_set_2.put("acb")
    test_set_2.put("ba")
    test_set_2.put("bacb")
    test_set_2.put("aba")

    test_set_3 = PowerSet()

    union_1 = test_set_1.union(test_set_2)
    union_2 = test_set_1.union(test_set_3)
    union_3 = test_set_3.union(test_set_2)

    assert {"a", "ba", "aba", "aa", "ab", "bab", "aca", "acb", "bacb"} == set(union_1.slots.values())
    assert test_set_1.size() + test_set_2.size() - 3 == union_1.size()

    assert {"a", "aa", "ab", "ba", "bab", "aba"} == set(union_2.slots.values())
    assert test_set_1.size() == union_2.size()

    assert {"a", "aca", "acb", "ba", "bacb", "aba"} == set(union_3.slots.values())
    assert test_set_2.size() == union_3.size()


def test_difference():
    test_set_1 = PowerSet()
    test_set_1.put("a")
    test_set_1.put("aa")
    test_set_1.put("ab")
    test_set_1.put("ba")
    test_set_1.put("bab")
    test_set_1.put("aba")

    test_set_2 = PowerSet()
    test_set_2.put("a")
    test_set_2.put("aca")
    test_set_2.put("acb")
    test_set_2.put("ba")
    test_set_2.put("bacb")
    test_set_2.put("aba")

    test_set_3 = PowerSet()

    difference_1 = test_set_1.difference(test_set_2)
    difference_2 = test_set_1.difference(test_set_3)
    difference_3 = test_set_3.difference(test_set_2)

    assert {"aa", "ab", "bab"} == set(difference_1.slots.values())
    assert {"a", "aa", "ab", "ba", "bab", "aba"} == set(difference_2.slots.values())
    assert difference_3.size() == 0


def test_issubset():
    test_set_1 = PowerSet()
    test_set_1.put("1")
    test_set_1.put("2")
    test_set_1.put("3")
    test_set_1.put("4")

    test_set_2 = PowerSet()
    test_set_2.put("1")
    test_set_2.put("2")
    test_set_2.put("3")
    test_set_2.put("4")
    test_set_2.put("5")
    test_set_2.put("6")

    test_set_3 = PowerSet()
    test_set_3.put("1")
    test_set_3.put("2")

    test_set_4 = PowerSet()
    test_set_4.put("1")
    test_set_4.put("3")
    test_set_4.put("4")
    test_set_4.put("5")

    is_subset_1 = test_set_1.issubset(test_set_2)
    is_subset_2 = test_set_1.issubset(test_set_3)
    is_subset_3 = test_set_1.issubset(test_set_4)

    assert is_subset_1 is False
    assert is_subset_2 is True
    assert is_subset_3 is False


def test_time():
    test_set_1 = PowerSet()
    start_time = time.monotonic()

    for i in range(20001):
        test_set_1.put(str(i))
    end_time = time.monotonic()
    diff_time = end_time - start_time
    assert diff_time < 2
