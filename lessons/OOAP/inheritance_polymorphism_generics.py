from typing import Any
from typing_extensions import Self


class TypeT:
    ADD_NILL = 0
    ADD_OK = 1
    ADD_ERR = 2

    def __init__(self, value: Any) -> None:
        self._value = value
        self._add_status = self.ADD_NILL

    def __add(self, new: Self) -> None:
        match (self._value, new._value):
            case x, y if type(x) is type(y):
                self._add_status = self.ADD_OK
                self._value += y

            case _:
                self._add_status = self.ADD_ERR

    def __add__(self, new: Self) -> Self | None:
        """Перегрузка оператора сложения"""
        result_t = TypeT(self._value)
        result_t.__add(new)
        if result_t._add_status == self.ADD_OK:
            return result_t
        return None

    @property
    def value(self):
        return self._value


class Vecrtor:
    ADD_NILL = 0
    ADD_OK = 1
    ADD_ERR = 2

    def __init__(self, values_list: list[TypeT]) -> None:
        self._vector = values_list
        self._add_status = self.ADD_NILL

    def __add__(self, new: Self) -> Self | None:
        """Перегрузка оператора сложения"""
        if len(self._vector) != len(new._vector):
            self._add_status = self.ADD_ERR
            return None

        new_vector = []
        for elem_1, elem_2 in zip(self._vector, new._vector):
            if type(elem_1) is not type(elem_2):
                self._add_status = self.ADD_ERR
                return None
            new_elem = elem_1 + elem_2
            new_vector.append(new_elem)

        self._add_status = self.ADD_OK
        return Vecrtor(new_vector)

    def get_add_status(self):
        return self._add_status

    @property
    def value(self):
        return self._vector


t1 = TypeT(1)
t2 = TypeT(2)
t3 = TypeT(3)
t4 = TypeT(4)

vector_1 = Vecrtor([t1, t2, t3, t4])
vector_2 = Vecrtor([t1, t2, t3, t4])

sum_vector = vector_1 + vector_2
for t in sum_vector.value:
    print(t.value)
# 2
# 4
# 6
# 8

vector_1_1 = Vecrtor([vector_1, vector_2])
vector_1_2 = Vecrtor([vector_2, vector_1])

sum_vector2 = vector_1_1 + vector_1_2
print(sum_vector2.value)
for v0 in sum_vector2.value:
    for t in v0.value:
        print(t.value)
# [<__main__.Vecrtor object at 0x7b64486c2080>, <__main__.Vecrtor object at 0x7b64486c2650>]
# 2
# 4
# 6
# 8
# 2
# 4
# 6
# 8

vector_1_1_1 = Vecrtor([vector_1_1, vector_1_2])
vector_1_1_2 = Vecrtor([vector_1_2, vector_1_1])

sum_vector3 = vector_1_1_1 + vector_1_1_2
print(sum_vector3.value)
for v0 in sum_vector3.value:
    for v1 in v0.value:
        for t in v1.value:
            print(t.value)
# [<__main__.Vecrtor object at 0x7b64485ac100>, <__main__.Vecrtor object at 0x7b64485ac5e0>]
# 2
# 4
# 6
# 8
# 2
# 4
# 6
# 8
# 2
# 4
# 6
# 8
# 2
# 4
# 6
# 8
