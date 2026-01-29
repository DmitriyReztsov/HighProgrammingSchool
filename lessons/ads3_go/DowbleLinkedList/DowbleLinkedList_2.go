// 2

package main

import (
	"errors"
	"os"
	"reflect"
)

// В плане рефлексии отметить, что подход с DummyNode в Go требует дисципинированного подхода к использованию
// соглашений. Поскольку в Го нет классов как таковых и нет возможности перегружать их методы, а также по сути нет
// геттеров и сеттеров в том смысле, в каком они есть в Питоне, то получение головы и хвоста списка, которые
// зафикисированы на DummyNode не представляет сложности и перегрузить их получение как я делал в Питоне не получится.
// Соответственно, использование функций, связанных со структурой, для получение тех или иных аттрибутов становится
// важным.

// 2.9 reverse the list
// time complexity O(n); space complexity O(1)
func (l *LinkedList2) Reverse() {
	for node := l.tail; node != nil; node = node.next {
		n := node.next
		node.next = node.prev
		node.prev = n
	}
	n := l.head
	l.head = l.tail
	l.tail = n
}

// 2.10 looking for a loop in the array
// time complexity O(n); space complexity O(n) for axillary map
func (l *LinkedList2) HasLoop() bool {
	visitedMapping := make(map[*Node]map[string]bool)
	for node := l.head; node != nil; node = node.next {
		_, exists := visitedMapping[node]
		if exists {
			return true
		}
		visitedMapping[node] = map[string]bool{"forward": true, "reverse": false}
	}

	for node := l.tail; node != nil; node = node.prev {
		visitedNode, exists := visitedMapping[node]
		if !exists {
			return true
		}
		if visitedNode["reverse"] {
			return true
		}
		visitedNode["reverse"] = true
	}

	for _, visited := range visitedMapping {
		if !visited["reverse"] {
			return true
		}
	}
	return false
}

func mergeSort(nodeMap map[int]*Node) map[int]*Node {
	if len(nodeMap) <= 1 {
		return nodeMap
	}

	midInd := len(nodeMap) / 2

	leftNodeMap := map[int]*Node{}
	for i := range midInd {
		leftNodeMap[i] = nodeMap[i]
	}
	leftNodeMap = mergeSort(leftNodeMap)

	rightNodeMap := map[int]*Node{}
	for i := midInd; i < len(nodeMap); i++ {
		rightNodeMap[i-midInd] = nodeMap[i]
	}
	rightNodeMap = mergeSort(rightNodeMap)
	return merge(leftNodeMap, rightNodeMap)
}

func merge(leftNodeMap, rightNodeMap map[int]*Node) map[int]*Node {
	sortedNodes := map[int]*Node{}
	s := 0
	i := 0
	j := 0

	for true {
		if i >= len(leftNodeMap) || j >= len(rightNodeMap) {
			break
		}

		if leftNodeMap[i] == nil || rightNodeMap[j] == nil {
			break
		}

		if leftNodeMap[i].value < rightNodeMap[j].value {
			sortedNodes[s] = leftNodeMap[i]
			i += 1
		} else {
			sortedNodes[s] = rightNodeMap[j]
			j += 1
		}
		s++
	}

	for true {
		_, exists := leftNodeMap[i]
		if !exists {
			break
		}
		sortedNodes[s] = leftNodeMap[i]
		s++
		i++
	}
	for true {
		_, exists := rightNodeMap[j]
		if !exists {
			break
		}
		sortedNodes[s] = rightNodeMap[j]
		s++
		j++
	}

	return sortedNodes
}

func convertListToMap(l *LinkedList2) map[int]*Node {
	indexNodeMap := map[int]*Node{}
	ind := 0
	for node := l.head; node != nil; node = node.next {
		indexNodeMap[ind] = node
		ind++
	}
	return indexNodeMap
}

func convertMapToList(indexNodeMap map[int]*Node, l *LinkedList2) {
	for ind, node := range indexNodeMap {
		if ind == 0 {
			node.prev = nil
		} else {
			n, ok := indexNodeMap[ind-1]
			if ok {
				node.prev = n
			}
		}
		if ind == len(indexNodeMap)-1 {
			node.next = nil
		} else {
			n, ok := indexNodeMap[ind+1]
			if ok {
				node.next = n
			}
		}
	}
	l.head = indexNodeMap[0]
	l.tail = indexNodeMap[len(indexNodeMap)-1]
}

// 2.11 Sort the array
// Можно было бы сортировать пузырьком, для этого списка это было бы не сложно, перестановка нод выглядит
// тривиально. Сложность по времени была бы O(n**(n/2)), по памяти O(1) если сортировать на месте.
// Решил попробовать реализовать сортировку слиянием. Была сложность с тем, что нет индексов. Решил ее использованием
// мап (чтобы не собирать список - было бы совсем масло масляное). Сейчас думаю,что можно было бы, конечно, попробовать
// и через создание связных списков. Просто на осознание механики всех указателей и переставки нод ушло бы больше
// времени. Все-таки, влияние Питона сильно.
// time complexity O(n*log(n)); space complexity O(n) на создание дополнительных мап на каждом этапе
func (l *LinkedList2) Sort() {
	indexNodeMap := convertListToMap(l)
	indexNodeMap = mergeSort(indexNodeMap)

	convertMapToList(indexNodeMap, l)
}

// 2.12 Объединение двух списков в третий с сортировкой. В общем, можно уже тут скомбинировать уже написанные методы
// time complexity O(n*log(n)); space complexity O(n)
func MergeSort(l1, l2 *LinkedList2) LinkedList2 {
	l1.Sort()
	l2.Sort()
	listMap1 := convertListToMap(l1)
	listMap2 := convertListToMap(l2)

	resultMap := merge(listMap1, listMap2)

	resultList := LinkedList2{}
	convertMapToList(resultMap, &resultList)
	return resultList
}

// 2.13 DummyNode
// Для наглядности дбавил несколько функций, которые стоит использовать при использовании этого типа структуры.
// Получать голову и хвост в этом подходе лучше не напрямую. А так - переписал основные методы под DummyNode,
// выглядит и читается легче и проще.
type NodeD struct {
	prev  *NodeD
	next  *NodeD
	value int
	dummy bool
}

type LinkedList2D struct {
	head *NodeD
	tail *NodeD
}

func NewList() *LinkedList2D {
	head := &NodeD{dummy: true}
	tail := &NodeD{dummy: true}

	head.next = tail
	tail.prev = head

	return &LinkedList2D{head: head, tail: tail}
}

func (l *LinkedList2D) getHead() *NodeD {
	return l.head.next
}

func (l *LinkedList2D) GetHead() *NodeD {
	if l.getHead().dummy {
		return nil
	}
	return l.getHead()
}

func (l *LinkedList2D) getTail() *NodeD {
	return l.tail.prev
}

func (l *LinkedList2D) GetTail() *NodeD {
	if l.getTail().dummy {
		return nil
	}
	return l.getTail()
}

func (l *LinkedList2D) AddInTailD(item NodeD) {
	l.InsertD(l.tail.prev, item)
}

func (l *LinkedList2D) CountD() int {
	if l.getHead().dummy {
		return 0
	}

	counter := 1
	for node := l.getHead(); node != l.tail; node = node.next {
		counter++
	}
	return counter
}

func (l *LinkedList2D) FindD(n int) (NodeD, error) {
	node, err := l.findLinkD(n)
	if err == nil {
		return *node, err
	}
	return NodeD{value: -1, next: nil}, err
}

func (l *LinkedList2D) findLinkD(n int) (*NodeD, error) {
	for node := l.getHead(); node != l.tail; node = node.next {
		if node.value == n {
			return node, nil
		}
	}
	return nil, errors.New("Node not found")
}

func (l *LinkedList2D) FindAll(n int) []NodeD {
	nodes := []NodeD{}
	listSlice := *l
	for true {
		node, err := listSlice.FindD(n)
		if err != nil {
			break
		}
		nodes = append(nodes, node)
		listSlice.head = node.next
	}
	return nodes
}

func (l *LinkedList2D) DeleteD(n int, all bool) {
	for node := l.getHead(); node != l.tail; node = node.next {
		if node.value == n {
			node.prev.next = node.next
			node.next.prev = node.prev

			if !all {
				break
			}
		}
	}
}

func (l *LinkedList2D) InsertD(after *NodeD, add NodeD) {
	add.next = after.next
	add.prev = after
	after.next = &add
}

func (l *LinkedList2D) InsertFirstD(first NodeD) {
	l.InsertD(l.head, first)
}

func (l *LinkedList2D) CleanD() {
	l.head.next = l.tail
	l.tail.prev = l.head
}
