// 7

package main

import (
	"constraints"
	"errors"
)

// 7.8 метод удаления всех дубликатов из упорядоченного списка. Для этого в метод find() был добавлен параметр startNode
func (l *OrderedList[T]) CleanDuplicates() {
	if l.head == nil {
		return
	}

	curNode := l.head

	for true {
		nextNode := curNode.next
		if nextNode == nil {
			return
		}
		if l.compareValues(curNode.value, nextNode.value) == 0 {
			curNode.next = nextNode.next
			if nextNode.next != nil {
				nextNode.next.prev = curNode
			}
			nextNode.prev = nil
			nextNode.next = nil
		} else {
			curNode = nextNode
		}
	}
}

// 7.9 слияние двух упорядоченных списков в один, сохраняя порядок элементов.
// Сложность O(n+m), где n и m - размеры списков.
func MergeOrderedLists[T constraints.Ordered](list1 *OrderedList[T], list2 *OrderedList[T]) (*OrderedList[T], error) {
	var newHead, newTail *Node[T]

	if list1._ascending != list2._ascending {
		return nil, errors.New("Lists have different sorting directions")
	}

	result := &OrderedList[T]{
		_ascending: list1._ascending,
		compare:    list1.compare,
	}

	node1 := list1.head
	node2 := list2.head

	for node1 != nil && node2 != nil {
		var selected *Node[T]

		if result.compareValues(node1.value, node2.value) <= 0 {
			selected = node1
			node1 = node1.next
		} else {
			selected = node2
			node2 = node2.next
		}

		newNode := &Node[T]{value: selected.value}
		if newHead == nil {
			newHead = newNode
		} else {
			newTail.next = newNode
			newNode.prev = newTail
		}
		newTail = newNode
	}

	for node1 != nil {
		newNode := &Node[T]{value: node1.value}
		if newHead == nil {
			newHead = newNode
		} else {
			newTail.next = newNode
			newNode.prev = newTail
		}
		newTail = newNode
		node1 = node1.next
	}

	for node2 != nil {
		newNode := &Node[T]{value: node2.value}
		if newHead == nil {
			newHead = newNode
		} else {
			newTail.next = newNode
			newNode.prev = newTail
		}
		newTail = newNode
		node2 = node2.next
	}

	result.head = newHead
	result.tail = newTail
	return result, nil
}

// 7.10 метод проверки наличия заданного упорядоченного под-списка (параметр метода) в текущем списке. O(n*m) поскольку
// надо обработать случаи, когда не известно с какого именно повторяющегося элемента начнется подсписок
func (l *OrderedList[T]) HasSublist(sublist *OrderedList[T]) bool {
	if sublist.head == nil {
		return true
	}

	for startNode := l.head; startNode != nil; startNode = startNode.next {
		subNode := sublist.head
		node := startNode

		for true {
			if l.compareValues(node.value, subNode.value) != 0 {
				break
			}
			node = node.next
			subNode = subNode.next

			if node == nil && subNode != nil {
				return false
			}

			if subNode == nil {
				return true
			}
		}
	}

	return false
}

// 7.11 метод, который находит наиболее часто встречающееся значение в списке.
// O(n) по времени, O(1) по памяти
func (l *OrderedList[T]) MostFrequentElement() (T, error) {
	var zero T

	if l.head == nil {
		return zero, errors.New("Empty list")
	}

	var elem *Node[T] = l.head
	var frequent int = 1

	var currentElem *Node[T] = l.head
	var frequentCurrent int = 1

	for node := l.head.next; node != nil; node = node.next {
		if currentElem.value == node.value {
			frequentCurrent++
		} else {
			if frequentCurrent > frequent {
				frequent = frequentCurrent
				elem = currentElem
			}
			currentElem = node
			frequentCurrent = 1
		}
	}

	if frequentCurrent > frequent {
		elem = currentElem
	}

	return elem.value, nil
}

// 7.12  возможность найти индекс элемента (параметр) в списке, которая должна работать за O(log N)
// бинарный поиск по упорядоченному массиву. В случае go применим слайсы, поскольку нам нужен доступ по индексу
type OrderedList2[T constraints.Ordered] struct {
	orderedList []T
	_ascending  bool
	compare     Comparator[T]
	zero        T
}

func MakeOrderedList2[T constraints.Ordered](direction string, cmp Comparator[T]) (*OrderedList2[T], error) {
	var _ascending bool

	switch direction {
	case "asc":
		_ascending = true
	case "desc":
		_ascending = false
	default:
		return nil, errors.New("Wrong value for ordering direction!")
	}

	return &OrderedList2[T]{
		orderedList: make([]T, 0),
		_ascending:  _ascending,
		compare:     cmp,
	}, nil
}

func (l *OrderedList2[T]) Count() int {
	return len(l.orderedList)
}

func (l *OrderedList2[T]) compareValues(v1, v2 T) int {
	comp := l.compare(v1, v2)
	if !l._ascending {
		return -comp
	}
	return comp
}

func (l *OrderedList2[T]) FindIndex(n T) int {
	left, right := 0, len(l.orderedList)-1

	for left <= right {
		mid := (left + right) / 2
		cmp := l.compareValues(l.orderedList[mid], n)

		if cmp == 0 {
			return mid
		} else if cmp < 0 {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return -1 // Элемент не найден
}

// Рефлексия
// 5.3 Я немного перемудрил, возможно, но в принципе так и реализовано. На отдельных нодах проще, на списках сложнее
// из-за необходимости управлять индексами

// 5.4 Так и сделано. Вход - в один стек, выход - из другого, который заплоняем, если пуст

// 5.5 Интересный подход со стеком. Я обращал связи нод, но если исплоьзовать очереди и стеки - получается более наглядно
// и более высокоуровнево

// 5.6 Единственное отличие от эталона - я не оставлял пустую ячейку, а считал количество элементов в очереди. Где-то в
// следующих заданиях я с тем же самым примерно столкнулся и корректировал индекс хвоста сдвигом назад.
