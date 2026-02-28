// 6

package main

import "errors"

// 6.4 функция, проверяющая, яявляется ли строка палиндромом
func IsPalindrome(stringLine string) bool {
	var d Deque[rune]

	for _, ch := range stringLine {
		d.AddFront(ch)
	}

	for true {
		head, err := d.RemoveFront()
		if err != nil {
			break
		}
		tail, err := d.RemoveTail()
		if err != nil {
			break
		}
		if head != tail {
			return false
		}
	}
	return true
}

// 6.5 метод, который возвращает минимальный элемент деки за O(1). Такой метод требует деку с дополнительной декой, на
// которой будем делать синхронные операции, сохраняя миннимум в голове и хвосте (в зависимости от типа операции).
// Минимум будет находиться как минимум между головой и хвостом. Поскольку итераций по деке не будет, значения головы и
// хвоста получим за О(1), то и вся операция получения минимума будет стоить О(1) по времени и О(n) по памяти.

type DequeWithMin[T int] struct {
	Deque[T]
	dequeueMin *Deque[T]
}

func NewDequeWithMin[T int]() *DequeWithMin[T] {
	return &DequeWithMin[T]{
		Deque:      Deque[T]{},
		dequeueMin: &Deque[T]{},
	}
}

func (d *DequeWithMin[T]) AddFront(itm T) {
	d.Deque.AddFront(itm)

	if d.dequeueMin.head != nil {
		if d.dequeueMin.head.value < itm {
			itm = d.dequeueMin.head.value
		}
	}
	d.dequeueMin.AddFront(itm)
}

func (d *DequeWithMin[T]) AddTail(itm T) {
	d.Deque.AddTail(itm)

	if d.dequeueMin.tail != nil {
		if d.dequeueMin.tail.value < itm {
			itm = d.dequeueMin.tail.value
		}
	}
	d.dequeueMin.AddTail(itm)
}

func (d *DequeWithMin[T]) RemoveFront() (T, error) {
	result, err := d.Deque.RemoveFront()
	d.dequeueMin.RemoveFront()
	return result, err
}

func (d *DequeWithMin[T]) RemoveTail() (T, error) {
	result, err := d.Deque.RemoveTail()
	d.dequeueMin.RemoveTail()
	return result, err
}

// тогда метод, возвращающий минимальный элемент будет таким
func (d *DequeWithMin[T]) GetMin() (T, error) {
	if d.Deque.Size() == 0 {
		return d.zero, errors.New("Empty dequeue")
	}

	if d.dequeueMin.head.value > d.dequeueMin.tail.value {
		return d.dequeueMin.tail.value, nil
	}
	return d.dequeueMin.head.value, nil
}

// 6.6 двусторонняя очередь с помощью динамического массива. Методы добавления и удаления элементов с обоих концов деки
//  должны работать за амортизированное время o(1). Идея в организации цикличной очереди. При заполнении массива - ресайз
//  и копирование. В таком случае мы всегда держим индекс головы и хваста - получение по индексу O(1). Копирование 
// происходит относительно редко, что дает амортизированное время выполнения.

type DequeD[T any] struct {
	deque    []T
	head     int
	tail     int
	size     int
	capacity int
	zero     T
}

func NewDequeD[T any](capacity int) *DequeD[T] {
	return &DequeD[T]{
		deque:    make([]T, capacity),
		head:     0,
		tail:     0,
		size:     0,
		capacity: capacity,
	}
}

func (d *DequeD[T]) Size() int {
	return d.size
}

func (d *DequeD[T]) AddFront(itm T) {
	if d.size == d.capacity {
		d.resizeUp()
	}

	d.head = (d.head - 1 + d.capacity) % d.capacity
	d.deque[d.head] = itm
	d.size++
}

func (d *DequeD[T]) AddTail(itm T) {
	if d.size == d.capacity {
		d.resizeUp()
	}

	d.deque[d.tail] = itm
	d.tail = (d.tail + 1) % d.capacity
	d.size++
}

func (d *DequeD[T]) resizeUp() {
	newCap := d.capacity * 2
	newDeque := make([]T, newCap)

	for i := 0; i < d.size; i++ {
		newDeque[i] = d.deque[(d.head+i)%d.capacity]
	}

	d.deque = newDeque
	d.head = 0
	d.tail = d.size
	d.capacity = newCap
}

func (d *DequeD[T]) resizeDown() {
	newCap := int(float32(d.capacity) / 1.5)
	if newCap < 16 {
		newCap = 16
	}

	newDeque := make([]T, newCap)

	for i := 0; i < d.size; i++ {
		newDeque[i] = d.deque[(d.head+i)%d.capacity]
	}

	d.deque = newDeque
	d.head = 0
	d.tail = d.size
	d.capacity = newCap
}

func (d *DequeD[T]) RemoveFront() (T, error) {
	var result T

	if d.size == 0 {
		return d.zero, errors.New("Empty deque")
	}

	result = d.deque[d.head]
	d.head = (d.head + 1) % d.capacity
	d.size--

	if d.capacity > 16 && d.size < d.capacity/2 {
		d.resizeDown()
	}
	return result, nil
}

func (d *DequeD[T]) RemoveTail() (T, error) {
	var result T

	if d.size == 0 {
		return d.zero, errors.New("Empty deque")
	}

	elemIndex := (d.tail - 1 + d.capacity) % d.capacity
	result = d.deque[elemIndex]
	d.tail = elemIndex
	d.size--

	if d.capacity > 16 && d.size < d.capacity/2 {
		d.resizeDown()
	}
	return result, nil
}
