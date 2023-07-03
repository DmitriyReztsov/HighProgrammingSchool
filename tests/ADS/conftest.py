from pytest import fixture

from lessons.ADS.linked_list import LinkedList, Node


@fixture
def setup_instances_to_delete():
    instances_list = []
    s_list = LinkedList()
    instances_list.append((s_list, None))

    n1 = Node(12)
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12))

    n1 = Node(12)
    n2 = Node(55)
    n1.next = n2
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n1.next = n2
    n2.next = n3
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 55))

    return instances_list


@fixture
def setup_instances_to_delete_multi():
    instances_list = []
    n1 = Node(12)
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n1
    # list, value to delete, counter of deletion, head, tail
    instances_list.append((s_list, 12, 1, None, None))

    n1 = Node(12)
    n2 = Node(12)
    n1.next = n2
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 12, 2, None, None))

    n1 = Node(12)
    n2 = Node(55)
    n1.next = n2
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, 1, n1, n1))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n1.next = n2
    n2.next = n3
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 12, 1, n2, n3))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n4 = Node(55)
    n5 = Node(12)
    n6 = Node(55)
    n7 = Node(99)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 55, 3, n1, n7))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n4 = Node(55)
    n5 = Node(12)
    n6 = Node(55)
    n7 = Node(99)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 12, 2, n2, n7))

    n1 = Node(12)
    n2 = Node(12)
    n3 = Node(12)
    n4 = Node(12)
    n5 = Node(12)
    n6 = Node(12)
    n7 = Node(12)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 12, 7, None, None))

    s_list = LinkedList()
    instances_list.append((s_list, 12, 0, None, None))

    n1 = Node(12)
    n2 = Node(12)
    n3 = Node(12)
    n4 = Node(12)
    n5 = Node(12)
    n6 = Node(12)
    n7 = Node(12)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 13, 0, n1, n7))

    n1 = Node(121)
    n2 = Node(12)
    n3 = Node(12)
    n4 = Node(12)
    n5 = Node(12)
    n6 = Node(12)
    n7 = Node(12)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 12, 6, n1, n1))

    n1 = Node(121)
    n2 = Node(12)
    n3 = Node(12)
    n4 = Node(12)
    n5 = Node(12)
    n6 = Node(12)
    n7 = Node(121)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 12, 5, n1, n7))

    n1 = Node(12)
    n2 = Node(12)
    n3 = Node(12)
    n4 = Node(12)
    n5 = Node(12)
    n6 = Node(12)
    n7 = Node(121)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 12, 6, n7, n7))
    return instances_list


@fixture
def setup_instances_to_clean():
    instances_list = []
    s_list = LinkedList()
    instances_list.append((s_list, 0))

    n1 = Node(12)
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 1))

    n1 = Node(12)
    n2 = Node(55)
    n1.next = n2
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 2))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n1.next = n2
    n2.next = n3
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 3))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n4 = Node(55)
    n5 = Node(12)
    n6 = Node(55)
    n7 = Node(99)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 7))

    return instances_list


@fixture
def setup_instances_to_find_all():
    instances_list = []
    s_list = LinkedList()
    instances_list.append((s_list, 55, 0))

    n1 = Node(12)
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, 1))

    n1 = Node(12)
    n2 = Node(55)
    n1.next = n2
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, 1))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n1.next = n2
    n2.next = n3
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 55, 1))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n4 = Node(55)
    n5 = Node(12)
    n6 = Node(55)
    n7 = Node(99)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 55, 3))

    return instances_list


@fixture
def setup_instances_to_len():
    instances_list = []
    s_list = LinkedList()
    instances_list.append((s_list, 0))

    n1 = Node(12)
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 1))

    n1 = Node(12)
    n2 = Node(55)
    n1.next = n2
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 2))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n1.next = n2
    n2.next = n3
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 3))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n4 = Node(55)
    n5 = Node(12)
    n6 = Node(55)
    n7 = Node(99)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, 7))

    return instances_list


@fixture
def setup_instances_to_insert():
    instances_list = []
    s_list = LinkedList()
    instances_list.append((s_list, None, "head", "tail"))

    n1 = Node(12)
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, n1, n1, "tail"))

    n1 = Node(12)
    n2 = Node(55)
    n1.next = n2
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, n2, n1, "tail"))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n1.next = n2
    n2.next = n3
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, n2, n1, n3))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n4 = Node(55)
    n5 = Node(12)
    n6 = Node(55)
    n7 = Node(99)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, None, "head", n7))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n4 = Node(55)
    n5 = Node(12)
    n6 = Node(55)
    n7 = Node(99)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, n4, n1, n7))

    n1 = Node(12)
    n2 = Node(55)
    n3 = Node(100)
    n4 = Node(55)
    n5 = Node(12)
    n6 = Node(55)
    n7 = Node(99)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list = LinkedList()
    s_list.head = n1
    s_list.tail = n7
    instances_list.append((s_list, n7, n1, "tail"))

    return instances_list


@fixture
def setup_instances_to_sum_positive():
    instances_list = []
    s_list_1 = LinkedList()
    s_list_2 = LinkedList()
    instances_list.append((s_list_1, s_list_2))

    n1 = Node(1)
    s_list_1 = LinkedList()
    s_list_1.head = n1
    s_list_1.tail = n1

    n1 = Node(1)
    s_list_2 = LinkedList()
    s_list_2.head = n1
    s_list_2.tail = n1
    instances_list.append((s_list_1, s_list_2))

    n1 = Node(1)
    n2 = Node(2)
    n1.next = n2
    s_list_1 = LinkedList()
    s_list_1.head = n1
    s_list_1.tail = n2

    n1 = Node(1)
    n2 = Node(2)
    n1.next = n2
    s_list_2 = LinkedList()
    s_list_2.head = n1
    s_list_2.tail = n2
    instances_list.append((s_list_1, s_list_2))

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)
    n7 = Node(7)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list_1 = LinkedList()
    s_list_1.head = n1
    s_list_1.tail = n7

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)
    n7 = Node(7)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list_2 = LinkedList()
    s_list_2.head = n1
    s_list_2.tail = n7
    instances_list.append((s_list_1, s_list_2))

    return instances_list


@fixture
def setup_instances_to_sum_negative():
    instances_list = []
    s_list_1 = LinkedList()

    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)
    n7 = Node(7)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    n5.next = n6
    n6.next = n7
    s_list_2 = LinkedList()
    s_list_2.head = n1
    s_list_2.tail = n7
    instances_list.append((s_list_1, s_list_2))
    return instances_list
