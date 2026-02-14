// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import "testing"

func TestQueue(t *testing.T) {
	q := &Queue[int]{}

	if q.Size() != 0 {
		t.Fatalf("Expected empty queue")
	}

	head, err := q.Dequeue()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if head != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	q.Enqueue(0)
	q.Enqueue(1)
	q.Enqueue(2)

	//
	if q.Size() != 3 {
		t.Fatalf("Expected queue with len 3")
	}
	if q.head.value != 0 {
		t.Fatalf("First elem in queue = 0")
	}
	if q.tail.value != 2 {
		t.Fatalf("Last elem in queue = 2")
	}

	//
	head, err = q.Dequeue()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 0 {
		t.Fatalf("Head elem in queue = 0")
	}

	if q.Size() != 2 {
		t.Fatalf("Expected queue with len 2")
	}
	if q.head.value != 1 {
		t.Fatalf("First elem in queue = 1")
	}
	if q.tail.value != 2 {
		t.Fatalf("Last elem in queue = 2")
	}

	//
	head, err = q.Dequeue()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 1 {
		t.Fatalf("Head elem in queue = 1")
	}

	if q.Size() != 1 {
		t.Fatalf("Expected queue with len 1")
	}
	if q.head.value != 2 {
		t.Fatalf("First elem in queue = 2")
	}
	if q.tail.value != 2 {
		t.Fatalf("Last elem in queue = 2")
	}

	//
	head, err = q.Dequeue()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 2 {
		t.Fatalf("Head elem in queue = 2")
	}
	if q.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}

	if q.head != nil {
		t.Fatalf("Empty queue")
	}
	if q.tail != nil {
		t.Fatalf("Empty queue")
	}
}

func TestQueueCircle(t *testing.T) {
	qc := &QueueC[int]{}
	qc.Init(6)

	if qc.Size() != 0 {
		t.Fatalf("Expected empty queue")
	}

	head, err := qc.Dequeue()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if head != 0 {
		t.Fatalf("Peek elem in empty queue = zero (0 for int)")
	}

	qc.Enqueue(10)
	qc.Enqueue(11)
	qc.Enqueue(12)

	//
	if qc.Size() != 3 {
		t.Fatalf("Expected queue with len 3")
	}
	if qc.head != 0 {
		t.Fatalf("First elem index in queue = 0")
	}
	if qc.tail != 2 {
		t.Fatalf("Last elem index in queue = 2")
	}
	if qc.queue[qc.head] != 10 {
		t.Fatalf("First elem index in queue = 10")
	}
	if qc.queue[qc.tail] != 12 {
		t.Fatalf("Last elem index in queue = 12")
	}

	//
	head, err = qc.Dequeue()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 10 {
		t.Fatalf("Head elem in queue = 10")
	}

	if qc.Size() != 2 {
		t.Fatalf("Expected queue with len 2")
	}
	if qc.head != 1 {
		t.Fatalf("First elem index in queue = 1")
	}
	if qc.tail != 2 {
		t.Fatalf("Last elem index in queue = 2")
	}

	//
	head, err = qc.Dequeue()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 11 {
		t.Fatalf("Head elem in queue = 11")
	}

	if qc.Size() != 1 {
		t.Fatalf("Expected queue with len 1")
	}
	if qc.head != 2 {
		t.Fatalf("First elem index in queue = 2")
	}
	if qc.tail != 2 {
		t.Fatalf("Last elem index in queue = 2")
	}

	//
	head, err = qc.Dequeue()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if head != 12 {
		t.Fatalf("Head elem in queue = 2")
	}
	if qc.Size() != 0 {
		t.Fatalf("Expected queue with len 0")
	}
}

func TestRotation(t *testing.T) {
	qc := &QueueC[int]{}
	qc.Init(10)
	qc.Enqueue(1)
	qc.Enqueue(2)
	qc.Enqueue(3)
	qc.Enqueue(4)
	qc.Enqueue(5)
	qc.Enqueue(6)
	qc.Enqueue(7)

	RotateQueue(qc, 5)
	if qc.Size() != 7 {
		t.Fatalf("Expected queue with len 7")
	}
	if qc.tail != 1 {
		t.Fatalf("Expected head index 1, got %d", qc.tail)
	}
	if qc.head != 5 {
		t.Fatalf("Expected head index 5, got %d", qc.head)
	}
	if qc.queue[qc.tail] != 5 {
		t.Fatalf("Expected head value 5, got %d", qc.queue[qc.tail])
	}
	if qc.queue[qc.head] != 6 {
		t.Fatalf("Expected tail value 6, got %d", qc.queue[qc.head])
	}
}
