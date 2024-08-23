from abc import ABC, abstractmethod
from typing import TypeVar

Node = TypeVar("Node")


# 2.1
class LinkedListABC(ABC):
    CURSOR_POS = 0  # начальное положение курсора

    HEAD_NIL: int = 0
    HEAD_OK: int = 1
    HEAD_ERR: int = 2

    TAIL_NIL: int = 0
    TAIL_OK: int = 1
    TAIL_ERR: int = 2

    RIGHT_NIL: int = 0
    RIGHT_OK: int = 1
    RIGHT_ERR: int = 2

    PUT_RIGHT_NIL: int = 0
    PUT_RIGHT_OK: int = 1
    PUT_RIGHT_ERR: int = 2

    PUT_LEFT_NIL: int = 0
    PUT_LEFT_OK: int = 1
    PUT_LEFT_ERR: int = 2

    REMOVE_NIL: int = 0
    REMOVE_OK: int = 1
    REMOVE_ERR: int = 2

    ADD_EMPTY_NIL: int = 0
    ADD_EMPTY_OK: int = 1
    ADD_EMPTY_ERR: int = 2

    ADD_TAIL_NIL: int = 0
    ADD_TAIL_OK: int = 1
    ADD_TAIL_ERR: int = 2

    REPLACE_NIL: int = 0
    REPLACE_OK: int = 1
    REPLACE_ERR: int = 2

    FIND_NIL: int = 0
    FIND_OK: int = 1
    FIND_ERR: int = 2

    GET_NIL: int = 0
    GET_OK: int = 1
    GET_ERR: int = 2

    # команды
    @abstractmethod
    def head() -> None:
        """
        предусловия: список не пустой
        постусловия: изменено значение курсора

        """
        pass

    @abstractmethod
    def tail() -> None:
        """
        предусловия: список не пустой
        постусловия: изменено значение курсора

        """
        pass

    @abstractmethod
    def right() -> None:
        """
        предусловия: список не пустой, справа должен быть узел (курсор стоит не на последнем узле)
        постусловия: изменено значение курсора

        """
        pass

    @abstractmethod
    def put_right(node: Node) -> None:
        """
        предусловие: список не пустой, значение курсора отличное от 0
        постусловие: в список добавлен узел

        """
        pass

    @abstractmethod
    def put_left(node: Node) -> None:
        """
        предусловие: список не пустой, значение курсора отличное от 0
        постусловие: в список добавлен узел, необходим пересчет позиции курсора,
        чтобы он продолжал указывать на текущий узел

        """
        pass

    @abstractmethod
    def remove() -> None:
        """
        предусловие: список не пустой, значение курсора отличное от 0
        постусловие: из списка удален узел, необходим пересчет позиции курсора
        курсор смещается к правому соседу, если он есть, иначе курсор смещается к левому соседу, если он есть, либо 0

        """
        pass

    @abstractmethod
    def clear() -> None:
        """
        предусловие: нет
        постусловие: пустой список, курсор возвращен на дефолтное значение (0)

        """
        pass

    @abstractmethod
    def add_to_empty(node: Node) -> None:
        """
        предусловие: список пустой, курсор = 0
        постусловие: в список добавлен узел, значение курсора = 1

        """
        pass

    @abstractmethod
    def add_tail(node: Node) -> None:
        """
        предусловие: список не пустой
        постусловие: в список добавлен узел, значение курсора изменилось

        """
        pass

    @abstractmethod
    def replace(node: Node) -> None:
        """
        предусловие: список не пустой, курсор отличен от 0
        постусловие: в списке изменилось значение текущего узла, значение курсора не изменилось

        """
        pass

    @abstractmethod
    def find(node: Node) -> None:
        """
        предусловие: список не пустой, курсор отличен от 0
        постусловие: значение курсора изменилось, указывает на узел с искомым значением, первый справа от текущего

        """
        pass

    @abstractmethod
    def remove_all(node: Node) -> None:
        """
        предусловие: нет
        постусловие: из списка удалены заданные узлы, значение курсора должно быть пересчитано

        """
        pass

    # запросы
    @abstractmethod
    def get() -> Node:
        """
        предусловия: значение курсора должно отличаться от 0, т.е. курсор стоит на узле

        """
        pass

    @abstractmethod
    def size() -> int:
        pass

    @abstractmethod
    def is_head() -> bool:
        pass

    @abstractmethod
    def is_tail() -> bool:
        pass

    @abstractmethod
    def is_value() -> bool:
        pass

    @abstractmethod
    def get_get_status() -> bool:
        pass

    @abstractmethod
    def get_head_status() -> bool:
        pass

    @abstractmethod
    def get_tail_status() -> bool:
        pass

    @abstractmethod
    def get_right_status() -> bool:
        pass

    @abstractmethod
    def get_put_right_status() -> bool:
        pass

    @abstractmethod
    def get_put_left_status() -> bool:
        pass

    @abstractmethod
    def get_remove_status() -> bool:
        pass

    @abstractmethod
    def get_add_empty_status() -> bool:
        pass

    @abstractmethod
    def get_add_tail_status() -> bool:
        pass

    @abstractmethod
    def get_replace_status() -> bool:
        pass

    @abstractmethod
    def get_find_status() -> bool:
        pass


# 2.2. Как говорится в теории - внутри класса активно используются различные контейнеры, например, списки.
# Их методы эффективно реализованы в стандартных библиотеках, взять последний индекс в списке будет эффективнее
# стандартным методом списка.

# 2.3. Операция поиска всех узлов с заданным значением сведется к набору из одних и тех же значений.
# В отличие от предыущего LinkedList, где Node- был отдельный объект, тут узел рассматривается как просто значение в списке.
