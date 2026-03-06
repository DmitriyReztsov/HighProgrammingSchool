// 7

package main

import (
	"constraints"
	"errors"
	"strings"
	"os"
)

type Node[T constraints.Ordered] struct {
	prev  *Node[T]
	next  *Node[T]
	value T
}

type OrderedList[T constraints.Ordered] struct {
	head       *Node[T]
	tail       *Node[T]
	_ascending bool
	compare    Comparator[T]
}

// Операция посчета стоит нам O(n), что дорого, но условие задачи - не менять сигнатуру и структуру :)
func (l *OrderedList[T]) Count() int {
	counter := 0

	for node := l.head; node != nil; node = node.next {
		counter++
	}
	return counter
}

// 7.3 Добавление элемента с учетом его значения и направления упорядоченности. Поскольку мы в текущей реализации не
// управляем индексами элементов, наш список - это отдельные ноды, хранящие ссылки друг на друга, а не непрерывный блок
// в памяти, то операция вставки в худшем случае будет занимать O(n) по времени. По памяти дополнительных структур не
// требуется, поэтому O(1)
func (l *OrderedList[T]) Add(item T) {
	var nextNode *Node[T]

	newNode := &Node[T]{value: item}
	if l.head == nil {
		l.head = newNode
		l.tail = newNode
		return
	}

	for node := l.head; node != nil; node = node.next {
		if l.compareValues(node.value, item) > 0 {
			nextNode = node
			break
		}
	}
	if nextNode == nil {
		newNode.prev = l.tail
		l.tail.next = newNode
		l.tail = newNode
		return
	}

	if nextNode != l.head {
		nextNode.prev.next = newNode
		newNode.prev = nextNode.prev
	}
	nextNode.prev = newNode
	newNode.next = nextNode
	if nextNode == l.head {
		l.head = newNode
	}
	return
}

// 7.6 Функция поиска в текущей сигнатуре возвращает копию ноды. Если так и задумано, то будут создавать новые ноды,
// которые нужны только для транспортировки значения (если сохранить nil в качестве next / prev), либо будут ноды со
// ссылками на оригинальные ноды списка, но сделав, например, node.next.prev мы попадаем на оригинальную ноду списка,
// а не на ноду, возвращенную этим методом. В общем, я реализую как написано, но сигнатура странная.
// Сложность будет O(n), от признака упорядоченности тут мало что зависит в общем.
func (l *OrderedList[T]) Find(n T) (Node[T], error) {
	originalNode, err := l.find(n, l.head)
	if err != nil {
		return Node[T]{}, err
	}

	return Node[T]{value: originalNode.value, next: originalNode.next, prev: originalNode.prev}, nil
}

func (l *OrderedList[T]) find(n T, startNode *Node[T]) (*Node[T], error) {
	for node := startNode; node != nil; node = node.next {
		if l.compareValues(node.value, n) > 0 {
			return nil, errors.New("Not found")
		}
		if l.compareValues(node.value, n) == 0 {
			return node, nil
		}
	}
	return nil, errors.New("Not found")
}

// 7.4. Удаление элемента по значению. Операция поиска элемента будет стоить нам O(n) в силу того, что мы не оперируем
// индексами, поэтому надо перебрать все (в худшем случае) элементы
func (l *OrderedList[T]) Delete(n T) {
	nodeToDel, err := l.find(n, l.head)

	if err != nil {
		return
	}

	if nodeToDel == l.head && nodeToDel != l.tail {
		l.head = nodeToDel.next
		nodeToDel.next.prev = nil
		nodeToDel.next = nil
		return
	}

	if nodeToDel == l.tail && nodeToDel != l.head {
		l.tail = nodeToDel.prev
		nodeToDel.prev.next = nil
		nodeToDel.prev = nil
		return
	}

	if nodeToDel == l.tail && nodeToDel == l.head {
		l.head = nil
		l.tail = nil
		return
	}

	nodeToDel.prev.next = nodeToDel.next
	nodeToDel.next.prev = nodeToDel.prev
	nodeToDel.next = nil
	nodeToDel.prev = nil
	return
}

func (l *OrderedList[T]) Clear(asc bool) {
	l.head = nil
	l.tail = nil
}

// 7.2 Сравнение экземпляров. Выглядит как будто в заготовке уже реализовано, если мы сюда передаем не ноды, а сразу
// значения нод
// После выполнения 7.5 утратил актуальность, переделан в функцию-компаратор
func (l *OrderedList[T]) Compare(v1 T, v2 T) int {
	if v1 < v2 {
		return -1
	}
	if v1 > v2 {
		return +1
	}
	return 0
}

func (l *OrderedList[T]) compareValues(v1, v2 T) int {
	var result int

	if l.compare != nil {
		result = l.compare(v1, v2)
	} else {
		result = l.Compare(v1, v2)
	}

	if l._ascending {
		return result
	}
	return -result
}

// 7.5 Для реализации концепции класса-генерика в Go сделаем компаратор как функцию и будем ее передавать в конструкторе
// списка. Тогда мы сможем сделать произвольное количество таких функций под разные типы данных.
// Это и реализет концепцию дженерика.
type Comparator[T any] func(a, b T) int

func IntComparator(v1, v2 int) int {
	if v1 < v2 {
		return -1
	}
	if v1 > v2 {
		return +1
	}
	return 0
}

func StringComparator(v1, v2 string) int {
	v1 = strings.TrimSpace(v1)
	v2 = strings.TrimSpace(v2)

	if v1 < v2 {
		return -1
	}
	if v1 > v2 {
		return +1
	}
	return 0
}

// 7.1 реализация дополнительной опции для определения направления упорядочивания. Решил сделать в более декларативном стиле
// 7.5 добавил компаратор
func MakeOrderedList[T constraints.Ordered](direction string, cmp Comparator[T]) (*OrderedList[T], error) {
	var _ascending bool

	switch direction {
	case "asc":
		_ascending = true
	case "desc":
		_ascending = false
	default:
		return nil, errors.New("Wrong value for ordering direction!")
	}

	return &OrderedList[T]{_ascending: _ascending, compare: cmp}, nil
}
