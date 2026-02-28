// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import "testing"

func TestDequeueRemoveFront(t *testing.T) {
	d := &Deque[int]{}

	if d.Size() != 0 {
		t.Fatalf("Expected empty queue")
	}

	head, err := d.RemoveFront()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if head != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	tail, err := d.RemoveTail()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if tail != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	d.AddFront(0)
	d.AddFront(1)
	d.AddFront(2)

	d.AddTail(10)
	d.AddTail(11)
	d.AddTail(12)

	//
	if d.Size() != 6 {
		t.Fatalf("Expected queue with len 6")
	}
	if d.head.value != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.tail.value != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 2 {
		t.Fatalf("Head elem in queue = 2")
	}

	if d.Size() != 5 {
		t.Fatalf("Expected queue with len 5")
	}
	if d.head.value != 1 {
		t.Fatalf("First elem in queue = 1")
	}
	if d.tail.value != 12 {
		t.Fatalf("Last elem in queue = 2")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 1 {
		t.Fatalf("Head elem in queue = 1")
	}

	if d.Size() != 4 {
		t.Fatalf("Expected queue with len 4")
	}
	if d.head.value != 0 {
		t.Fatalf("First elem in queue = 0")
	}
	if d.tail.value != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 0 {
		t.Fatalf("Head elem in queue = 0")
	}
	if d.Size() != 3 {
		t.Fatalf("Expected queue with len 3")
	}

	if d.head.value != 10 {
		t.Fatalf("First elem in queue = 10")
	}
	if d.tail.value != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 10 {
		t.Fatalf("Head elem in queue = 10")
	}
	if d.Size() != 2 {
		t.Fatalf("Expected queue with len 2")
	}

	if d.head.value != 11 {
		t.Fatalf("First elem in queue = 11")
	}
	if d.tail.value != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 11 {
		t.Fatalf("Head elem in queue = 11")
	}
	if d.Size() != 1 {
		t.Fatalf("Expected queue with len 1")
	}

	if d.head.value != 12 {
		t.Fatalf("First elem in queue = 12")
	}
	if d.tail.value != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 12 {
		t.Fatalf("Head elem in queue = 12")
	}
	if d.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}

	if d.head != nil {
		t.Fatalf("Empty dequeue")
	}
	if d.tail != nil {
		t.Fatalf("Empty dequeue")
	}

	//
	head, err = d.RemoveFront()
	if err == nil {
		t.Fatalf("Expected error - empty dequeue")
	}
	if head != d.zero {
		t.Fatalf("Empty value")
	}
	if d.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}

	if d.head != nil {
		t.Fatalf("Empty dequeue")
	}
	if d.tail != nil {
		t.Fatalf("Empty dequeue")
	}
}

func TestDequeueRemoveTail(t *testing.T) {
	d := &Deque[int]{}

	if d.Size() != 0 {
		t.Fatalf("Expected empty queue")
	}

	head, err := d.RemoveFront()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if head != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	tail, err := d.RemoveTail()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if tail != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	d.AddFront(0)
	d.AddFront(1)
	d.AddFront(2)

	d.AddTail(10)
	d.AddTail(11)
	d.AddTail(12)

	//
	if d.Size() != 6 {
		t.Fatalf("Expected queue with len 6")
	}
	if d.head.value != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.tail.value != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 12 {
		t.Fatalf("Tail elem in queue = 12")
	}

	if d.Size() != 5 {
		t.Fatalf("Expected queue with len 5")
	}
	if d.head.value != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.tail.value != 11 {
		t.Fatalf("Last elem in queue = 11")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 11 {
		t.Fatalf("Tail elem in queue = 1")
	}

	if d.Size() != 4 {
		t.Fatalf("Expected queue with len 4")
	}
	if d.head.value != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.tail.value != 10 {
		t.Fatalf("Last elem in queue = 10")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 10 {
		t.Fatalf("Tail elem in queue = 10")
	}
	if d.Size() != 3 {
		t.Fatalf("Expected queue with len 3")
	}

	if d.head.value != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.tail.value != 0 {
		t.Fatalf("Last elem in queue = 0")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 0 {
		t.Fatalf("Tail elem in queue = 0")
	}
	if d.Size() != 2 {
		t.Fatalf("Expected queue with len 2")
	}

	if d.head.value != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.tail.value != 1 {
		t.Fatalf("Last elem in queue = 1")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 1 {
		t.Fatalf("Tail elem in queue = 1")
	}
	if d.Size() != 1 {
		t.Fatalf("Expected queue with len 1")
	}

	if d.head.value != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.tail.value != 2 {
		t.Fatalf("Last elem in queue = 2")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 2 {
		t.Fatalf("Tail elem in queue = 2")
	}
	if d.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}

	if d.head != nil {
		t.Fatalf("Empty dequeue")
	}
	if d.tail != nil {
		t.Fatalf("Empty dequeue")
	}

	//
	tail, err = d.RemoveFront()
	if err == nil {
		t.Fatalf("Expected error - empty dequeue")
	}
	if tail != d.zero {
		t.Fatalf("Empty value")
	}
	if d.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}

	if d.head != nil {
		t.Fatalf("Empty dequeue")
	}
	if d.tail != nil {
		t.Fatalf("Empty dequeue")
	}
}

func TestPalindrome(t *testing.T) {
	if IsPalindrome("asd") != false {
		t.Fatalf("asd = not palindrome")
	}

	if IsPalindrome("") != true {
		t.Fatalf("empty string = palindrome")
	}

	if IsPalindrome("a") != true {
		t.Fatalf("a = palindrome")
	}

	if IsPalindrome("asddsa") != true {
		t.Fatalf("asddsa = palindrome")
	}

	if IsPalindrome("asdsa") != true {
		t.Fatalf("asdsa = palindrome")
	}

	if IsPalindrome("asd dsa") != true {
		t.Fatalf("asd dsa = palindrome")
	}
}

func TestDequeueWithMin(t *testing.T) {
	d := NewDequeWithMin()

	d.AddFront(7)
	d.AddFront(3)
	d.AddFront(2)

	d.AddTail(10)
	d.AddTail(1)
	d.AddTail(5)

	m, err := d.GetMin()
	if err != nil {
		t.Fatal("Error should be nil")
	}
	if m != 1 {
		t.Fatalf("Min = 1")
	}

	d.RemoveTail()
	m, err = d.GetMin()
	if err != nil {
		t.Fatal("Error should be nil")
	}
	if m != 1 {
		t.Fatalf("Min = 1")
	}

	d.RemoveFront()
	m, err = d.GetMin()
	if err != nil {
		t.Fatal("Error should be nil")
	}
	if m != 1 {
		t.Fatalf("Min = 1")
	}

	d.RemoveTail()
	m, err = d.GetMin()
	if err != nil {
		t.Fatal("Error should be nil")
	}
	if m != 3 {
		t.Fatalf("Min = 3")
	}

	d.RemoveTail()
	m, err = d.GetMin()
	if err != nil {
		t.Fatal("Error should be nil")
	}
	if m != 3 {
		t.Fatalf("Min = 3")
	}

	d.RemoveFront()
	m, err = d.GetMin()
	if err != nil {
		t.Fatal("Error should be nil")
	}
	if m != 7 {
		t.Fatalf("Min = 7")
	}

	d.RemoveFront()
	_, err = d.GetMin()
	if err == nil {
		t.Fatal("Error should NOT be nil")
	}
}

func TestDequeueDRemoveFront(t *testing.T) {
	d := NewDequeD[int](16)

	if d.Size() != 0 {
		t.Fatalf("Expected empty queue")
	}

	head, err := d.RemoveFront()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if head != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	tail, err := d.RemoveTail()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if tail != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	d.AddFront(0)
	d.AddFront(1)
	d.AddFront(2)

	d.AddTail(10)
	d.AddTail(11)
	d.AddTail(12)

	//
	if d.Size() != 6 {
		t.Fatalf("Expected queue with len 6")
	}
	if d.deque[d.head] != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.deque[d.tail-1] != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 2 {
		t.Fatalf("Head elem in queue = 2")
	}

	if d.Size() != 5 {
		t.Fatalf("Expected queue with len 5")
	}
	if d.deque[d.head] != 1 {
		t.Fatalf("First elem in queue = 1")
	}
	if d.deque[d.tail-1] != 12 {
		t.Fatalf("Last elem in queue = 2")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 1 {
		t.Fatalf("Head elem in queue = 1")
	}

	if d.Size() != 4 {
		t.Fatalf("Expected queue with len 4")
	}
	if d.deque[d.head] != 0 {
		t.Fatalf("First elem in queue = 0")
	}
	if d.deque[d.tail-1] != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 0 {
		t.Fatalf("Head elem in queue = 0")
	}
	if d.Size() != 3 {
		t.Fatalf("Expected queue with len 3")
	}

	if d.deque[d.head] != 10 {
		t.Fatalf("First elem in queue = 10")
	}
	if d.deque[d.tail-1] != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 10 {
		t.Fatalf("Head elem in queue = 10")
	}
	if d.Size() != 2 {
		t.Fatalf("Expected queue with len 2")
	}

	if d.deque[d.head] != 11 {
		t.Fatalf("First elem in queue = 11")
	}
	if d.deque[d.tail-1] != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 11 {
		t.Fatalf("Head elem in queue = 11")
	}
	if d.Size() != 1 {
		t.Fatalf("Expected queue with len 1")
	}

	if d.deque[d.head] != 12 {
		t.Fatalf("First elem in queue = 12")
	}
	if d.deque[d.tail-1] != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	head, err = d.RemoveFront()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 12 {
		t.Fatalf("Head elem in queue = 12")
	}
	if d.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}

	if d.head != d.tail {
		t.Fatalf("Empty dequeue")
	}

	//
	head, err = d.RemoveFront()
	if err == nil {
		t.Fatalf("Expected error - empty dequeue")
	}
	if head != d.zero {
		t.Fatalf("Empty value")
	}
	if d.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}
}

func TestDequeueDRemoveTail(t *testing.T) {
	d := NewDequeD[int](16)

	if d.Size() != 0 {
		t.Fatalf("Expected empty queue")
	}

	head, err := d.RemoveFront()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if head != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	tail, err := d.RemoveTail()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if tail != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	d.AddFront(0)
	d.AddFront(1)
	d.AddFront(2)

	d.AddTail(10)
	d.AddTail(11)
	d.AddTail(12)

	//
	if d.Size() != 6 {
		t.Fatalf("Expected queue with len 6")
	}
	if d.deque[d.head] != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.deque[d.tail-1] != 12 {
		t.Fatalf("Last elem in queue = 12")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 12 {
		t.Fatalf("Tail elem in queue = 12")
	}

	if d.Size() != 5 {
		t.Fatalf("Expected queue with len 5")
	}
	if d.deque[d.head] != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.deque[d.tail-1] != 11 {
		t.Fatalf("Last elem in queue = 11")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 11 {
		t.Fatalf("Tail elem in queue = 1")
	}

	if d.Size() != 4 {
		t.Fatalf("Expected queue with len 4")
	}
	if d.deque[d.head] != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.deque[d.tail-1] != 10 {
		t.Fatalf("Last elem in queue = 10")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 10 {
		t.Fatalf("Tail elem in queue = 10")
	}
	if d.Size() != 3 {
		t.Fatalf("Expected queue with len 3")
	}

	if d.deque[d.head] != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.deque[(d.tail-1+d.capacity)%d.capacity] != 0 {
		t.Fatalf("Last elem in queue = 0")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 0 {
		t.Fatalf("Tail elem in queue = 0")
	}
	if d.Size() != 2 {
		t.Fatalf("Expected queue with len 2")
	}

	if d.deque[d.head] != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.deque[(d.tail-1+d.capacity)%d.capacity] != 1 {
		t.Fatalf("Last elem in queue = 1")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 1 {
		t.Fatalf("Tail elem in queue = 1")
	}
	if d.Size() != 1 {
		t.Fatalf("Expected queue with len 1")
	}

	if d.deque[d.head] != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if d.deque[(d.tail-1+d.capacity)%d.capacity] != 2 {
		t.Fatalf("Last elem in queue = 2")
	}

	//
	tail, err = d.RemoveTail()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if tail != 2 {
		t.Fatalf("Tail elem in queue = 2")
	}
	if d.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}

	if d.head != d.tail {
		t.Fatalf("Empty dequeue")
	}

	//
	head, err = d.RemoveFront()
	if err == nil {
		t.Fatalf("Expected error - empty dequeue")
	}
	if head != d.zero {
		t.Fatalf("Empty value")
	}
	if d.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}
}
