from pymonad.list import ListMonad
from pymonad.tools import curry
from pymonad.maybe import Maybe, Just, Nothing
from pymonad.reader import Compose


"""
Задание.
В статье есть вторая задача про канатоходца, тоже по сути в декларативном стиле. Перепишите её на
работу с PyMonad.
Обратите внимание, что, во-первых, поле .result (извлечение данных из функтора) в оригинальном примере
надо заменить на метод getValue() (в последней версии PyMonad он вроде был заменён на прямой доступ к
полю value, как раньше был result), и во-вторых, в функции вывода результата show() случай, когда
канатоходец упал, выявляется простой проверкой параметра maybe на равенство Nothing. Если канатоходец
держится нормально, то результат будет представлен в виде функтора Just(), который обёртывает список из
двух элементов (сколько птиц слева и сколько птиц справа). """


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
