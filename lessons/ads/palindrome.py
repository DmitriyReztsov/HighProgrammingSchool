from lessons.ads.deque import Deque


def is_palindrome(phrase: str) -> bool:
    phrase_deque = Deque()
    for char in phrase:
        phrase_deque.addTail(char)

    while phrase_deque.size() > 1:
        if phrase_deque.removeFront() != phrase_deque.removeTail():
            return False

    return True
