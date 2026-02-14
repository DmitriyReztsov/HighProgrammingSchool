// 5

package main

import (
	"errors"
	"os"
)

// Поскольку в слайсах операция добавления по индексу будет нам стоить O(n) на копирование слайса, то
// эффективнее воспользоваться связным списком для неограниченной очереди - тогда все операции 
// будут стоить O(1)
type Node[T any] struct {
	value T
	next  *Node[T]
	prev  *Node[T]
}

// 5.1.
type Queue[T any] struct {
	head *Node[T]
	tail *Node[T]
	size int
}

// 5.1.
func (q *Queue[T]) Size() int {
	return q.size
}

func (q *Queue[T]) getHead() T {
	return q.head.value
}

func (q *Queue[T]) removeHead() {
	newHead := q.head.next

	q.head.prev = nil
	q.head.next = nil
	q.head = newHead
	if q.head != nil {
		q.head.prev = nil
	} else {
		q.tail = nil
	}
	q.size--
}

// 5.1.
func (q *Queue[T]) Dequeue() (T, error) {
	var result T
	var zero T

	if q.size == 0 {
		return zero, errors.New("Empty queue")
	}

	result = q.getHead()
	q.removeHead()
	return result, nil
}

// 5.1.
func (q *Queue[T]) Enqueue(itm T) {
	n := &Node[T]{value: itm, prev: q.tail}

	if q.size == 0 {
		q.head = n
	} else {
		q.tail.next = n
	}
	q.tail = n
	q.size++
}

// 5.2. В этой реализации добавление и получение значения будет стоить O(1) для временной и пространственнй сложности
