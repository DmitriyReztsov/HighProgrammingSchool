// 1

package main

import (
	"errors"
	"os"
	"reflect"
)

type Node struct {
	next  *Node
	value int
}

type LinkedList struct {
	head *Node
	tail *Node
}

func (l *LinkedList) AddInTail(item Node) {
	if l.head == nil {
		l.head = &item
	} else {
		l.tail.next = &item
	}

	l.tail = &item
}

// 1.5 count method. time complexity O(n); space complexity O(1)
func (l *LinkedList) Count() int {
	if l.head == nil {
		return 0
	}

	node := l.head
	for counter := 1; ; counter++ {
		node = node.next
		if node == nil {
			return counter
		}
	}
}

//1.4 find by value. time complexity O(n); space complexity O(1)
func (l *LinkedList) Find(n int) (Node, error) {
	node := l.head
	for true {
		if node == nil {
			break
		}
		if node.value == n {
			return *node, nil
		}
		node = node.next
	}
	return Node{value: -1, next: nil}, errors.New("Node not found")
}

func (l *LinkedList) findLink(n int) (*Node, error) {
	node := l.head
	for true {
		if node == nil {
			break
		}
		if node.value == n {
			return node, nil
		}
		node = node.next
	}
	return nil, errors.New("Node not found")
}

// 1.4. find all nodes by value. time complexity O(n); space complexity O(n)
func (l *LinkedList) FindAll(n int) []Node {
	nodes := []Node{}
	node := l.head
	for true {
		if node == nil {
			break
		}
		if node.value == n {
			nodes = append(nodes, *node)
		}
		node = node.next
	}
	return nodes
}

func (l *LinkedList) findAllLinks(n int) map[*Node]bool {
	nodes := map[*Node]bool{}
	node := l.head
	for true {
		if node == nil {
			break
		}
		if node.value == n {
			nodes[node] = true
		}
		node = node.next
	}
	return nodes
}

// 1.1 + 1.2 deletion of node(s) by value.
// time complexity O(n); space complexity O(1)
func (l *LinkedList) Delete(n int, all bool) {
	// look for head
	skip := false
	for true {
		if l.head == nil {
			break
		}
		if l.head.value != n {
			break
		}
		
		l.head = l.head.next
		if !all {
			skip = true
			break
		}
	}

	// go on with the rest of nodes
	parent := l.head
	if parent == nil {
		return
	}

	node := parent.next
	for true {
		if node == nil {
			break
		}
		if node.value != n || skip {
			node = node.next
			parent = parent.next
		} else {
			parent.next = node.next
			node = node.next
			if !all {
				skip = true
			}
		}
	}
	l.tail = parent
}

// 1.6 insertion after given node.
// time complexity O(n); space complexity O(1)
func (l *LinkedList) Insert(after *Node, add Node) {
	if l.tail == after {
		l.tail.next = &add
		l.tail = &add
		return
	}
	node := l.head
	for true {
		if node == nil {
			return
		}
		if node == after {
			add.next = node.next
			node.next = &add
			return
		}
		node = node.next
	}
}

// time complexity O(1); space complexity O(1)
func (l *LinkedList) InsertFirst(first Node) {
	first.next = l.head
	l.head = &first
	if l.tail == nil {
		l.tail = &first
	}
}

// 1.3 cleaning of list
// time complexity O(1); space complexity O(1)
func (l *LinkedList) Clean() {
	l.head = nil
	l.head = nil
}

