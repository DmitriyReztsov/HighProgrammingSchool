// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import "testing"

func TestAddInTail(t *testing.T) {
	list := &LinkedList{}
	node1 := Node{value: 10}
	node2 := Node{value: 20}

	list.AddInTail(node1)
	list.AddInTail(node2)

	if list.head.value != 10 {
		t.Fatalf("Expected head value 10, got %d", list.head.value)
	}

	if list.tail.value != 20 {
		t.Fatalf("Expected tail value 20, got %d", list.tail.value)
	}
}

func TestCount(t *testing.T) {
	list := &LinkedList{}
	count := list.Count()

	if count != 0 {
		t.Errorf("Expected count 0, got %d", count)
	}

	node1 := Node{value: 10}
	node2 := Node{value: 20}
	node1.next = &node2

	list.head = &node1
	list.tail = &node2

	count = list.Count()

	if count != 2 {
		t.Errorf("Expected count 2, got %d", count)
	}
}

func TestFind(t *testing.T) {
	list := &LinkedList{}
	_, err := list.Find(1)

	if err == nil {
		t.Errorf("Expected error on find in empty list, got nil")
	}

	node := &Node{value: 10}

	list.head = node
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

	for i := 0; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node.next = newNode
		node = newNode
	}
	list.tail = node

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
}

func TestFindAll(t *testing.T) {
	list := &LinkedList{}
	nodeCopySlice := list.FindAll(1)

	if len(nodeCopySlice) > 0 {
		t.Errorf("Expected empty list, got non-empty")
	}

	node := &Node{value: 10}

	list.head = node
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
		node = newNode
	}
	list.tail = node

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
	list2 := &LinkedList{}
	node2 := &Node{value: 10}
	list2.head = node2

	for i := 0; i <= 12; i++ {
		newNode2 := &Node{value: 10}
		node2.next = newNode2
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
}

func TestDelete(t *testing.T) {
	list := &LinkedList{}

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
		t.Errorf("Expected list with 0 node, got smth else")
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
		node = newNode
	}
	list.tail = node

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

	// list2 with the same nodes like 10 10 10 10 10 ... 10
	list2 := &LinkedList{}
	node2 := &Node{value: 10}
	list2.head = node2

	for i := 0; i <= 12; i++ {
		newNode2 := &Node{value: 10}
		node2.next = newNode2
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
	list := &LinkedList{}

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
	list := &LinkedList{}

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
	list := &LinkedList{}

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
		t.Errorf("Expected nil in had AND tail")
	}
}

func TestMergeLists(t *testing.T) {
	list1 := &LinkedList{}
	node1 := &Node{value: 10}
	list1.head = node1

	for i := 2; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node1.next = newNode
		node1 = newNode
	}
	list1.tail = node1

	count := list1.Count()
	if count != 12 {
		t.Errorf("Expected 12 nodes1, got %d", count)
	}

	list2 := &LinkedList{}
	node2 := &Node{value: 10}
	list2.head = node2

	for i := 2; i <= 12; i++ {
		newNode := &Node{value: 10 * i}
		node2.next = newNode
		node2 = newNode
	}
	list2.tail = node2

	count = list2.Count()
	if count != 12 {
		t.Errorf("Expected 12 nodes2, got %d", count)
	}

	mergedList := MergeLists(list1, list2)
	count = mergedList.Count()
	if count != 12 {
		t.Errorf("Expected 12 nodes2, got %d", count)
	}

	n1 := list1.head
	n2 := list2.head
	m := mergedList.head
	for true {
		if m.value != n1.value + n2.value {
			t.Errorf("Expected %d + %d, got %d", n1.value, n2.value, m.value)
		}
		n1 = n1.next
		n2 = n2.next
		m = m.next
		if n1 == nil {
			break
		}
	}

	mergedList = MergeLists(list1, &LinkedList{})
	if mergedList.head != nil && mergedList.tail != nil {
		t.Errorf("Expected empty list")
	}

	mergedList = MergeLists(&LinkedList{}, &LinkedList{})
	if mergedList.head != nil && mergedList.tail != nil {
		t.Errorf("Expected empty list")
	}
}