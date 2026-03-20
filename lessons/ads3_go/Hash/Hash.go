//8

package main

import (
	"strconv"
	"os"
)

// IHashTable по рекомендации ИИ ревьюера
type IHashTable interface {
	HashFun(value string) int
	SeekSlot(value string) int
	Put(value string) int
	Find(value string) int
}

type HashTable struct {
	size     int
	step     int
	slots    []string
	occupied []bool
}

func Init(sz int, stp int) HashTable {
	ht := HashTable{size: sz, step: stp, slots: nil, occupied: nil}
	ht.slots = make([]string, sz)
	ht.occupied = make([]bool, sz)
	return ht
}

// 8.3 Реализация.
func (ht *HashTable) HashFun(value string) int {
	// сумма байтов по модулю размера таблицы
	sum := 0
	for _, b := range []byte(value) {
		sum += int(b)
	}
	return sum % ht.size
}

func (ht *HashTable) probeFind(startHash int, condition func(index int) bool) int {
	for i := 0; i < ht.size; i++ {
		index := (startHash + i*ht.step) % ht.size
		if condition(index) {
			return index
		}
	}
	return -1
}

func (ht *HashTable) SeekSlot(value string) int {
	// находит индекс пустого слота для значения,
	// или -1 если свободного слота не найти
	hash := ht.HashFun(value)

	for i := 0; i < ht.size; i++ {
		index := (hash + i*ht.step) % ht.size
		if !ht.occupied[index] {
			return index
		}
	}
	return -1
}

func (ht *HashTable) Put(value string) int {
	// записываем значение по хэш-функции

	// возвращается индекс слота или -1
	// если из-за коллизий элемент не удаётся разместить
	index := ht.SeekSlot(value)
	if index == -1 {
		return -1
	}
	ht.slots[index] = value
	ht.occupied[index] = true
	return index
}

func (ht *HashTable) Find(value string) int {
	// находит индекс слота со значением, или -1
	hash := ht.HashFun(value)
	for i := 0; i < ht.size; i++ {
		index := (hash + i*ht.step) % ht.size
		if ht.occupied[index] && ht.slots[index] == value {
			return index
		}

		if !ht.occupied[index] {
			return -1
		}
	}
	return -1
}
