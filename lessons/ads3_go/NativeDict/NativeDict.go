// 9
package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
)

// 9.1 В Go словарь реализован как структура бакетов по 8 пар ключ-значение. Сначала хэш-функция вычисляет
// в какой бакет идти за значением, далее ищет начиная с этого стартового бакета.

type INativeDictionary interface {
	HashFun(value string) int
	IsKey(key string) bool
	Get(key string) (any, error)
	Put(key string, value any)
}

type NativeDictionary[T any] struct {
	size     int
	slots    []string
	occupied []bool
	values   []T
	step     int
}

// создание экземпляра словаря
func Init[T any](sz int) NativeDictionary[T] {
	nd := NativeDictionary[T]{size: sz, slots: nil, values: nil, step: 1}
	nd.slots = make([]string, sz)
	nd.occupied = make([]bool, sz)
	nd.values = make([]T, sz)
	return nd
}

func (nd *NativeDictionary[T]) HashFun(value string) int {
	// всегда возвращает корректный индекс слота
	// сумма байтов по модулю размера таблицы - из предыдущего занятия
	sum := 0
	for _, b := range []byte(value) {
		sum += int(b)
	}
	return sum % nd.size
}

func (nd *NativeDictionary[T]) seekSlot(key string) int {
	// находит индекс пустого слота для значения,
	// или -1 если свободного слота не найти
	hash := nd.HashFun(key)

	for i := 0; i < nd.size; i++ {
		index := (hash + i*nd.step) % nd.size
		if !nd.occupied[index] {
			return index
		}
	}
	return -1
}

func (nd *NativeDictionary[T]) find(key string) int {
	// находит индекс слота со значением, или -1
	hash := nd.HashFun(key)
	for i := 0; i < nd.size; i++ {
		index := (hash + i*nd.step) % nd.size
		if nd.occupied[index] && nd.slots[index] == key {
			return index
		}

		if !nd.occupied[index] {
			return -1
		}
	}
	return -1
}

func (nd *NativeDictionary[T]) IsKey(key string) bool {
	// возвращает true если ключ имеется
	slot := nd.find(key)
	return slot != -1
}

func (nd *NativeDictionary[T]) Get(key string) (T, error) {
	// возвращает value для key,
	// или error если ключ не найден

	var result T

	slot := nd.find(key)
	if slot == -1 {
		return result, errors.New("Key error!")
	}
	return nd.values[slot], nil
}

func (nd *NativeDictionary[T]) Put(key string, value T) {
	// гарантированно записываем
	// значение value по ключу key
	
	// First check if key already exists
	existingSlot := nd.find(key)
	if existingSlot != -1 {
		// Update existing key's value
		nd.values[existingSlot] = value
		return
	}
	
	// Key doesn't exist, find new slot
	slot := nd.seekSlot(key)

	if slot == -1 {
		return
	}
	nd.slots[slot] = key
	nd.occupied[slot] = true
	nd.values[slot] = value
}
