// 3.6. Вообще из того, что посмотрел по ключевым словам "банковский метод", я сделал вывод, что банковский метод -
// это не столько метод реализации, сколлько метод анализа алгоритма. Абстракция, объясняющая, почему амортизировано
// мы имеем О(1) в среднем на вставку (при чем, не любую, а в конец). В этой реализации я оставлю только метод
// добавления элемента в конец и метод увеличения массива.

package main

import (
	"os"
	"fmt"
	"math"
)

type DynArrayBank[T any] struct {
	count    int
	capacity int
	array    []T
	bank     int // "банк" для складывания токенов при добавлении элемента, который будем использовать для увеличения массива
}

func (da *DynArrayBank[T]) Init() {
	da.count = 0
	da.MakeArray(2)
	da.bank = 0
}

func (da *DynArrayBank[T]) MakeArray(sz int) {
	var arr = make([]T, sz)

	if da.count != 0 {
		copy(arr, da.array)
	}
	da.capacity = sz
	da.array = arr
}

func (da *DynArrayBank[T]) calculateCapacity(direction string) int {
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

func (da *DynArrayBank[T]) append(itm T, index int) {
	da.array[da.count] = itm
	da.count++
}

func (da *DynArrayBank[T]) resizeIfNeeded() {
	cost := da.count                              // стоимость нового массива - количество операций копирования элементов
	price := int(math.Log2(float64(da.capacity))) // цена как степень двойки
	bank2 := int(math.Log2(float64(da.bank)))     // размер банка как степень двойки

	if bank2 > price { // можем оплатить
		da.calculateCapacity("up")
		da.MakeArray(int(math.Pow(2, float64(bank2))))
		da.bank = da.bank - cost // недостающие токены возьмутся из банка
	}
}

func (da *DynArrayBank[T]) Append(itm T) {
	cost := 1                          // стоимость операции (сложность, количество действий)
	price := 3                         // сколько мы возьмем за ее исполнение
	da.bank = da.bank + (price - cost) // в банк идет 2**1 токенов
	da.resizeIfNeeded()
	da.append(itm, da.count)
}

func (da *DynArrayBank[T]) GetItem(index int) (T, error) {
	var zero T
	if index >= da.count {
		return zero, fmt.Errorf("Index out of range")
	}
	if index < 0 {
		return zero, fmt.Errorf("Syntax sugar is not implemented")
	}
	return da.array[index], nil
}
