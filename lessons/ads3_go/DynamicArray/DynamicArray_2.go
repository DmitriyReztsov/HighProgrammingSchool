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


// 3.7 Многомерный динамический массив.

// Надо добавить метод для обычного массива, который принимал бы размерность
func (da *DynArray[T]) InitParam(sz int) {
	da.count = 0
	da.MakeArray(sz)
}

// Определение структуры много мерного массива
type NDimensionDynArray[T any] struct {
	dimensionNum int
	array        *DynArray[any]
}

func (da *NDimensionDynArray[T]) Init(capacities []int) {
	da.dimensionNum = len(capacities)

	da.array = makeNDimArray(capacities)
}

// функция-фабрика для массива с заданными параметрами
func makeNDimArray(capacities []int) *DynArray[any] {
	cap := capacities[0]
	a := &DynArray[any]{}
	a.InitParam(cap)

	if len(capacities) != 1 {
		for i := 0; i < cap; i++ {
			a.Append(makeNDimArray(capacities[1:]))
		}
	}
	return a
}

// Получение элемента по индексу в многомерном массиве
func (da *NDimensionDynArray[T]) GetItem(indexes ...int) (any, error) {
	var zero any

	if len(indexes) > da.dimensionNum+1 {
		return zero, fmt.Errorf("Too many indexes - out of dimensions")
	}
	return getItemInArrays(da.array, indexes...)
}

func getItemInArrays(arr *DynArray[any], indexes ...int) (any, error) {
	var zero any

	if len(indexes) == 0 {
		return zero, fmt.Errorf("What are you waiting for?")
	}

	idx := indexes[0]
	if idx < 0 || idx >= arr.count {
		return zero, fmt.Errorf("index out of range")
	}

	val, err := arr.GetItem(idx)

	if len(indexes) == 1 {
		return val, err
	}

	nextArray, ok := val.(*DynArray[any]) // приводим тип any к DynArray и проверяем, что это он
	if !ok {
		return zero, fmt.Errorf("Expected nested array")
	}

	return getItemInArrays(nextArray, indexes[1:]...)
}

func (da *NDimensionDynArray[T]) Append(itm T, indexes ...int) {
	arr, err := getItemInArrays(da.array, indexes...)

	if err != nil {
		return
	}

	array, ok := arr.(*DynArray[any])
	if !ok {
		return
	}

	array.Append(itm)
}

// Рефлексия по заданию 1.8.
// Я так же начал с проверки длин списков, добавив еще проверку на пустой список. Поскольку в задаче не было напрямую
// указано, что делать в случае неравенства, то я в обоих случаях возвращаю просто пустой список. Я тоже решил, что
// бросать исключение или ошибку было бы не правильно, мы не декларируем возврат ошибки.
// Далее я соединяю списки на низком уровне, хотя стоило бы воспользоваться уже реализованой функцией Append. Ну и до
// кучи, можно было бы пробегаться не в
// ```for true```,
// а в нормально организованном цикле
// ```for node := l.head; node != nil; node = node.next```.
