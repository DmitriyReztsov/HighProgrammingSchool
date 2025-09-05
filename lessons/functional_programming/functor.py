from pymonad.list import ListMonad
from pymonad.tools import curry
from pymonad.maybe import Maybe, Just, Nothing


@curry(2)
def add(x, y):
    return x + y


add10 = add(10)
Just(12).map(add10)
ListMonad(1, 2, 3, 4).map(add10)


def add10_to_monad(monad):
    return monad.map(add10)


print(add10_to_monad(Just(10)).value)  # 20
print(add10_to_monad(ListMonad(1, 2, 3, 4)).value)  # [11, 12, 13, 14]
