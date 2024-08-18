from abc import ABC, abstractmethod
from typing import Any


class BoundedStackABC(ABC):
    POP_NIL: int = 0
    POP_OK: int = 1
    POP_ERR: int = 2
    PEEK_NIL: int = 0
    PEEK_OK: int = 1
    PEEK_ERR: int = 2
    PUSH_NIL: int = 0
    PUSH_OK: int = 1
    PUSH_ERR: int = 2
    BOUND_VALUE: int = 32

    @abstractmethod
    def BoundedStack(bound_value: int | None = None) -> Any:
        """
        предусловия: устанавливается значение лимита стека по умолчанию
        постусловия: меняется значение лимита стека, если он задан

        """
        pass

    @abstractmethod
    def push(value: Any) -> None:
        """
        предусловия: размер стека должен быть строго меньше лимита, в стеке есть место хотя бы для одного элемента
        постусловия: в стек добавлен новый элемент

        """
        pass

    @abstractmethod
    def pop() -> None:
        """
        предусловия: стек не пустой
        постусловия: из стека удален верхний элемент

        """
        pass

    @abstractmethod
    def clear() -> None:
        """
        предусловия: нет
        постусловия: стек очищен, атрибуты класса приведены к дефолтным значениям

        """
        pass

    @abstractmethod
    def peek() -> Any:
        """
        предусловия: стек не пустой
        постусловия: нет

        """
        pass

    @abstractmethod
    def size() -> int:
        """
        предусловия: нет
        постусловия: нет

        """
        pass

    @abstractmethod
    def stack_limit() -> int:
        """
        предусловия: нет
        постусловия: нет

        """
        pass

    @abstractmethod
    def get_pop_status() -> int:
        """
        предусловия: нет
        постусловия: нет

        """
        pass

    @abstractmethod
    def get_peek_status() -> int:
        """
        предусловия: нет
        постусловия: нет

        """
        pass

    @abstractmethod
    def get_push_status() -> int:
        """
        предусловия: нет
        постусловия: нет

        """
        pass


class BoundedStack(BoundedStackABC):
    def BoundedStack(self, bound_value: int = None) -> Any:
        self.clear()
        if bound_value is not None:
            self._bound_value = bound_value
        return self

    def clear(self) -> None:
        self._stack: list = []
        self._peek_status: int = self.PEEK_NIL
        self._pop_status: int = self.POP_NIL
        self._push_status: int = self.PUSH_NIL
        self._bound_value: int = self.BOUND_VALUE

    def push(self, value: Any) -> None:
        if self.size() < self.stack_limit():
            self._stack.append(value)
            self._push_status = self.PUSH_OK
        else:
            self._push_status = self.PUSH_ERR

    def pop(self) -> None:
        if self.size() > 0:
            self._stack.pop()
            self._pop_status = self.POP_OK
        else:
            self._pop_status = self.POP_ERR

    def peek(self) -> Any:
        if self.size() > 0:
            result = self._stack[-1]
            self._peek_status = self.PEEK_OK
        else:
            result = 0
            self._peek_status = self.PEEK_ERR
        return result

    def size(self) -> int:
        return len(self._stack)

    def stack_limit(self):
        return self._bound_value

    def get_pop_status(self) -> int:
        return self._pop_status

    def get_peek_status(self) -> int:
        return self._peek_status

    def get_push_status(self) -> int:
        return self._push_status
