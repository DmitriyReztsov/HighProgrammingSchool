package main

import (
	"os"
	"reflect"
)

// Рефлексии пока, видимо, нет. Напишу в следующей сдаче.
// Надеюсь, что кириллица в рефлексии не сломает ничего.

// 1.8 функция получает на вход два связных списка и возвращает список, каждый элемент которого равен сумме соответствующих элементов входных списков.
// time complexity O(n); space complexity O(n)
func MergeLists (l1, l2 *LinkedList) LinkedList {
	count1 := l1.Count()
	count2 := l2.Count()
	if count1 != count2 || count1 == 0 {
		return LinkedList{}
	}

	mergedList := LinkedList{}
	n1 := l1.head
	n2 := l2.head
	mergedList.head = &Node{value: n1.value + n2.value}
	mNode := mergedList.head
	for true {
		if n1.next == nil {
			break
		}

		n1 = n1.next
		n2 = n2.next
		mNode.next = &Node{value: n1.value + n2.value}
		mNode = mNode.next
	}
	mergedList.tail = mNode
	return mergedList
}

