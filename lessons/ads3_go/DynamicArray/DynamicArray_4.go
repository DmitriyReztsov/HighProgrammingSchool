// 3.7 Многомерный динамический массив.

package main

import (
	"os"
	"fmt"
)

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
