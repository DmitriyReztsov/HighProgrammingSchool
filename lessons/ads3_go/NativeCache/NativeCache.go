// 12
package main

import (
	"errors"
)

type NativeCache[T any] struct {
	size   int
	slots  []string
	values []T
	hits   []int
	step   int
}

// создание экземпляра словаря
func Init[T any](sz int) NativeCache[T] {
	nc := NativeCache[T]{size: sz, slots: nil, values: nil, hits: nil, step: 1}
	nc.slots = make([]string, sz)
	nc.values = make([]T, sz)
	nc.hits = make([]int, sz)
	return nc
}

func (nc *NativeCache[T]) HashFun(value string) int {
	// всегда возвращает корректный индекс слота
	// сумма байтов по модулю размера таблицы - из предыдущего занятия
	sum := 0
	for _, b := range []byte(value) {
		sum += int(b)
	}
	return sum % nc.size
}

func (nc *NativeCache[T]) seekMinHitSlot() int {
	minInd := 0
	min := nc.hits[minInd]

	for i, v := range nc.hits {
		if v < min {
			min = v
			minInd = i
		}
	}
	nc.hits[minInd] = 0
	return minInd
}

func (nc *NativeCache[T]) seekSlot(key string) int {
	// находит индекс пустого слота для значения,
	// или -1 если свободного слота не найти
	hash := nc.HashFun(key)

	for i := 0; i < nc.size; i++ {
		index := (hash + i*nc.step) % nc.size
		if nc.slots[index] == "" {
			return index
		}
	}

	// если не нашли ни одного пустого слота - надо освободить слот и вернуть его индекс
	return nc.seekMinHitSlot()
}

func (nc *NativeCache[T]) find(key string) int {
	// находит индекс слота со значением, или -1
	hash := nc.HashFun(key)
	for i := 0; i < nc.size; i++ {
		index := (hash + i*nc.step) % nc.size
		if nc.slots[index] == key {
			return index
		}
	}
	return -1
}

func (nc *NativeCache[T]) IsKey(key string) bool {
	// возвращает true если ключ имеется
	slot := nc.find(key)
	return slot != -1
}

func (nc *NativeCache[T]) Get(key string) (T, error) {
	// возвращает value для key,
	// или error если ключ не найден

	var result T

	slot := nc.find(key)
	if slot == -1 {
		return result, errors.New("Key error!")
	}
	nc.hits[slot]++
	return nc.values[slot], nil
}

func (nc *NativeCache[T]) Put(key string, value T) {
	// гарантированно записываем
	// значение value по ключу key

	existingSlot := nc.find(key)
	if existingSlot != -1 {
		// считаем, что мы заинтересованы в частоте обращения к ключу, а не к значению
		// поэтому счетчик не трогаем
		nc.values[existingSlot] = value
		return
	}

	slot := nc.seekSlot(key)

	if slot == -1 {
		return
	}
	nc.slots[slot] = key
	nc.values[slot] = value
}
