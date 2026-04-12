//11

package main

import (
	// "os"
)

// битовый массив длиной f_len = 32. Для учебной задачи по условию хардкодим тип bitArray как 32-х разрядный int
type BloomFilter struct {
	filterLen int
	bitArray  uint32
}

// хэш-функции
// для избегания переполнения типа используем явно и приводит int к uint32 \
// + сразу берем на каждом шаге модуль sum
func hashHelper(value string, salt, filterLen int) uint32 {
	var sum uint32 = 0

	for _, char := range value {
		sum = (sum*uint32(salt) + uint32(char)) % uint32(filterLen)
	}
	return 1 << sum
}

// 17
func (bf *BloomFilter) Hash1(s string) uint32 {
	return hashHelper(s, 17, bf.filterLen)
}

// 223
func (bf *BloomFilter) Hash2(s string) uint32 {
	return hashHelper(s, 223, bf.filterLen)
}

// добавляем строку s в фильтр
func (bf *BloomFilter) Add(s string) {
	bf.bitArray |= bf.Hash1(s)
	bf.bitArray |= bf.Hash2(s)
}

// проверка, имеется ли строка s в фильтре
func (bf *BloomFilter) IsValue(s string) bool {
	mask1 := bf.Hash1(s)
	mask2 := bf.Hash2(s)
	if mask1&bf.bitArray == mask1 && mask2&bf.bitArray == mask2 {
		return true
	}
	return false
}
