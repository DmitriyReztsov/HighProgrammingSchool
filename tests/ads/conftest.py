from pytest import fixture

from lessons.ads.double_linked_list import LinkedList2
from lessons.ads.double_linked_list import Node as Node2
from lessons.ads.double_linked_list_star import DummyLinkedList, NodeD
from lessons.ads.dynamic_array import DynArray
from lessons.ads.linked_list import LinkedList, Node
from lessons.ads.stack import Stack
from lessons.ads.stack_FIFO import Stack as StackFIFO


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


@fixture
def setup_instances_to_find():
    instances_list = []
    s_list = LinkedList2()
    instances_list.append((s_list, 12, None))

    n1 = Node2(12)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, n1))

    n1 = Node2(12)
    n2 = Node2(55)
    n1.next = n2
    n2.prev = n1
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, n2))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 55, n2))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(100)
    n4 = Node2(99)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 5500, None))

    return instances_list


@fixture
def setup_instances_to_find_all_2():
    instances_list = []
    s_list = LinkedList2()
    instances_list.append((s_list, 12, []))

    n1 = Node2(12)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, [n1]))

    n1 = Node2(12)
    n2 = Node2(55)
    n1.next = n2
    n2.prev = n1
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, [n2]))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 55, [n2]))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(100)
    n4 = Node2(55)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 55, [n2, n4]))

    return instances_list


@fixture
def setup_instances_to_delete_2():
    instances_list = []
    s_list = LinkedList2()
    instances_list.append((s_list, 12, None, None))

    n1 = Node2(12)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, None, None))

    n1 = Node2(12)
    n2 = Node2(55)
    n1.next, n2.prev = n2, n1
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, n1, n1))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(2100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 55, n1, n3))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(2100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 12, n2, n3))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(2100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 2100, n1, n2))

    return instances_list


@fixture
def setup_instances_to_delete_all_2():
    instances_list = []
    s_list = LinkedList2()
    instances_list.append((s_list, 12, None, None))

    n1 = Node2(12)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, None, None))

    n1 = Node2(55)
    n2 = Node2(55)
    n1.next, n2.prev = n2, n1
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, None, None))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(55)
    n4 = Node2(200)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 55, n1, n4))

    n1 = Node2(12)
    n2 = Node2(55)
    n3 = Node2(200)
    n4 = Node2(55)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 55, n1, n3))

    n1 = Node2(55)
    n2 = Node2(12)
    n3 = Node2(55)
    n4 = Node2(200)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 55, n2, n4))

    return instances_list


@fixture
def setup_instances_to_insert_2():
    instances_list = []
    s_list = LinkedList2()
    n1 = Node2(0)
    instances_list.append((s_list, None, n1, n1, n1))

    n1 = Node2(0)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    n2 = Node2(1)
    instances_list.append((s_list, None, n2, n1, n2))

    n1 = Node2(0)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    n2 = Node2(1)
    instances_list.append((s_list, n1, n2, n1, n2))

    n1 = Node2(0)
    n2 = Node2(1)
    n1.next, n2.prev = n2, n1
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n2
    n3 = Node2(2)
    instances_list.append((s_list, None, n3, n1, n3))

    n1 = Node2(0)
    n2 = Node2(2)
    n1.next, n2.prev = n2, n1
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n2
    n3 = Node2(1)
    instances_list.append((s_list, n1, n3, n1, n2))

    n1 = Node2(0)
    n2 = Node2(1)
    n1.next, n2.prev = n2, n1
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n2
    n3 = Node2(2)
    instances_list.append((s_list, n2, n3, n1, n3))

    n1 = Node2(0)
    n2 = Node2(2)
    n3 = Node2(3)
    n4 = Node2(4)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    n5 = Node2(1)
    instances_list.append((s_list, n1, n5, n1, n4))

    n1 = Node2(0)
    n2 = Node2(1)
    n3 = Node2(3)
    n4 = Node2(4)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    n5 = Node2(2)
    instances_list.append((s_list, n2, n5, n1, n4))

    n1 = Node2(0)
    n2 = Node2(1)
    n3 = Node2(2)
    n4 = Node2(3)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    n5 = Node2(4)
    instances_list.append((s_list, n4, n5, n1, n5))

    n1 = Node2(0)
    n2 = Node2(1)
    n3 = Node2(2)
    n4 = Node2(3)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    n5 = Node2(4)
    instances_list.append((s_list, None, n5, n1, n5))

    return instances_list


@fixture
def setup_instances_to_add_in_head():
    instances_list = []
    s_list = LinkedList2()
    n1 = Node2(0)
    instances_list.append((s_list, n1, n1, n1))

    n1 = Node2(0)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    n2 = Node2(1)
    instances_list.append((s_list, n2, n2, n1))

    n1 = Node2(0)
    n2 = Node2(1)
    n1.next, n2.prev = n2, n1
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n2
    n3 = Node2(2)
    instances_list.append((s_list, n3, n3, n2))

    return instances_list


@fixture
def setup_instances_to_clean_2():
    instances_list = []
    s_list = LinkedList2()
    instances_list.append((s_list, None, None, 0))

    n1 = Node2(0)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, None, None, 0))

    n1 = Node2(0)
    n2 = Node2(1)
    n3 = Node2(2)
    n4 = Node2(3)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, None, None, 0))

    return instances_list


@fixture
def setup_instances_to_len_2():
    instances_list = []
    s_list = LinkedList2()
    instances_list.append((s_list, 0))

    n1 = Node2(0)
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 1))

    n1 = Node2(0)
    n2 = Node2(1)
    n3 = Node2(2)
    n4 = Node2(3)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = LinkedList2()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 4))

    return instances_list


@fixture
def setup_instances_to_add_in_tail():
    instances_list = []
    s_list = DummyLinkedList()
    n1 = NodeD(0)
    instances_list.append((s_list, n1, n1, n1))

    n1 = NodeD(0)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    n2 = NodeD(1)
    instances_list.append((s_list, n2, n1, n2))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    n3 = NodeD(2)
    instances_list.append((s_list, n3, n1, n3))

    return instances_list


@fixture
def setup_instances_to_delete_3():
    instances_list = []
    s_list = DummyLinkedList()
    instances_list.append((s_list, 12, None, None))

    n1 = NodeD(12)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, None, None))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, n1, n1))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(2100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 55, n1, n3))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(2100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 12, n2, n3))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(2100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 2100, n1, n2))

    return instances_list


@fixture
def setup_instances_to_delete_all_3():
    instances_list = []
    s_list = DummyLinkedList()
    instances_list.append((s_list, 12, None, None))

    n1 = NodeD(12)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, None, None))

    n1 = NodeD(55)
    n2 = NodeD(55)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, None, None))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(55)
    n4 = NodeD(200)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 55, n1, n4))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(200)
    n4 = NodeD(55)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 55, n1, n3))

    n1 = NodeD(55)
    n2 = NodeD(12)
    n3 = NodeD(55)
    n4 = NodeD(200)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 55, n2, n4))

    return instances_list


@fixture
def setup_instances_to_find_3():
    instances_list = []
    s_list = DummyLinkedList()
    instances_list.append((s_list, 12, None))

    n1 = NodeD(12)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, n1))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n1.next = n2
    n2.prev = n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, n2))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 55, n2))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(100)
    n4 = NodeD(99)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 5500, None))

    return instances_list


@fixture
def setup_instances_to_find_all_3():
    instances_list = []
    s_list = DummyLinkedList()
    instances_list.append((s_list, 12, []))

    n1 = NodeD(12)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, 12, [n1]))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n1.next = n2
    n2.prev = n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    instances_list.append((s_list, 55, [n2]))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(100)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n3
    instances_list.append((s_list, 55, [n2]))

    n1 = NodeD(12)
    n2 = NodeD(55)
    n3 = NodeD(100)
    n4 = NodeD(55)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, 55, [n2, n4]))

    return instances_list


@fixture
def setup_instances_to_clean_3():
    instances_list = []
    s_list = DummyLinkedList()
    instances_list.append((s_list, None, None, 0))

    n1 = NodeD(0)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    instances_list.append((s_list, None, None, 0))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n3 = NodeD(2)
    n4 = NodeD(3)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    instances_list.append((s_list, None, None, 0))

    return instances_list


@fixture
def setup_instances_to_insert_3():
    instances_list = []
    s_list = DummyLinkedList()
    n1 = NodeD(0)
    instances_list.append((s_list, None, n1, n1, n1))

    n1 = NodeD(0)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    n2 = NodeD(1)
    instances_list.append((s_list, None, n2, n1, n2))

    n1 = NodeD(0)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    n2 = NodeD(1)
    instances_list.append((s_list, n1, n2, n1, n2))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    n3 = NodeD(2)
    instances_list.append((s_list, None, n3, n1, n3))

    n1 = NodeD(0)
    n2 = NodeD(2)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    n3 = NodeD(1)
    instances_list.append((s_list, n1, n3, n1, n2))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    n3 = NodeD(2)
    instances_list.append((s_list, n2, n3, n1, n3))

    n1 = NodeD(0)
    n2 = NodeD(2)
    n3 = NodeD(3)
    n4 = NodeD(4)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    n5 = NodeD(1)
    instances_list.append((s_list, n1, n5, n1, n4))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n3 = NodeD(3)
    n4 = NodeD(4)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    n5 = NodeD(2)
    instances_list.append((s_list, n2, n5, n1, n4))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n3 = NodeD(2)
    n4 = NodeD(3)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    n5 = NodeD(4)
    instances_list.append((s_list, n4, n5, n1, n5))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n3 = NodeD(2)
    n4 = NodeD(3)
    n1.next, n2.prev = n2, n1
    n2.next, n3.prev = n3, n2
    n3.next, n4.prev = n4, n3
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n4
    n5 = NodeD(4)
    instances_list.append((s_list, None, n5, n1, n5))

    return instances_list


@fixture
def setup_instances_to_add_in_head_3():
    instances_list = []
    s_list = DummyLinkedList()
    n1 = NodeD(0)
    instances_list.append((s_list, n1, n1, n1))

    n1 = NodeD(0)
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n1
    n2 = NodeD(1)
    instances_list.append((s_list, n2, n2, n1))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    n3 = NodeD(2)
    instances_list.append((s_list, n3, n3, n2))

    return instances_list


@fixture
def setup_instances_to_dynamic_array_insert():
    instances_list = []
    da = DynArray()
    instances_list.append((da, 0, 16))

    da = DynArray()
    for i in range(5):
        da.append(i)
    instances_list.append((da, 5, 16))

    da = DynArray()
    for i in range(16):
        da.append(i)
    instances_list.append((da, 2, 16 * 2))

    da = DynArray()
    for i in range(16):
        da.append(i)
    instances_list.append((da, 16, 16 * 2))

    return instances_list


@fixture
def setup_instances_to_dynamic_array_delete():
    instances_list = []
    da = DynArray()
    for i in range(5):
        da.append(i)
    instances_list.append((da, 1, 16))

    da = DynArray()
    for i in range(32):
        da.append(i)
    instances_list.append((da, 15, 21))

    da = DynArray()
    for i in range(16):
        da.append(i)
    instances_list.append((da, 5, 16))

    return instances_list


@fixture
def setup_instances_to_dynamic_array_delete_no_resize():
    instances_list = []
    da = DynArray()
    for i in range(5):
        da.append(i)
    instances_list.append((da, 4, 4))

    da = DynArray()
    for i in range(32):
        da.append(i)
    instances_list.append((da, 2, 2))

    da = DynArray()
    for i in range(16):
        da.append(i)
    instances_list.append((da, 15, 15))

    return instances_list


@fixture
def setup_instances_to_stack_push():
    instances_list = []
    stack = Stack()
    instances_list.append((stack,))

    stack = Stack()
    stack.stack = [0, 1, 2, 3]
    instances_list.append((stack,))

    return instances_list


@fixture
def setup_instances_to_stack_pop():
    instances_list = []
    stack = Stack()
    instances_list.append((stack, None))

    stack = Stack()
    stack.stack = [0, 1, 2, 3]
    instances_list.append((stack, 3))

    return instances_list


@fixture
def setup_instances_to_stack_size():
    instances_list = []
    stack = Stack()
    instances_list.append((stack, 0))

    stack = Stack()
    stack.stack = [0, 1, 2, 3]
    instances_list.append((stack, 4))

    return instances_list


@fixture
def setup_instances_to_stack_peek():
    instances_list = []
    stack = Stack()
    instances_list.append((stack, None))

    stack = Stack()
    stack.stack = [0, 1, 2, 3]
    instances_list.append((stack, 3))

    return instances_list


@fixture
def setup_instances_to_stack_push_2():
    instances_list = []
    stack = StackFIFO()
    instances_list.append((stack,))

    stack = StackFIFO()
    stack.stack = [0, 1, 2, 3]
    instances_list.append((stack,))

    return instances_list


@fixture
def setup_instances_to_stack_pop_2():
    instances_list = []
    stack = StackFIFO()
    instances_list.append((stack, None))

    stack = StackFIFO()
    stack.stack = [0, 1, 2, 3]
    instances_list.append((stack, 0))

    return instances_list


@fixture
def setup_instances_to_stack_size_2():
    instances_list = []
    stack = StackFIFO()
    instances_list.append((stack, 0))

    stack = StackFIFO()
    stack.stack = [0, 1, 2, 3]
    instances_list.append((stack, 4))

    return instances_list


@fixture
def setup_instances_to_stack_peek_2():
    instances_list = []
    stack = StackFIFO()
    instances_list.append((stack, None))

    stack = StackFIFO()
    stack.stack = [0, 1, 2, 3]
    instances_list.append((stack, 0))

    return instances_list


@fixture
def setup_instances_to_queue_enqueue():
    from lessons.ads.queue import DummyLinkedList, NodeD, Queue

    instances_list = []
    queue = Queue()
    instances_list.append((queue,))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    queue = Queue()
    queue.queue = s_list
    instances_list.append((queue,))

    return instances_list


@fixture
def setup_instances_to_queue_dequeue():
    from lessons.ads.queue import DummyLinkedList, NodeD, Queue

    instances_list = []
    queue = Queue()
    instances_list.append((queue, None))

    n1 = NodeD(0)
    n2 = NodeD(1)
    n1.next, n2.prev = n2, n1
    s_list = DummyLinkedList()
    s_list.head = n1
    s_list.tail = n2
    queue = Queue()
    queue.queue = s_list
    instances_list.append((queue, 0))

    return instances_list


@fixture
def setup_instances_to_queue_enqueue_2():
    from lessons.ads.queue_on_list import Queue

    instances_list = []
    queue = Queue()
    instances_list.append((queue,))

    queue = Queue()
    queue.queue = [0, 1, 2]
    queue.counter = len(queue.queue)
    instances_list.append((queue,))

    return instances_list


@fixture
def setup_instances_to_queue_dequeue_2():
    from lessons.ads.queue_on_list import Queue

    instances_list = []
    queue = Queue()
    instances_list.append((queue, None))

    queue = Queue()
    queue.queue = [0, 1, 2, 3]
    queue.counter = len(queue.queue)
    instances_list.append((queue, 0))

    return instances_list


@fixture
def setup_instances_to_queue_enqueue_3():
    from lessons.ads.queue_on_stacks import Stack, Queue

    instances_list = []
    queue = Queue()
    instances_list.append((queue,))

    queue = Queue()
    queue.inbox = Stack()
    queue.inbox.stack = [0, 1, 2]
    instances_list.append((queue,))

    return instances_list


@fixture
def setup_instances_to_queue_dequeue_3():
    from lessons.ads.queue_on_stacks import Stack, Queue

    instances_list = []
    queue = Queue()
    instances_list.append((queue, None))

    queue = Queue()
    queue.inbox = Stack()
    queue.inbox.stack = [0, 1, 2, 3]
    instances_list.append((queue, 0))

    queue = Queue()
    queue.inbox = Stack()
    queue.inbox.stack = [4, 5, 6, 7]
    queue.outbox = Stack()
    queue.outbox.stack = [3, 2, 1, 0]
    instances_list.append((queue, 0))
    instances_list.append((queue, 1))
    instances_list.append((queue, 2))
    instances_list.append((queue, 3))
    instances_list.append((queue, 4))

    return instances_list


@fixture
def setup_instances_to_queue_rotate():
    from lessons.ads.queue_on_list import Queue

    instances_list = []
    queue = Queue()
    queue.queue = [0, 1, 2, 3]
    instances_list.append((queue, 10))

    return instances_list
