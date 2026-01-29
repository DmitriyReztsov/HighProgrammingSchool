// 2

package main

import (
	"errors"
	"os"
	"reflect"
)

type Node struct {
	prev  *Node
	next  *Node
	value int
}

type LinkedList2 struct {
	head *Node
	tail *Node
}

func (l *LinkedList2) AddInTail(item Node) {
	if l.head == nil {
		l.head = &item
		l.head.next = nil
		l.head.prev = nil
	} else {
		l.tail.next = &item
		item.prev = l.tail
	}

	l.tail = &item
	l.tail.next = nil
}

func (l *LinkedList2) Count() int {
	if l.head == nil {
		return 0
	}
	cursor := l.head
	for counter := 1; ; counter++ {
		if cursor.next == nil {
			return counter
		}
		cursor = cursor.next
	}
}

// 2.1 looking for a first Node by value
// time complexity O(n); space complexity O(1)
// error не nil, если узел не найден
func (l *LinkedList2) Find(n int) (Node, error) {
	node, err := l.findLink(n)
	if err == nil {
		return *node, err
	}
	return Node{value: -1, next: nil}, err
}

func (l *LinkedList2) findLink(n int) (*Node, error) {
	cursor := l.head
	for true {
		if cursor == nil {
			break
		}
		if cursor.value == n {
			return cursor, nil
		}
		cursor = cursor.next
	}
	return nil, errors.New("Node not found")
}

// 2.2 looking for all nodes with the given value
// time complexity O(n); space complexity O(n) for returning array
func (l *LinkedList2) FindAll(n int) []Node {
	nodes := []Node{}
	listSlice := *l
	for true {
		node, err := listSlice.Find(n)
		if err != nil {
			break
		}
		nodes = append(nodes, node)
		listSlice.head = node.next
	}
	return nodes
}

// 2.3 & 2.4 deletion by value
// time complexity O(n); space complexity O(1)
func (l *LinkedList2) Delete(n int, all bool) {
	node := l.head

	for true {
		if node == nil {
			break
		}
		if node.value != n {
			node = node.next
			continue
		}
		if node.prev == nil {
			l.head = node.next
		}
		if node.next == nil {
			l.tail = node.prev
		}
		if node.prev != nil {
			node.prev.next = node.next
		}
		if node.next != nil {
			node.next.prev = node.prev
		}
		if !all {
			break
		}
		node = node.next
	}
}

// 2.5 insertion of a node after the given node
// time complexity O(1); space complexity O(1)
func (l *LinkedList2) Insert(after *Node, add Node) {
	add.next = after.next
	add.prev = after
	after.next = &add

	if after == l.tail {
		l.tail = &add
	}
}

// 2.6 insertion of the first node
// time complexity O(1); space complexity O(1)
func (l *LinkedList2) InsertFirst(first Node) {
	if l.head == nil {
		l.head = &first
		l.tail = &first
		return
	}
	l.head.prev = &first
	first.next = l.head
	l.head = &first
}

// 2.7 clean up of the list
// time complexity O(1); space complexity O(1)
func (l *LinkedList2) Clean() {
	l.head = nil
	l.tail = nil
}

