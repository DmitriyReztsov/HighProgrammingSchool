from abc import ABC, abstractmethod
from typing import Self, TypeVar

Node = TypeVar("Node")


class QueueABC(ABC):
    HEAD_POS: int = 0
    TAIL_POS: int = 0
    COUNT: int = 0  # начальное количество элементов в массиве

    DEQUEUE_NIL: int = 0
    DEQUEUE_OK: int = 1
    DEQUEUE_ERR: int = 2

    # конструктор
    @abstractmethod
    def Queue() -> Self:
        """
        предусловия: нет
        постусловия: создана новая очередь

        """
        pass

    # команды
    @abstractmethod
    def enqueue(node: Node) -> None:
        """
        предусловия: нет, если очередь не фиксированной емкости.
        постусловие: элемент добавлен в конец очереди. Тут нужен был бы статус,
        если бы у нас была закольцованная очередь фиксированной емкости

        """

    @abstractmethod
    def dequeue() -> Node:
        """
        предусловие: хвост не равен голове, т.е. очередь не пустая
        постусловие: элемент удален из головы очереди

        эта операция сводится к двум атомарным: _get_tail и _remove_tail, видимо. скрытых реализацией

        """
        pass

    @abstractmethod
    def _remove_head() -> None:
        """
        предусловие: хвост не равен голове, т.е. очередь не пуста
        постусловие: удален головной элемент

        """
        pass

    # запросы
    @abstractmethod
    def _get_head() -> Node:
        """
        предусловия: хвост не равен голове, т.е. очередь не пуста

        """
        pass

    @abstractmethod
    def size() -> int:
        pass

    @abstractmethod
    def get_dequeue_status() -> int:
        pass


class Queue(QueueABC):
    def Queue(self) -> Self:
        self._clear()
        return self

    def _clear(self):
        self._head = self.HEAD_POS
        self._tail = self.TAIL_POS

        self._queue = []
        self._count = self.COUNT

        self._dequeue_status = self.DEQUEUE_NIL

    def enqueue(self, node: Node) -> None:
        self._queue.append(node)
        self._count += 1
        self._tail += 1
        if self._head == self.HEAD_POS:
            self._head += 1

    def _remove_head(self) -> None:
        self._queue.pop(self._head - 1)
        self._tail -= 1
        self._count -= 1

    def _get_head(self) -> Node:
        return self._queue[self._head - 1]

    def dequeue(self) -> Node:
        if not (self._tail == self._head == 0):
            head_element = self._get_head()
            self._remove_head()
            self._dequeue_status = self.DEQUEUE_OK
            return head_element  # noqa R504

        self._dequeue_status = self.DEQUEUE_ERR
        return 0

    def size(self) -> int:
        return self._count

    def get_dequeue_status(self) -> int:
        return self._dequeue_status
