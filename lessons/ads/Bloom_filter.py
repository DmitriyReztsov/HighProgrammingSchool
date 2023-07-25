from array import array


class BloomFilter:
    def __init__(self, f_len: int) -> None:
        self.filter_len = f_len
        # создаём битовый массив длиной f_len = 32
        # количество значений для фильтра n=10
        self.bit_array = array('I')
        self.bit_array.extend((0,) * self.filter_len)

    def hash1(self, str1: str) -> int:
        # 17
        hash = 17
        for c in str1:
            # code = ord(c)
            hash = ((hash << 5) + hash) + ord(c)
        return hash % self.filter_len

    def hash2(self, str1: str) -> int:
        # 223 
        hash = 223
        for c in str1:
            # code = ord(c)
            hash = ((hash << 5) + hash) + ord(c)
        return hash % self.filter_len

    def add(self, str1: str) -> None:
        # добавляем строку str1 в фильтр
        self.bit_array[self.hash1(str1)] = 1
        self.bit_array[self.hash2(str1)] = 1

    def is_value(self, str1: str) -> bool:
        # проверка, имеется ли строка str1 в фильтре
        if self.bit_array[self.hash1(str1)] == 1 and self.bit_array[self.hash2(str1)] == 1:
            return True
        return False
