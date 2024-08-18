from lessons.OOAP.BoundedStack import BoundedStack


def test_create_boundedstack():
    stack = BoundedStack().BoundedStack()

    assert stack.stack_limit() == 32
    assert stack.get_peek_status() == 0
    assert stack.get_pop_status() == 0
    assert stack.get_push_status() == 0

    stack_2 = BoundedStack().BoundedStack(5)

    assert stack_2.stack_limit() == 5
    assert stack_2.get_peek_status() == 0
    assert stack_2.get_pop_status() == 0
    assert stack_2.get_push_status() == 0


def test_push():
    stack: BoundedStack = BoundedStack().BoundedStack(5)

    stack.push(1)
    assert stack.get_push_status() == 1
    assert stack.size() == 1

    stack.push(2)
    assert stack.get_push_status() == 1
    assert stack.size() == 2

    stack.push(3)
    assert stack.get_push_status() == 1
    assert stack.size() == 3

    stack.push(4)
    assert stack.get_push_status() == 1
    assert stack.size() == 4

    stack.push(5)
    assert stack.get_push_status() == 1
    assert stack.size() == 5

    stack.push(6)
    assert stack.get_push_status() == 2
    assert stack.size() == 5

    assert stack._stack == [1, 2, 3, 4, 5]


def test_pop():
    stack: BoundedStack = BoundedStack().BoundedStack(5)

    stack._stack = [1, 2, 3, 4, 5]
    
    assert stack.size() == 5
    stack.pop()
    assert stack.get_pop_status() == 1

    assert stack.size() == 4
    stack.pop()
    assert stack.get_pop_status() == 1

    assert stack.size() == 3
    stack.pop()
    assert stack.get_pop_status() == 1

    assert stack.size() == 2
    stack.pop()
    assert stack.get_pop_status() == 1
    assert stack.size() == 1

    stack.pop()
    assert stack.get_pop_status() == 1
    assert stack.size() == 0

    stack.pop()
    assert stack.get_pop_status() == 2
    assert stack.size() == 0


def test_peek():
    stack: BoundedStack = BoundedStack().BoundedStack(5)

    stack._stack = [1, 2, 3, 4, 5]

    assert stack.size() == 5
    assert stack.peek() == 5
    assert stack.get_peek_status() == 1

    assert stack.size() == 5
    stack.pop()
    assert stack.peek() == 4
    assert stack.get_peek_status() == 1

    assert stack.size() == 4
    stack.pop()
    assert stack.peek() == 3
    assert stack.get_peek_status() == 1

    assert stack.size() == 3
    stack.pop()
    assert stack.peek() == 2
    assert stack.get_peek_status() == 1

    assert stack.size() == 2
    stack.pop()
    assert stack.peek() == 1
    assert stack.get_peek_status() == 1

    assert stack.size() == 1
    stack.pop()
    assert stack.peek() == 0
    assert stack.get_peek_status() == 2
