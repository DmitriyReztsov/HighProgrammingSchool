//11

package main

import (
	"os"
)

// битовый массив длиной f_len = 32. Для учебной задачи по условию хардкодим тип bitArray как 32-х разрядный int
// сигнатура скрывает в себе серьезную уязвимость: f_len должна быть не больше 32, иначе при таком коде мы можем
// попасть на маску, которая всегда будет -1 из-за того, что int - знаковый тип, зависящий от платформы:
type BloomFilter struct {
	filter_len int
}

func Init(f_len uint) BloomFilter {
	return BloomFilter{
		filter_len: (1 << f_len) - 1,
	}
}

// хэш-функции
// для избегания переполнения типа используем явно и приводит int к uint32 \
// + сразу берем на каждом шаге модуль sum
func hashHelper(value string, salt, filterLen int) int {
	var sum uint32 = 0

	for _, char := range value {
		sum = (sum*uint32(salt) + uint32(char)) % uint32(filterLen)
	}
	return 1 << sum
}

// 17
func (bf *BloomFilter) Hash1(s string) int {
	return hashHelper(s, 17, 32)
}

// 223
func (bf *BloomFilter) Hash2(s string) int {
	return hashHelper(s, 223, 32)
}

// добавляем строку s в фильтр
func (bf *BloomFilter) Add(s string) {
	bf.filter_len |= bf.Hash1(s)
	bf.filter_len |= bf.Hash2(s)
}

// проверка, имеется ли строка s в фильтре
func (bf *BloomFilter) IsValue(s string) bool {
	mask1 := bf.Hash1(s)
	mask2 := bf.Hash2(s)
	if mask1&bf.filter_len == mask1 && mask2&bf.filter_len == mask2 {
		return true
	}
	return false
}
