// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import "testing"

func TestAddInTail(t *testing.T) {
	list := &LinkedList2{}
	node1 := Node{value: 10}
	node2 := Node{value: 20}

	list.AddInTail(node1)
	if list.head.value != 10 {
		t.Fatalf("Expected head value 10, got %d", list.head.value)
	}
	if list.tail.value != 10 {
		t.Fatalf("Expected head value 10, got %d", list.head.value)
	}

	list.AddInTail(node2)

	if list.head.value != 10 {
		t.Fatalf("Expected head value 10, got %d", list.head.value)
	}

	if list.tail.value != 20 {
		t.Fatalf("Expected tail value 20, got %d", list.tail.value)
	}
}

func TestCount(t *testing.T) {
	list := &LinkedList2{}
	count := list.Count()

	if count != 0 {
		t.Errorf("Expected count 0, got %d", count)
	}

	node1 := Node{value: 10}
	node2 := Node{value: 20}
	node1.next = &node2
	node2.prev = &node1

	list.head = &node1
	list.tail = &node2

	count = list.Count()

	if count != 2 {
		t.Errorf("Expected count 2, got %d", count)
	}
}

func TestFind(t *testing.T) {
	list := &LinkedList2{}
	_, err := list.Find(1)

	if err == nil {
		t.Errorf("Expected error on find in empty list, got nil")
	}

	node := &Node{value: 10}

	list.head = node
	headAddr := list.head
	list.tail = node
	_, err = list.Find(1)

	if err == nil {
		t.Errorf("Expected error on non-empty list, got nil")
	}

	nodeCopy, err := list.Find(10)
	if err != nil {
		t.Errorf("Expected nil on non-empty list, got error")
	}

	if nodeCopy.value != 10 {
		t.Errorf("Expected node with value 10, got smth else")
	}

	if nodeCopy.next != node.next {
		t.Errorf("Expected node.next is nodeCopy.next, got smth else")
	}

	for i := 0; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node.next = newNode
		newNode.prev = node
		node = newNode
	}
	list.tail = node
	tailAddr := list.tail

	count := list.Count()
	if count != 14 {
		t.Errorf("Expected count 14, got %d", count)
	}

	nodeCopy, err = list.Find(10)
	if err != nil {
		t.Errorf("Expected nil on non-empty list, got error")
	}

	if nodeCopy.value != 10 {
		t.Errorf("Expected node with value 10, got smth else")
	}

	nodeCopy, err = list.Find(120)
	if err != nil {
		t.Errorf("Expected nil on non-empty list, got error")
	}

	if nodeCopy.value != 120 {
		t.Errorf("Expected node with value 10, got smth else")
	}

	nodeCopy, err = list.Find(100)
	if err != nil {
		t.Errorf("Expected nil on non-empty list, got error")
	}

	if nodeCopy.value != 100 {
		t.Errorf("Expected node with value 10, got smth else")
	}

	nodeCopy, err = list.Find(1000)
	if err == nil {
		t.Errorf("Expected error on non-empty list with non-existing node, got nil")
	}

	if nodeCopy.value != -1 {
		t.Errorf("Expected node with default value 0, got smth else")
	}

	if list.head != headAddr || list.tail != tailAddr {
		t.Errorf("Expected list not modified")
	}
}

func TestFindAll(t *testing.T) {
	list := &LinkedList2{}
	nodeCopySlice := list.FindAll(1)

	if len(nodeCopySlice) > 0 {
		t.Errorf("Expected empty list, got non-empty")
	}

	node := &Node{value: 10}

	list.head = node
	headAddr := list.head
	list.tail = node
	nodeCopySlice = list.FindAll(1)

	if len(nodeCopySlice) > 0 {
		t.Errorf("Expected empty list, got non-empty")
	}

	nodeCopySlice = list.FindAll(10)
	if len(nodeCopySlice) != 1 {
		t.Errorf("Expected len list = 1, got smth else")
	}

	for _, node := range nodeCopySlice {
		if node.value != 10 {
			t.Errorf("Expected node with value 10, got smth else")
		}
	}

	// list with different nodes like 10 0 10 20 30 ... 120
	for i := 0; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node.next = newNode
		newNode.prev = node
		node = newNode
	}
	list.tail = node
	tailAddr := list.tail

	count := list.Count()
	if count != 14 {
		t.Errorf("Expected count 14, got %d", count)
	}

	nodeCopySlice = list.FindAll(10)
	if len(nodeCopySlice) != 2 {
		t.Errorf("Expected len list = 2, got smth else")
	}

	for _, node := range nodeCopySlice {
		if node.value != 10 {
			t.Errorf("Expected node with value 10, got smth else")
		}
	}

	nodeCopySlice = list.FindAll(20)
	if len(nodeCopySlice) != 1 {
		t.Errorf("Expected len list = 1, got smth else")
	}

	for _, node := range nodeCopySlice {
		if node.value != 20 {
			t.Errorf("Expected node with value 20, got smth else")
		}
	}

	nodeCopySlice = list.FindAll(120)
	if len(nodeCopySlice) != 1 {
		t.Errorf("Expected len list = 1, got smth else")
	}

	for _, node := range nodeCopySlice {
		if node.value != 120 {
			t.Errorf("Expected node with value 120, got smth else")
		}
	}

	nodeCopySlice = list.FindAll(100)
	if len(nodeCopySlice) != 1 {
		t.Errorf("Expected len list = 1, got smth else")
	}

	for _, node := range nodeCopySlice {
		if node.value != 100 {
			t.Errorf("Expected node with value 100, got smth else")
		}
	}

	nodeCopySlice = list.FindAll(1000)
	if len(nodeCopySlice) != 0 {
		t.Errorf("Expected len list = 0, got smth else")
	}

	// list2 with the same nodes like 10 10 10 10 10 ... 10
	list2 := &LinkedList2{}
	node2 := &Node{value: 10}
	list2.head = node2

	for i := 0; i <= 12; i++ {
		newNode2 := &Node{value: 10}
		node2.next = newNode2
		newNode2.prev = node2
		node2 = newNode2
	}
	list2.tail = node2

	count2 := list2.Count()
	if count2 != 14 {
		t.Errorf("Expected count 14, got %d", count2)
	}

	nodeCopySlice2 := list2.FindAll(10)
	if len(nodeCopySlice2) != 14 {
		t.Errorf("Expected len list = 14, got smth else")
	}

	for _, node := range nodeCopySlice2 {
		if node.value != 10 {
			t.Errorf("Expected node with value 10, got smth else")
		}
	}

	if list.head != headAddr || list.tail != tailAddr {
		t.Errorf("Expected list not modified")
	}
}

func TestDelete(t *testing.T) {
	list := &LinkedList2{}

	count := list.Count()
	if count != 0 {
		t.Errorf("Expected empty list, got non-empty")
	}

	list.Delete(1, false)
	count = list.Count()
	if count != 0 {
		t.Errorf("Expected empty list, got non-empty")
	}

	node := &Node{value: 10}

	list.head = node
	headAddr := list.head
	list.tail = node

	count = list.Count()
	if count != 1 {
		t.Errorf("Expected list with 1 node, got smth else")
	}

	list.Delete(1, false)
	count = list.Count()
	if count != 1 {
		t.Errorf("Expected list with 1 node, got smth else")
	}

	list.Delete(10, false)
	count = list.Count()
	if count != 0 {
		t.Errorf("Expected list with 0 node, got %d", count)
	}
	if list.head != nil || list.tail != nil {
		t.Errorf("Expected list with nil head and tail, got smth else")
	}

	// list with different nodes like 10 0 10 20 30 ... 120
	node = &Node{value: 10}
	list.head = node

	for i := 0; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node.next = newNode
		newNode.prev = node
		node = newNode
	}
	list.tail = node
	tailAddr := list.tail

	count = list.Count()
	if count != 14 {
		t.Errorf("Expected count 14, got %d", count)
	}

	list.Delete(20, false)
	count = list.Count()
	if count != 13 {
		t.Errorf("Expected count 13, got %d", count)
	}

	node = list.head
	for i := 0; i < count; i++ {
		if node.value == 20 {
			t.Errorf("Expected node with value 20 be removed, got smth else")
		}
		node = node.next
	}

	list.Delete(10, true)
	count = list.Count()
	if count != 11 {
		t.Errorf("Expected count 11, got %d", count)
	}

	node = list.head
	for i := 0; i < count; i++ {
		if node.value == 10 {
			t.Errorf("Expected node with value 10 be removed, got smth else")
		}
		node = node.next
	}

	list.Delete(120, true)
	count = list.Count()
	if count != 10 {
		t.Errorf("Expected count 10, got %d", count)
	}

	node = list.head
	for i := 0; i < count; i++ {
		if node.value == 120 {
			t.Errorf("Expected node with value 120 be removed, got smth else")
		}
		node = node.next
	}

	if list.head == headAddr || list.tail == tailAddr {
		t.Errorf("Expected list modified. Head value %d, tail value %d", list.head.value, list.tail.value)
	}

	// list2 with the same nodes like 10 10 10 10 10 ... 10
	list2 := &LinkedList2{}
	node2 := &Node{value: 10}
	list2.head = node2

	for i := 0; i <= 12; i++ {
		newNode2 := &Node{value: 10}
		node2.next = newNode2
		newNode2.prev = node2
		node2 = newNode2
	}
	list2.tail = node2

	count2 := list2.Count()
	if count2 != 14 {
		t.Errorf("Expected count 14, got %d", count2)
	}

	list2.Delete(10, false)
	count2 = list2.Count()
	if count2 != 13 {
		t.Errorf("Expected count 13, got %d", count2)
	}

	list2.Delete(10, true)
	count2 = list2.Count()
	if count2 != 0 {
		t.Errorf("Expected count 0, got %d", count2)
	}
}

func TestInsert(t *testing.T) {
	list := &LinkedList2{}

	node := &Node{value: 10}

	list.head = node
	list.tail = node

	count := list.Count()
	if count != 1 {
		t.Errorf("Expected list with 1 node, got %d", count)
	}

	list.Insert(node, Node{value: 20})
	count = list.Count()
	if count != 2 {
		t.Errorf("Expected list with 2 node, got %d", count)
	}
	if list.tail.value != 20 {
		t.Errorf("Expected tail with value 20, got smth else")
	}
	if list.head.value != 10 {
		t.Errorf("Expected list.head with value 20, got smth else")
	}
	if list.head.next.value != 20 {
		t.Errorf("Expected list.head.next next with value 20, got smth else")
	}
	if list.tail.prev.value != 10 {
		t.Errorf("Expected list.tail.prev with value 10, got smth else")
	}
	if node.next.value != 20 {
		t.Errorf("Expected node next with value 20, got smth else")
	}

	list.Insert(list.head, Node{value: 30})
	count = list.Count()
	if count != 3 {
		t.Errorf("Expected list with 3 node, got %d", count)
	}
	if list.tail.value != 20 {
		t.Errorf("Expected tail with value 20, got smth else")
	}
	if list.head.value != 10 {
		t.Errorf("Expected list.head with value 10, got smth else")
	}
	if list.head.next.value != 30 {
		t.Errorf("Expected list.head.next next with value 30, got smth else")
	}

	list.Insert(list.tail, Node{value: 40})
	count = list.Count()
	if count != 4 {
		t.Errorf("Expected list with 4 node, got %d", count)
	}
	if list.tail.value != 40 {
		t.Errorf("Expected tail with value 20, got smth else")
	}
	if list.head.value != 10 {
		t.Errorf("Expected list.head with value 10, got smth else")
	}
	if list.head.next.value != 30 {
		t.Errorf("Expected list.head.next next with value 30, got smth else")
	}
	if list.head.next.next.value != 20 {
		t.Errorf("Expected list.head.next.next (ex. tail) next with value 20, got smth else")
	}
}

func TestInsertFirst(t *testing.T) {
	list := &LinkedList2{}

	count := list.Count()
	if count != 0 {
		t.Errorf("Expected list with 0 node, got %d", count)
	}

	list.InsertFirst(Node{value: 10})
	count = list.Count()
	if count != 1 {
		t.Errorf("Expected list with 1 node, got %d", count)
	}
	if list.tail.value != 10 {
		t.Errorf("Expected tail with value 10, got smth else")
	}
	if list.head.value != 10 {
		t.Errorf("Expected list.head with value 20, got smth else")
	}
	if list.head.next != nil {
		t.Errorf("Expected list.head.next with nil, got smth else")
	}
	if list.tail.prev != nil {
		t.Errorf("Expected list.head.next with nil, got smth else")
	}

	list.InsertFirst(Node{value: 20})
	count = list.Count()
	if count != 2 {
		t.Errorf("Expected list with 2 node, got %d", count)
	}
	if list.tail.value != 10 {
		t.Errorf("Expected tail with value 20, got smth else")
	}
	if list.head.value != 20 {
		t.Errorf("Expected list.head with value 20, got smth else")
	}
	if list.head.next.value != 10 {
		t.Errorf("Expected list.head.next next with value 20, got smth else")
	}
	if list.tail.prev.value != 20 {
		t.Errorf("Expected list.head.next next with value 20, got smth else")
	}

	list.InsertFirst(Node{value: 30})
	count = list.Count()
	if count != 3 {
		t.Errorf("Expected list with 3 node, got %d", count)
	}
	if list.tail.value != 10 {
		t.Errorf("Expected tail with value 20, got smth else")
	}
	if list.head.value != 30 {
		t.Errorf("Expected list.head with value 10, got smth else")
	}
	if list.head.next.value != 20 {
		t.Errorf("Expected list.head.next next with value 30, got smth else")
	}
}

func TestClean(t *testing.T) {
	list := &LinkedList2{}

	count := list.Count()
	if count != 0 {
		t.Errorf("Expected empty list, got non-empty")
	}

	list.Clean()
	count = list.Count()
	if count != 0 {
		t.Errorf("Expected empty list, got non-empty")
	}

	node := &Node{value: 10}
	list.head = node

	for i := 0; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node.next = newNode
		node = newNode
	}
	list.tail = node

	count = list.Count()
	if count != 14 {
		t.Errorf("Expected count 14, got %d", count)
	}
	if list.head == nil || list.tail == nil {
		t.Errorf("Expected NOT nil in had AND tail")
	}

	list.Clean()
	count = list.Count()
	if count != 0 {
		t.Errorf("Expected count 13, got %d", count)
	}
	if list.head != nil || list.tail != nil {
		t.Errorf("Expected nil in head AND tail")
	}
}

func TestReverseList(t *testing.T) {
	list1 := &LinkedList2{}
	node1 := &Node{value: 10}
	list1.head = node1

	for i := 2; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node1.next = newNode
		newNode.prev = node1
		node1 = newNode
	}
	list1.tail = node1

	count := list1.Count()
	if count != 12 {
		t.Errorf("Expected 12, got %d", count)
	}

	list1.Reverse()
	count = list1.Count()
	if count != 12 {
		t.Errorf("Expected 12, got %d", count)
	}

	m := list1.head
	checkedValue := 120
	for true {
		if m.value != checkedValue {
			t.Errorf("Expected %d in node, got %d", checkedValue, m.value)
		}
		m = m.next
		checkedValue -= 10
		if m == nil {
			break
		}
	}
}

func TestHasLoop(t *testing.T) {
	list := &LinkedList2{}
	node := &Node{value: 10}
	list.head = node

	for i := 2; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node.next = newNode
		newNode.prev = node
		node = newNode
	}
	list.tail = node

	if list.HasLoop() {
		t.Errorf("Expected list does not have a loop")
	}

	list2 := &LinkedList2{}
	node21 := &Node{value: 10}
	list2.head = node21

	node22 := &Node{value: 20}
	node23 := &Node{value: 30}
	node24 := &Node{value: 40}
	node25 := &Node{value: 50}

	list2.tail = node25

	node21.next = node22
	node22.next = node24 // loop
	node24.next = node25

	node25.prev = node24
	node24.prev = node23
	node23.prev = node22
	node22.prev = node21

	if !list2.HasLoop() {
		t.Errorf("Expected list does have a loop")
	}

	list3 := &LinkedList2{}
	node31 := &Node{value: 10}
	list3.head = node31

	node32 := &Node{value: 20}
	node33 := &Node{value: 30}
	node34 := &Node{value: 40}
	node35 := &Node{value: 50}

	list3.tail = node35

	node31.next = node32
	node32.next = node33
	node33.next = node34
	node34.next = node32 // loop

	node35.prev = node34
	node34.prev = node33
	node33.prev = node32
	node32.prev = node31

	if !list3.HasLoop() {
		t.Errorf("Expected list does have a loop")
	}

	list4 := &LinkedList2{}
	node41 := &Node{value: 10}
	list4.head = node41

	node42 := &Node{value: 20}
	node43 := &Node{value: 30}
	node44 := &Node{value: 40}
	node45 := &Node{value: 50}

	list4.tail = node45

	node41.next = node42
	node42.next = node43
	node43.next = node44
	node44.next = node45

	node45.prev = node43 // loop
	node44.prev = node43
	node43.prev = node42
	node42.prev = node41

	if !list4.HasLoop() {
		t.Errorf("Expected list does have a loop")
	}

	list5 := &LinkedList2{}
	node51 := &Node{value: 10}
	list5.head = node51

	node52 := &Node{value: 20}
	node53 := &Node{value: 30}
	node54 := &Node{value: 40}
	node55 := &Node{value: 50}

	list5.tail = node55

	node51.next = node52
	node52.next = node53
	node53.next = node54
	node54.next = node55

	node55.prev = node54
	node54.prev = node53
	node53.prev = node55 // loop
	node52.prev = node51

	if !list5.HasLoop() {
		t.Errorf("Expected list does have a loop")
	}
}

func TestSort(t *testing.T) {
	list := &LinkedList2{}
	node := &Node{value: 10}
	list.head = node

	for i := 2; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node.next = newNode
		newNode.prev = node
		node = newNode
	}
	list.tail = node

	list.Sort()
	for n := list.head; n != nil; n = n.next {
		if n.prev != nil && !(n.prev.value <= n.value) {
			t.Errorf("Prev = %d, node = %d", n.prev.value, n.value)
		}
		if n.next != nil && !(n.next.value >= n.value) {
			t.Errorf("Node = %d, next = %d", n.value, n.next.value)
		}
	}

	list2 := &LinkedList2{}
	node21 := &Node{value: 50}
	list2.head = node21

	node22 := &Node{value: 40}
	node23 := &Node{value: 30}
	node24 := &Node{value: 20}
	node25 := &Node{value: 10}

	list2.tail = node25

	node21.next = node22
	node22.next = node23
	node23.next = node24
	node24.next = node25

	node25.prev = node24
	node24.prev = node23
	node23.prev = node22
	node22.prev = node21

	list2.Sort()
	for n := list2.head; n != nil; n = n.next {
		if n.prev != nil && !(n.prev.value <= n.value) {
			t.Errorf("Prev = %d, node = %d", n.prev.value, n.value)
		}
		if n.next != nil && !(n.next.value >= n.value) {
			t.Errorf("Node = %d, next = %d", n.value, n.next.value)
		}
	}

	list3 := &LinkedList2{}
	node31 := &Node{value: 10}
	list3.head = node31

	node32 := &Node{value: 50}
	node33 := &Node{value: 30}
	node34 := &Node{value: 40}
	node35 := &Node{value: 20}

	list3.tail = node35

	node31.next = node32
	node32.next = node33
	node33.next = node34
	node34.next = node35

	node35.prev = node34
	node34.prev = node33
	node33.prev = node32
	node32.prev = node31

	list3.Sort()
	for n := list3.head; n != nil; n = n.next {
		if n.prev != nil && !(n.prev.value <= n.value) {
			t.Errorf("Prev = %d, node = %d", n.prev.value, n.value)
		}
		if n.next != nil && !(n.next.value >= n.value) {
			t.Errorf("Node = %d, next = %d", n.value, n.next.value)
		}
	}

	list4 := &LinkedList2{}
	node41 := &Node{value: 10}
	list4.head = node41

	node42 := &Node{value: 10}
	node43 := &Node{value: 10}
	node44 := &Node{value: 10}
	node45 := &Node{value: 10}

	list4.tail = node45

	node41.next = node42
	node42.next = node43
	node43.next = node44
	node44.next = node45

	node45.prev = node44
	node44.prev = node43
	node43.prev = node42
	node42.prev = node41

	list4.Sort()
	for n := list4.head; n != nil; n = n.next {
		if n.prev != nil && !(n.prev.value <= n.value) {
			t.Errorf("Prev = %d, node = %d", n.prev.value, n.value)
		}
		if n.next != nil && !(n.next.value >= n.value) {
			t.Errorf("Node = %d, next = %d", n.value, n.next.value)
		}
	}

	list5 := &LinkedList2{}
	list5.Sort()

	node51 := &Node{value: 10}
	list5.head = node51
	list5.tail = node51

	list5.Sort()
	for n := list5.head; n != nil; n = n.next {
		if n.prev != nil && !(n.prev.value <= n.value) {
			t.Errorf("Prev = %d, node = %d", n.prev.value, n.value)
		}
		if n.next != nil && !(n.next.value >= n.value) {
			t.Errorf("Node = %d, next = %d", n.value, n.next.value)
		}
		if n.value != 10 {
			t.Errorf("Wrong Node")
		}
	}
}

func TestMergeSort(t *testing.T) {
	list11 := &LinkedList2{}
	node := &Node{value: 10}
	list11.head = node

	for i := 2; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node.next = newNode
		newNode.prev = node
		node = newNode
	}
	list11.tail = node

	list12 := &LinkedList2{}
	node121 := &Node{value: 130}
	list12.head = node121

	for i := 12; i > 0; i-- {
		newNode := &Node{value: 10*i + 5}
		node121.next = newNode
		newNode.prev = node121
		node121 = newNode
	}
	list12.tail = node121

	l := MergeSort(list11, list12)
	refValues := []int{10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130}
	i := 0
	for n := l.head; n != nil; n = n.next {
		if n.value != refValues[i] {
			t.Errorf("Wrong order, node = %d, index %d", n.value, i)
		}
		i++
	}
}
