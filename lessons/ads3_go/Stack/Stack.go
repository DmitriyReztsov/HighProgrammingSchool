// 4

package main

import (
	"os"
	"errors"
)

type Stack[T any] struct {
	stack []T
}

// 4.1 time & space complexity O(1)
func (st *Stack[T]) Size() int {
	return len(st.stack)
}

// 4.1 time & space complexity O(1)
func (st *Stack[T]) Peek() (T, error) {
	var zero T

	if st.Size() == 0 {
		return zero, errors.New("Stack is empty")
	}
	return st.stack[st.Size()-1], nil
}

// 4.1 time & space complexity O(1)
// единственная проблема -необходимость через zero освобождать ячейку памяти.
// Выглядит костыльно, решение - на основе связного списка (см. ниже, для реверснутого стека)
func (st *Stack[T]) Pop() (T, error) {
	var zero T

	result, err := st.Peek()

	if err == nil {
		st.stack[st.Size()-1] = zero
		st.stack = st.stack[:st.Size()-1]
	}

	return result, err
}

// 4.1 time & space complexity O(1)
func (st *Stack[T]) Push(itm T) {
	st.stack = append(st.stack, itm)
}

// 4.2. Чтобы стек работал с головой можно либо костылить мапу, либо, что удобнее - сделать свою структуру односвязного списка
// Тогда сложность по времени и памяти останется О(1) для операций, не пришлось бы реаллоцировать слайсы, что стоило бы О(n)
type Node[T any] struct {
	value T
	next  *Node[T]
}

type StackR[T any] struct {
	head *Node[T]
	tail *Node[T]
	size int
}

func (st *StackR[T]) Size() int {
	return st.size
}

func (st *StackR[T]) Peek() (T, error) {
	var zero T

	if st.Size() == 0 {
		return zero, errors.New("Stack is empty")
	}
	return st.head.value, nil
}

func (st *StackR[T]) Pop() (T, error) {
	result, err := st.Peek()

	if err == nil {
		st.size--
		exHead := st.head
		st.head = st.head.next
		exHead.next = nil
	}

	return result, err
}

func (st *StackR[T]) Push(itm T) {
	n := &Node[T]{value: itm}

	if st.size == 0 {
		st.head = n
		st.tail = n
	} else {
		st.tail.next = n
		st.tail = n
	}
	st.size++
}

// 4.3. Теоретически цикл может завешиться ошибкой, если в стеке нечетное количество элементов и попытка сделать pop()
// на пустом стеке вернет панику (для Go). Если же результат не прервет выполнение программы, то просто цикл завершится
// и мы получим пустой стек
