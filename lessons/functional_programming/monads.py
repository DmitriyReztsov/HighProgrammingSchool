from pymonad.list import ListMonad
from pymonad.tools import curry
from pymonad.maybe import Maybe, Just, Nothing
from pymonad.reader import Compose


# посадка птиц на левую сторону
@curry(2)
def to_left(num: int, cur_dispos: tuple) -> "Maybe":
    l, r = cur_dispos
    if abs((l + num) - r) > 4:
        return Nothing
    return Just((l + num, r))


# посадка птиц на правую сторону
@curry(2)
def to_right(num: int, cur_dispos: tuple) -> "Maybe":
    l, r = cur_dispos
    if abs((r + num) - l) > 4:
        return Nothing()
    return Just((l, r + num))


# банановая кожура
banana = lambda x: Nothing


# отображение результата
def show(maybe: Maybe) -> None:
    if maybe is Nothing:
        print("Fallen")
        return
    print("Stayed")


# начальное состояние
begin = Just((0, 0))

# show(begin() + ">>=" + to_left(2) + ">>=" + to_right(5) + ">>=" + to_left(-2))  # канатоходец упадёт тут
show(begin.bind(to_left(2)).bind(to_right(5)).bind(to_left(-2)))
# show(begin() + ">>=" + to_left(2) + ">>=" + to_right(5) + ">>=" + to_left(-1))  # в данном случае всё ок
show(begin.bind(to_left(2)).bind(to_right(5)).bind(to_left(-1)))
# show(begin() + ">>=" + to_left(2) + ">>=" + banana + ">>=" + to_right(5) + ">>=" + to_left(-1))  # кожура всё испортит
show(begin.bind(to_left(2)).bind(banana).bind(to_left(-2)))
