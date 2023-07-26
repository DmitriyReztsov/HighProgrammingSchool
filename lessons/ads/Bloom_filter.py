class BloomFilter:
    def __init__(self, f_len: int) -> None:
        self.filter_len = f_len
        # создаём битовый массив длиной f_len = 32
        # количество значений для фильтра n=10
        self.bit_array = int("0", 2)

    def hash1(self, str1: str) -> int:
        # 17
        code = 0
        for c in str1:
            code = code * 17 + ord(c)
        bit_position = code % self.filter_len
        bit_mask = "0" * bit_position + "1" + "0" * (self.filter_len - bit_position - 1)
        return int(bit_mask, 2)

    def hash2(self, str1: str) -> int:
        # 223
        code = 0
        for c in str1:
            code = code * 223 + ord(c)
        bit_position = code % self.filter_len
        bit_mask = "0" * bit_position + "1" + "0" * (self.filter_len - bit_position - 1)
        return int(bit_mask, 2)

    def add(self, str1: str) -> None:
        # добавляем строку str1 в фильтр
        self.bit_array = self.hash1(str1) | self.bit_array
        self.bit_array = self.hash2(str1) | self.bit_array

    def is_value(self, str1: str) -> bool:
        # проверка, имеется ли строка str1 в фильтре
        mask_1 = self.hash1(str1)
        mask_2 = self.hash2(str1)
        if mask_1 & self.bit_array == mask_1 and mask_2 & self.bit_array == mask_2:
            return True
        return False
