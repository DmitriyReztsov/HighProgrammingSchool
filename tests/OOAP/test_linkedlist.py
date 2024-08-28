from lessons.OOAP.TwoWayList import LinkedList


def test_create_boundedstack():
    tw_list = LinkedList().LinkedList()

    assert tw_list.get_head_status() == 0
    assert hasattr(tw_list, "get_head_status")
    assert not hasattr(tw_list, "get_left_status")
    assert not hasattr(tw_list, "put_left")


def test_add():
    tw_list = LinkedList().LinkedList()

    tw_list.add_to_empty("12")
    assert tw_list.get_add_empty_status() == 1
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 1
    assert tw_list._list == ["12"]

    tw_list.add_to_empty(12)
    assert tw_list.get_add_empty_status() == 2
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 1
    assert tw_list._list == ["12"]

    tw_list.add_tail("tail")
    assert tw_list.get_add_tail_status() == 1
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 2
    assert tw_list._list == ["12", "tail"]

    tw_list.add_tail("tail_2")
    assert tw_list.get_add_tail_status() == 1
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 3
    assert tw_list._list == ["12", "tail", "tail_2"]


def test_put():
    tw_list = LinkedList().LinkedList()
    tw_list.add_to_empty("12")

    tw_list.put_right("right")
    assert tw_list.get_put_right_status() == 1
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 2
    assert tw_list._list == ["12", "right"]

    tw_list.put_right(11)
    assert tw_list.get_put_right_status() == 1
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 3
    assert tw_list._list == ["12", 11, "right"]

    tw_list.tail()
    tw_list.put_right("tail")
    assert tw_list.get_put_right_status() == 1
    assert tw_list._cursor == 3
    assert tw_list._head == 1
    assert tw_list._tail == 4
    assert tw_list._list == ["12", 11, "right", "tail"]
    tw_list.head()


def test_move_cursor():
    tw_list = LinkedList().LinkedList()
    tw_list._list = ["left", "12", 11, "right", "left tail", "tail"]
    tw_list._cursor = 1
    tw_list._head = 1
    tw_list._tail = 6

    tw_list.left()
    assert tw_list.get_left_status() == 2
    assert tw_list._cursor == 1

    tw_list.right()
    assert tw_list.get_right_status() == 1
    assert tw_list._cursor == 2

    tw_list.right()
    tw_list.right()
    tw_list.right()
    assert tw_list.get_right_status() == 1
    assert tw_list._cursor == 5

    tw_list.right()
    assert tw_list.get_right_status() == 1
    assert tw_list._cursor == 6

    tw_list.right()
    assert tw_list.get_right_status() == 2
    assert tw_list._cursor == 6

    tw_list.left()
    assert tw_list.get_left_status() == 1
    assert tw_list._cursor == 5

    tw_list.left()
    tw_list.left()
    tw_list.left()
    tw_list.left()
    assert tw_list.get_left_status() == 1
    assert tw_list._cursor == 1

    tw_list.left()
    assert tw_list.get_left_status() == 2
    assert tw_list._cursor == 1


def test_remove():
    tw_list = LinkedList().LinkedList()
    tw_list._list = ["left", "12", 11, "right", "left tail", "tail"]
    tw_list._cursor = 1
    tw_list._head = 1
    tw_list._tail = 6

    tw_list.remove()
    assert tw_list.get_remove_status() == 1
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 5
    assert tw_list._list == ["12", 11, "right", "left tail", "tail"]

    tw_list.right()
    tw_list.right()
    assert tw_list._cursor == 3

    tw_list.remove()
    assert tw_list.get_remove_status() == 1
    assert tw_list._cursor == 3
    assert tw_list._head == 1
    assert tw_list._tail == 4
    assert tw_list._list == ["12", 11, "left tail", "tail"]

    tw_list.tail()
    assert tw_list._cursor == 4

    tw_list.remove()
    assert tw_list.get_remove_status() == 1
    assert tw_list._cursor == 3
    assert tw_list._head == 1
    assert tw_list._tail == 3
    assert tw_list._list == ["12", 11, "left tail"]

    tw_list.remove()
    tw_list.remove()
    tw_list.remove()
    assert tw_list.get_remove_status() == 1
    assert tw_list._cursor == 0
    assert tw_list._head == 0
    assert tw_list._tail == 0
    assert tw_list._list == []

    tw_list.remove()
    assert tw_list.get_remove_status() == 2


def test_clear():
    tw_list = LinkedList().LinkedList()
    tw_list._list = ["left", "12", 11, "right", "left tail", "tail"]
    tw_list._cursor = 1
    tw_list._head = 1
    tw_list._tail = 6

    tw_list.clear()
    assert tw_list._list == []
    assert tw_list._cursor == 0
    assert tw_list._head == 0
    assert tw_list._tail == 0


def test_replace():
    tw_list = LinkedList().LinkedList()
    tw_list._list = ["left", "12", 11, "right", "left tail", "tail"]
    tw_list._cursor = 1
    tw_list._head = 1
    tw_list._tail = 6

    tw_list.replace("NEW")
    assert tw_list.get_replace_status() == 1
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 6
    assert tw_list._list == ["NEW", "12", 11, "right", "left tail", "tail"]


def test_find():
    tw_list = LinkedList().LinkedList()
    tw_list._list = ["left", "12", 11, "right", "left tail", "tail"]
    tw_list._cursor = 1
    tw_list._head = 1
    tw_list._tail = 6

    tw_list.find("left")
    assert tw_list.get_find_status() == 2
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 6

    tw_list.find("right")
    assert tw_list.get_find_status() == 1
    assert tw_list._cursor == 4
    assert tw_list._head == 1
    assert tw_list._tail == 6

    tw_list.find("unknown")
    assert tw_list.get_find_status() == 2
    assert tw_list._cursor == 4
    assert tw_list._head == 1
    assert tw_list._tail == 6


def test_remove_all():
    tw_list = LinkedList().LinkedList()
    tw_list._list = ["12", "left", "12", 11, "right", "12", "left tail", "tail", "12"]
    tw_list._cursor = 1
    tw_list._head = 1
    tw_list._tail = 9

    tw_list.remove_all("12")
    assert tw_list._cursor == 5
    assert tw_list._head == 1
    assert tw_list._tail == 5
    assert tw_list._list == ["left", 11, "right", "left tail", "tail"]


def test_get():
    tw_list = LinkedList().LinkedList()

    value = tw_list.get()
    assert value == 0
    assert tw_list.get_get_status() == 2
    assert tw_list._cursor == 0
    assert tw_list._head == 0
    assert tw_list._tail == 0
    assert tw_list.size() == 0

    tw_list._list = ["12", "left", "12", 11, "right", "12", "left tail", "tail", "12t"]
    tw_list._cursor = 1
    tw_list._head = 1
    tw_list._tail = 9

    value = tw_list.get()
    assert value == "12"
    assert tw_list.get_get_status() == 1
    assert tw_list._cursor == 1
    assert tw_list._head == 1
    assert tw_list._tail == 9

    value = tw_list._cursor = 4
    tw_list.get()
    assert value == 4
    assert tw_list.get_get_status() == 1

    tw_list.tail()
    value = tw_list.get()
    assert value == "12t"
    assert tw_list.get_get_status() == 1
    assert tw_list._cursor == 9

    assert tw_list.size() == 9


def test_is_tail_is_head():
    tw_list = LinkedList().LinkedList()

    assert tw_list.is_head() is True
    assert tw_list.is_tail() is True
    assert tw_list.is_value() is False

    tw_list._list = ["12", "left", "12", 11, "right", "12", "left tail", "tail", "12t"]
    tw_list._cursor = 1
    tw_list._head = 1
    tw_list._tail = 9

    assert tw_list.is_head() is True
    assert tw_list.is_tail() is False
    assert tw_list.is_value() is True

    tw_list._cursor = 4
    assert tw_list.is_head() is False
    assert tw_list.is_tail() is False
    assert tw_list.is_value() is True

    tw_list.tail()
    assert tw_list.is_head() is False
    assert tw_list.is_tail() is True
    assert tw_list.is_value() is True
