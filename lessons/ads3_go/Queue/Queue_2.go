// 5

package main

import (
	"errors"
	"myproject/Stack"
)

// 5.3. Кольцевая очередь на ограниченном массиве
type QueueC[T any] struct {
	head     int
	tail     int
	size     int
	capacity int
	queue    []T
}

func (qc *QueueC[T]) Init(capacity int) {
	qc.size = 0
	qc.capacity = capacity
	qc.queue = make([]T, capacity)
}

func (qc *QueueC[T]) Size() int {
	return qc.size
}

func (qc *QueueC[T]) getHead() T {
	return qc.queue[qc.head]
}

func (qc *QueueC[T]) calculateNextIndex(ind int) int {
	if ind+1 == qc.capacity {
		return 0
	}
	return ind + 1
}

func (qc *QueueC[T]) removeHead() {
	var zero T

	qc.queue[qc.head] = zero
	qc.head = qc.calculateNextIndex(qc.head)
	qc.size--
}

func (qc *QueueC[T]) Dequeue() (T, error) {
	var result T
	var zero T

	if qc.size == 0 {
		return zero, errors.New("Empty queue")
	}

	result = qc.getHead()
	qc.removeHead()
	return result, nil
}

func (qc *QueueC[T]) Enqueue(itm T) error {
	if qc.size == qc.capacity {
		return errors.New("Queue is full")
	}

	if qc.size == 0 {
		qc.head = 0
		qc.tail = 0
	} else {
		qc.tail = qc.calculateNextIndex(qc.tail)
	}
	qc.queue[qc.tail] = itm
	qc.size++
	return nil
}

// функция, вращающая очередь, реализованную выше
func RotateQueue[T any](queue *QueueC[T], rotateNum int) {
	if queue.size == 0 {
		return
	}

	for i := 0; i < rotateNum; i++ {
		val, err := queue.Dequeue()
		if err != nil {
			return
		}
		err = queue.Enqueue(val)
		if err != nil {
			return
		}
	}
}

// 5.4 Очередь на двух стеках
type QueueS[T any] struct {
	inbox  stack.Stack[T]
	outbox stack.Stack[T]
	zero   T
}

func (qs *QueueS[T]) Enqueue(itm T) {
	qs.inbox.Push(itm)
}

func (qs *QueueS[T]) Dequeue() (T, error) {
	if qs.outbox.Size() == 0 && qs.inbox.Size() == 0 {
		return qs.zero, errors.New("Queue is empty")
	}
	if qs.outbox.Size() == 0 {
		err := qs.refillOutbox()
		if err != nil {
			return qs.zero, errors.New("Queue is broken")
		}
	}

	return qs.outbox.Pop()
}

func (qs *QueueS[T]) refillOutbox() error {
	for i := qs.inbox.Size(); i > 0; i = qs.inbox.Size() {
		elem, err := qs.inbox.Pop()
		if err != nil {
			return errors.New("Queue is empty")
		}

		qs.outbox.Push(elem)
	}
	return nil
}

func (qs *QueueS[T]) Size() int {
	return qs.outbox.Size() + qs.inbox.Size()
}

// 5.5. Обращение элементов в обратный порядок. В зависимости от реализации очереди надо либо создать копированием новый
// слайс в обратном порядке элементов, либо поменять направления в связном списке. Моя очередь реализована на связном
// списке - обращаем связи.
func ReverseQueue[T any](q *Queue[T]) {
	for node := q.tail; node != nil; node = node.next {
		n := node.next
		node.next = node.prev
		node.prev = n
	}
	n := q.head
	q.head = q.tail
	q.tail = n
}

// 5.6 см. п. 5.3. Поясню: вращение очереди на связном списке не представляет никакой сложности - забрать элемент и
// вставить его обратно - просто два метода, повторяющиеся N раз. Поэтому я в том задании реализовал очередь на
// ограниченном массиве. А оказалось, что эта реализация - отдельное задание :)) (да, как-то получилось, что я не читал
// все задания до выполнения, а выполнял и вчитывался по-очереди)

// Рефлексия по теме 3.
// 5.6. Динамический массив на основе банковского метода. Я вчитывался в разные источники, пытаясь понять эту тему. Как
// писал - вычитал, что банковский метод - больше говорит не о реализации, а о схеме рассуждения. Моя реализация учла
// ваше замечание о том, что списание и увеличение массива должно быть степенью двойки, постарался это отразить в формуле
// перерасчета. По сути дела, я просто описал подход удвоения массива при его полном заполнении. Поэтому "Когда надо
// выполнять реаллокацию, вопрос неоднозначный, можно по некоторому порогу в банке, но лучше когда внутренний массив весь
// заполнен." - тоже учтено, получилось. В принципе, этот подход и оправдан, поскольку для целей получения среднего О(1)
// надо делать реаллокации как можно реже, по необходимости.

// 5.7. Вот тут ваш подход - это для меня мини-откровение. Я "в лоб" пошел городить несколько списков списков списков ...
// То, что у нас есть фиксированный размер массивов и, значит, мы может сэмулировать выделение непрерывной памяти в виде
// просто одномерного массива - классная идея. Тут мне не хватило фантазии и, может, насмотренности технических идей.
// В мемориз, однозначно.
