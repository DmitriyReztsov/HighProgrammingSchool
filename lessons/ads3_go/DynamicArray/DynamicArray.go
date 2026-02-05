// 3

package main

import (
	"os"
	"fmt"
)

type DynArray[T any] struct {
	count    int
	capacity int
	array    []T
}

func (da *DynArray[T]) Init() {
	da.count = 0
	da.MakeArray(16)
}

func (da *DynArray[T]) MakeArray(sz int) {
	var arr = make([]T, sz)
	//  копируем содержимое array в arr ...
	if da.count != 0 {
		copy(arr, da.array)
	}
	da.capacity = sz
	da.array = arr
}

func (da *DynArray[T]) calculateCapacity(direction string) int {
	var newCapacity int

	if direction == "up" {
		return da.capacity * 2
	}
	if direction == "down" {
		newCapacity = int(float32(da.capacity) / 1.5)
		if newCapacity < 16 {
			newCapacity = 16
		}
	}
	return newCapacity
}

func (da *DynArray[T]) insertOrAppend(itm T, index int) {
	if da.count != index {
		itm = da.insert(itm, index)
	}
	da.array[da.count] = itm
	da.count++
}

func (da *DynArray[T]) insert(itm T, index int) T {
	var buff T

	for ind := range da.count {
		if ind < index {
			continue
		}
		buff = da.array[ind]
		da.array[ind] = itm
		itm = buff
	}

	return itm
}

func (da *DynArray[T]) remove(index int) {
	var zero T
	newIndex := 0
	for ind := range da.count {
		if ind < index {
			continue
		}
		if ind == index {
			newIndex = ind
			da.array[newIndex] = zero
			continue
		}
		da.array[newIndex] = da.array[ind]
		newIndex++
	}

	da.count--
}

func (da *DynArray[T]) resizeIfNeeded() {
	var sz int
	lastIndex := da.count
	if lastIndex >= da.capacity {
		sz = da.calculateCapacity("up")
		da.MakeArray(sz)
	} else if lastIndex < int(float32(da.capacity)/2) {
		sz = da.calculateCapacity("down")
		da.MakeArray(sz)
	}
}

// 3.2 Вставка по индексу
// сложность по времени O(n), по памяти O(1)
func (da *DynArray[T]) Insert(itm T, index int) error {
	// максимальный индекс, в который допустима вставка - сразу за последним элементом,
	// т.е. по значению равен текущему количеству элементов
	if index > da.count || index < 0 {
		return fmt.Errorf("bad index '%d'", index)
	}
	da.resizeIfNeeded()
	da.insertOrAppend(itm, index)
	return nil
}

// 3.3 Удаление по индексу
// сложность по времени O(n), по памяти O(1)
// можно было бы оптимизировать удаление последнего элемента О(1)
func (da *DynArray[T]) Remove(index int) error {
	if index >= da.count || index < 0 {
		return fmt.Errorf("bad index '%d'", index)
	}
	da.remove(index)
	da.resizeIfNeeded()
	return nil
}

// 3.1. Добавление в конец
// по времени и памяти O(1) если не надо увеличивать размер массива, иначе O(n)
func (da *DynArray[T]) Append(itm T) {
	da.resizeIfNeeded()
	da.insertOrAppend(itm, da.count)
}

// 3.1 Получение элемента по индексу
// сложность по времени O(1), по памяти O(1)
func (da *DynArray[T]) GetItem(index int) (T, error) {
	var zero T
	if index >= da.count {
		return zero, fmt.Errorf("Index out of range")
	}
	if index < 0 {
		return zero, fmt.Errorf("Syntax sugar is not implemented")
	}
	return da.array[index], nil
}
