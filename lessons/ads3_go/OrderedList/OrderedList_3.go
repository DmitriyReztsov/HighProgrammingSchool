// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import "testing"

func TestAddOLA(t *testing.T) {
	ol := OrderedList[int]{_ascending: true}

	if ol.Count() != 0 {
		t.Fatalf("0 elements")
	}

	ol.Add(1)

	if ol.Count() != 1 {
		t.Fatalf("1 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 1 {
		t.Fatalf("Tail 1")
	}

	ol.Add(5)
	if ol.Count() != 2 {
		t.Fatalf("2 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 5 {
		t.Fatalf("Tail 5")
	}
	if ol.tail.prev.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.head.next.value != 5 {
		t.Fatalf("Tail 5")
	}

	ol.Add(15)
	if ol.Count() != 3 {
		t.Fatalf("3 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 15 {
		t.Fatalf("Tail 15")
	}
	if ol.tail.prev.value != 5 {
		t.Fatalf("Pre-tail = 5")
	}
	if ol.head.next.value != 5 {
		t.Fatalf("Next-head 5")
	}

	ol.Add(10)
	if ol.Count() != 4 {
		t.Fatalf("4 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 15 {
		t.Fatalf("Tail 15")
	}
	if ol.tail.prev.value != 10 {
		t.Fatalf("Pre-tail = 10")
	}
	if ol.head.next.value != 5 {
		t.Fatalf("Next-head 5")
	}

	ol.Add(0)
	if ol.Count() != 5 {
		t.Fatalf("5 elements")
	}

	if ol.head.value != 0 {
		t.Fatalf("Head = 0")
	}
	if ol.tail.value != 15 {
		t.Fatalf("Tail 15")
	}
	if ol.tail.prev.value != 10 {
		t.Fatalf("Pre-tail = 10")
	}
	if ol.head.next.value != 1 {
		t.Fatalf("Next-head 1")
	}
}

func TestAddOLD(t *testing.T) {
	ol := OrderedList[int]{_ascending: false}

	if ol.Count() != 0 {
		t.Fatalf("0 elements")
	}

	ol.Add(1)

	if ol.Count() != 1 {
		t.Fatalf("1 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 1 {
		t.Fatalf("Tail 1")
	}

	ol.Add(5)
	if ol.Count() != 2 {
		t.Fatalf("2 elements")
	}

	if ol.head.value != 5 {
		t.Fatalf("Head = 5")
	}
	if ol.tail.value != 1 {
		t.Fatalf("Tail 1")
	}
	if ol.tail.prev.value != 5 {
		t.Fatalf("Head = 5")
	}
	if ol.head.next.value != 1 {
		t.Fatalf("Tail 1")
	}

	ol.Add(15)
	if ol.Count() != 3 {
		t.Fatalf("3 elements")
	}

	if ol.head.value != 15 {
		t.Fatalf("Head = 15")
	}
	if ol.tail.value != 1 {
		t.Fatalf("Tail 1")
	}
	if ol.tail.prev.value != 5 {
		t.Fatalf("Pre-tail = 5")
	}
	if ol.head.next.value != 5 {
		t.Fatalf("Next-head 5")
	}

	ol.Add(10)
	if ol.Count() != 4 {
		t.Fatalf("4 elements")
	}

	if ol.head.value != 15 {
		t.Fatalf("Head = 15")
	}
	if ol.tail.value != 1 {
		t.Fatalf("Tail 1")
	}
	if ol.tail.prev.value != 5 {
		t.Fatalf("Pre-tail = 5")
	}
	if ol.head.next.value != 10 {
		t.Fatalf("Next-head 10")
	}

	ol.Add(0)
	if ol.Count() != 5 {
		t.Fatalf("5 elements")
	}

	if ol.head.value != 15 {
		t.Fatalf("Head = 15")
	}
	if ol.tail.value != 0 {
		t.Fatalf("Tail 0")
	}
	if ol.tail.prev.value != 1 {
		t.Fatalf("Pre-tail = 1")
	}
	if ol.head.next.value != 10 {
		t.Fatalf("Next-head 10")
	}
}

func TestDeleteOLA(t *testing.T) {
	ol := OrderedList[int]{_ascending: true}

	ol.Add(1)
	ol.Add(1)
	ol.Add(1)
	ol.Add(5)
	ol.Add(10)
	ol.Add(10)
	ol.Add(10)
	ol.Add(10)
	ol.Add(15)
	ol.Add(15)
	ol.Add(19)

	if ol.Count() != 11 {
		t.Fatalf("11 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(5)
	if ol.Count() != 10 {
		t.Fatalf("10 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(5)
	if ol.Count() != 10 {
		t.Fatalf("10 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(1)
	if ol.Count() != 9 {
		t.Fatalf("9 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(1)
	if ol.Count() != 8 {
		t.Fatalf("8 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(10)
	if ol.Count() != 7 {
		t.Fatalf("7 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(15)
	if ol.Count() != 6 {
		t.Fatalf("6 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(19)
	if ol.Count() != 5 {
		t.Fatalf("5 elements")
	}

	if ol.head.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.tail.value != 15 {
		t.Fatalf("Tail 15")
	}

	ol.Delete(1)
	if ol.Count() != 4 {
		t.Fatalf("4 elements")
	}

	if ol.head.value != 10 {
		t.Fatalf("Head = 10")
	}
	if ol.tail.value != 15 {
		t.Fatalf("Tail 15")
	}

	ol.Delete(10)
	if ol.Count() != 3 {
		t.Fatalf("3 elements")
	}

	if ol.head.value != 10 {
		t.Fatalf("Head = 10")
	}
	if ol.tail.value != 15 {
		t.Fatalf("Tail 15")
	}

	ol.Delete(10)
	if ol.Count() != 2 {
		t.Fatalf("2 elements")
	}

	if ol.head.value != 10 {
		t.Fatalf("Head = 10")
	}
	if ol.tail.value != 15 {
		t.Fatalf("Tail 15")
	}

	ol.Delete(10)
	if ol.Count() != 1 {
		t.Fatalf("1 elements")
	}

	if ol.head.value != 15 {
		t.Fatalf("Head = 15")
	}
	if ol.tail.value != 15 {
		t.Fatalf("Tail 15")
	}

	ol.Delete(15)
	if ol.Count() != 0 {
		t.Fatalf("0 elements")
	}
}

func TestDeleteOLD(t *testing.T) {
	ol := OrderedList[int]{_ascending: false}

	ol.Add(1)
	ol.Add(5)
	ol.Add(10)
	ol.Add(15)
	ol.Add(15)
	ol.Add(19)

	if ol.Count() != 6 {
		t.Fatalf("6 elements")
	}

	if ol.tail.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.head.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(5)
	if ol.Count() != 5 {
		t.Fatalf("5 elements")
	}

	if ol.tail.value != 1 {
		t.Fatalf("Head = 1")
	}
	if ol.head.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(1)
	if ol.Count() != 4 {
		t.Fatalf("4 elements")
	}

	if ol.tail.value != 10 {
		t.Fatalf("Head = 1")
	}
	if ol.head.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(10)
	if ol.Count() != 3 {
		t.Fatalf("3 elements")
	}

	if ol.tail.value != 15 {
		t.Fatalf("Head = 15")
	}
	if ol.head.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(15)
	if ol.Count() != 2 {
		t.Fatalf("2 elements")
	}

	if ol.tail.value != 15 {
		t.Fatalf("Head = 15")
	}
	if ol.head.value != 19 {
		t.Fatalf("Tail 19")
	}

	ol.Delete(19)
	if ol.Count() != 1 {
		t.Fatalf("1 elements")
	}

	if ol.tail.value != 15 {
		t.Fatalf("Head = 15")
	}
	if ol.head.value != 15 {
		t.Fatalf("Tail 15")
	}

	ol.Delete(15)
	if ol.Count() != 0 {
		t.Fatalf("0 elements")
	}
}

func TestAddOLAS(t *testing.T) {
	ol, err := MakeOrderedList[string]("asc", StringComparator)

	if err != nil {
		t.Fatal("nil errors expected")
	}
	if ol.Count() != 0 {
		t.Fatalf("0 elements")
	}

	ol.Add("a")

	if ol.Count() != 1 {
		t.Fatalf("1 elements")
	}

	if ol.head.value != "a" {
		t.Fatalf("Head = a")
	}
	if ol.tail.value != "a" {
		t.Fatalf("Tail a")
	}

	ol.Add(" b ")
	if ol.Count() != 2 {
		t.Fatalf("2 elements")
	}

	if ol.head.value != "a" {
		t.Fatalf("Head = a")
	}
	if ol.tail.value != " b " {
		t.Fatalf("Tail b")
	}
	if ol.tail.prev.value != "a" {
		t.Fatalf("Head = a")
	}
	if ol.head.next.value != " b " {
		t.Fatalf("Tail b")
	}

	ol.Add("f")
	if ol.Count() != 3 {
		t.Fatalf("3 elements")
	}

	if ol.head.value != "a" {
		t.Fatalf("Head = a")
	}
	if ol.tail.value != "f" {
		t.Fatalf("Tail f")
	}
	if ol.tail.prev.value != " b " {
		t.Fatalf("Pre-tail = b")
	}
	if ol.head.next.value != " b " {
		t.Fatalf("Next-head b")
	}
}

func TestCleanDuplicates(t *testing.T) {
	ol, _ := MakeOrderedList("asc", IntComparator)

	ol.Add(1)
	ol.Add(5)
	ol.Add(2)
	ol.Add(3)
	ol.Add(5)
	ol.Add(4)
	ol.Add(1)
	ol.Add(2)
	ol.Add(10)
	ol.Add(7)
	ol.Add(12)
	ol.Add(5)

	if ol.Count() != 12 {
		t.Fatalf("12 elements")
	}

	ol.CleanDuplicates()
	if ol.Count() != 8 {
		t.Fatalf("8 elements")
	}
}

func TestMergeTwoEmptyLists(t *testing.T) {
	ol1, _ := MakeOrderedList[int]("asc", IntComparator)
	ol2, _ := MakeOrderedList[int]("asc", IntComparator)

	result, err := MergeOrderedLists(ol1, ol2)
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result.Count() != 0 {
		t.Fatalf("Expected 0 elements")
	}
}

func TestMergeOneEmptyList(t *testing.T) {
	ol1, _ := MakeOrderedList[int]("asc", IntComparator)
	ol2, _ := MakeOrderedList[int]("asc", IntComparator)

	ol2.Add(1)
	ol2.Add(5)
	ol2.Add(10)

	result, err := MergeOrderedLists(ol1, ol2)
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result.Count() != 3 {
		t.Fatalf("Expected 3 elements")
	}
	if result.head.value != 1 {
		t.Fatalf("Expected head 1")
	}
	if result.tail.value != 10 {
		t.Fatalf("Expected tail 10")
	}

	expected := []int{1, 5, 10}
	current := result.head
	for i, exp := range expected {
		if current.value != exp {
			t.Fatalf("At position %d: expected %d, got %d", i, exp, current.value)
		}
		current = current.next
	}
}

func TestMergeTwoNonEmptyLists(t *testing.T) {
	ol1, _ := MakeOrderedList[int]("asc", IntComparator)
	ol2, _ := MakeOrderedList[int]("asc", IntComparator)

	ol1.Add(1)
	ol1.Add(5)
	ol1.Add(10)

	ol2.Add(2)
	ol2.Add(6)
	ol2.Add(15)

	result, err := MergeOrderedLists(ol1, ol2)
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result.Count() != 6 {
		t.Fatalf("Expected 6 elements")
	}
	if result.head.value != 1 {
		t.Fatalf("Expected head 1")
	}
	if result.tail.value != 15 {
		t.Fatalf("Expected tail 15")
	}

	expected := []int{1, 2, 5, 6, 10, 15}
	current := result.head
	for i, exp := range expected {
		if current.value != exp {
			t.Fatalf("At position %d: expected %d, got %d", i, exp, current.value)
		}
		current = current.next
	}
}

func TestMergeOneListIsSubset(t *testing.T) {
	ol1, _ := MakeOrderedList[int]("asc", IntComparator)
	ol2, _ := MakeOrderedList[int]("asc", IntComparator)

	ol1.Add(1)
	ol1.Add(3)
	ol1.Add(5)
	ol1.Add(7)
	ol1.Add(9)

	ol2.Add(3)
	ol2.Add(5)
	ol2.Add(7)

	result, err := MergeOrderedLists(ol1, ol2)
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result.Count() != 8 {
		t.Fatalf("Expected 8 elements")
	}

	expected := []int{1, 3, 3, 5, 5, 7, 7, 9}
	current := result.head
	for i, exp := range expected {
		if current.value != exp {
			t.Fatalf("At position %d: expected %d, got %d", i, exp, current.value)
		}
		current = current.next
	}
}

func TestMergeIntersectingLists(t *testing.T) {
	ol1, _ := MakeOrderedList[int]("asc", IntComparator)
	ol2, _ := MakeOrderedList[int]("asc", IntComparator)

	ol1.Add(1)
	ol1.Add(3)
	ol1.Add(5)

	ol2.Add(2)
	ol2.Add(3)
	ol2.Add(4)
	ol2.Add(5)
	ol2.Add(6)

	result, err := MergeOrderedLists(ol1, ol2)
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result.Count() != 8 {
		t.Fatalf("Expected 8 elements")
	}

	expected := []int{1, 2, 3, 3, 4, 5, 5, 6}
	current := result.head
	for i, exp := range expected {
		if current.value != exp {
			t.Fatalf("At position %d: expected %d, got %d", i, exp, current.value)
		}
		current = current.next
	}
}

func TestHasSublist1(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	sublist, _ := MakeOrderedList[int]("asc", IntComparator)

	list.Add(1)
	list.Add(2)
	list.Add(2)
	list.Add(3)
	list.Add(4)
	list.Add(5)

	sublist.Add(2)
	sublist.Add(3)
	sublist.Add(4)

	if !list.HasSublist(sublist) {
		t.Fatalf("Expected true")
	}
}

func TestHasSublist2(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	sublist, _ := MakeOrderedList[int]("asc", IntComparator)

	list.Add(1)
	list.Add(2)
	list.Add(3)
	list.Add(3)
	list.Add(4)
	list.Add(5)

	sublist.Add(1)
	sublist.Add(2)
	sublist.Add(3)

	if !list.HasSublist(sublist) {
		t.Fatalf("Expected true")
	}
}

func TestHasSublist3(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	sublist, _ := MakeOrderedList[int]("asc", IntComparator)

	list.Add(1)
	list.Add(2)
	list.Add(3)
	list.Add(4)
	list.Add(5)
	list.Add(5)

	sublist.Add(3)
	sublist.Add(4)
	sublist.Add(5)
	sublist.Add(5)

	if !list.HasSublist(sublist) {
		t.Fatalf("Expected true")
	}
}

func TestHasSublist4(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	sublist, _ := MakeOrderedList[int]("asc", IntComparator)

	list.Add(1)
	list.Add(2)
	list.Add(3)
	list.Add(4)
	list.Add(5)

	sublist.Add(0)
	sublist.Add(1)
	sublist.Add(2)

	if list.HasSublist(sublist) {
		t.Fatalf("Expected false")
	}
}

func TestHasSublist5(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	sublist, _ := MakeOrderedList[int]("asc", IntComparator)

	list.Add(1)
	list.Add(2)
	list.Add(3)
	list.Add(4)
	list.Add(5)

	sublist.Add(4)
	sublist.Add(5)
	sublist.Add(6)

	if list.HasSublist(sublist) {
		t.Fatalf("Expected false")
	}
}

func TestMostFrequentElement1(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	list.Add(5)

	result, err := list.MostFrequentElement()
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result != 5 {
		t.Fatalf("Expected 5")
	}
}

func TestMostFrequentElement2(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	list.Add(1)
	list.Add(2)
	list.Add(3)
	list.Add(4)
	list.Add(5)

	result, err := list.MostFrequentElement()
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result != 1 {
		t.Fatalf("Expected 1 (first element)")
	}
}

func TestMostFrequentElement3(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	list.Add(1)
	list.Add(2)
	list.Add(2)
	list.Add(2)
	list.Add(3)
	list.Add(3)
	list.Add(4)

	result, err := list.MostFrequentElement()
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result != 2 {
		t.Fatalf("Expected 2 (3 times)")
	}
}

func TestMostFrequentElement4(t *testing.T) {
	list, _ := MakeOrderedList[int]("asc", IntComparator)
	list.Add(7)
	list.Add(7)
	list.Add(7)
	list.Add(7)

	result, err := list.MostFrequentElement()
	if err != nil {
		t.Fatalf("Expected nil error")
	}

	if result != 7 {
		t.Fatalf("Expected 7")
	}
}
