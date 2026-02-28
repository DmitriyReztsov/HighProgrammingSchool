// 6

package main

import (
	"errors"
	"os"
)

// так же, как и с очередью, если пользоваться одним слайсом - то это дорогие операции вставки / удаления в 0-й индекс -
// не важно, будет ли он головой или хвостом. Как вариант можно было бы воспользоваться двумя слайсами - один для вставки
// и выдачи из головы, второй - из хвоста. Это снимет проблему вставки / удаления, добавит периодические (не на каждую
// операцию) копирования из одного слайса в другой, что в среднем самортизируется в О(1), но останется проблема динамического
// расширения слайса и копирования содержимого, плюс реальная сложность будет очень зависеть от соотношения операций на
// голове и хвосте. Самым универсальным выглядит очередь на основе двунаправленного списка. Поскольку нам нет нужды
// получать элементы очереди по индексу, достаточно держать голову и хвост и тогда все операции записи и получения будут О(1)

type Node[T any] struct {
	prev  *Node[T]
	next  *Node[T]
	value T
}

type Deque[T any] struct {
	head *Node[T]
	tail *Node[T]
	size int
	zero T
}

func (d *Deque[T]) Size() int {
	return d.size
}

func (d *Deque[T]) AddFront(itm T) {
	n := &Node[T]{next: d.head, value: itm}
	if d.head != nil {
		d.head.prev = n
	} else {
		d.tail = n
	}

	d.head = n
	d.size++
}

func (d *Deque[T]) AddTail(itm T) {
	n := &Node[T]{prev: d.tail, value: itm}
	if d.tail != nil {
		d.tail.next = n
	} else {
		d.head = n
	}

	d.tail = n
	d.size++
}

func (d *Deque[T]) RemoveFront() (T, error) {
	var result T

	if d.size == 0 {
		return d.zero, errors.New("Empty Dequeue")
	}
	result = d.head.value

	d.head = d.head.next
	if d.head != nil {
		d.head.prev.next = nil
		d.head.prev = nil
	} else {
		d.tail = nil
	}

	if d.size > 0 {
		d.size--
	}

	return result, nil
}

func (d *Deque[T]) RemoveTail() (T, error) {
	var result T

	if d.size == 0 {
		return d.zero, errors.New("Empty Dequeue")
	}
	result = d.tail.value

	d.tail = d.tail.prev
	if d.tail != nil {
		d.tail.next.prev = nil
		d.tail.next = nil
	} else {
		d.head = nil
	}

	d.size--
	return result, nil
}
