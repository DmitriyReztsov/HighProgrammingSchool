// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import "testing"

func TestPush(t *testing.T) {
	st := &Stack[int]{}

	if st.Size() != 0 {
		t.Fatalf("Expected empty stack")
	}

	st.Push(0)
	if st.Size() != 1 {
		t.Fatalf("Expected stack with len 1")
	}
	if st.stack[0] != 0 {
		t.Fatalf("First elem in stack = 0")
	}

	st.Push(1)
	if st.Size() != 2 {
		t.Fatalf("Expected stack with len 2")
	}
	if st.stack[0] != 0 {
		t.Fatalf("First elem in stack = 0")
	}
	if st.stack[st.Size()-1] != 1 {
		t.Fatalf("Last elem in stack = 1")
	}

	st.Push(2)
	if st.Size() != 3 {
		t.Fatalf("Expected stack with len 3")
	}
	if st.stack[0] != 0 {
		t.Fatalf("First elem in stack = 0")
	}
	if st.stack[st.Size()-1] != 2 {
		t.Fatalf("Last elem in stack = 2")
	}
}

func TestPeek(t *testing.T) {
	st := &Stack[int]{}

	if st.Size() != 0 {
		t.Fatalf("Expected empty stack")
	}
	peek, err := st.Peek()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if peek != 0 {
		t.Fatalf("Peek elem in empty stack = zero (0 for int)")
	}

	st.Push(0)
	st.Push(1)
	st.Push(2)
	if st.Size() != 3 {
		t.Fatalf("Expected stack with len 3")
	}
	if st.stack[0] != 0 {
		t.Fatalf("First elem in stack = 0")
	}
	if st.stack[st.Size()-1] != 2 {
		t.Fatalf("Last elem in stack = 2")
	}

	peek, err = st.Peek()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if peek != 2 {
		t.Fatalf("Peek elem in stack = 2")
	}
}

func TestPop(t *testing.T) {
	st := &Stack[string]{}

	if st.Size() != 0 {
		t.Fatalf("Expected empty stack")
	}
	pop, err := st.Pop()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if pop != "" {
		t.Fatalf("Pop elem in empty stack = zero (empty string for int)")
	}

	st.Push("0")
	st.Push("1")
	st.Push("2")
	if st.Size() != 3 {
		t.Fatalf("Expected stack with len 3")
	}
	if st.stack[0] != "0" {
		t.Fatalf("First elem in stack = '0")
	}
	if st.stack[st.Size()-1] != "2" {
		t.Fatalf("Last elem in stack = '2'")
	}

	pop, err = st.Pop()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if pop != "2" {
		t.Fatalf("Peek elem in stack = '2'")
	}

	if st.Size() != 2 {
		t.Fatalf("Expected stack with len 2")
	}
	if st.stack[0] != "0" {
		t.Fatalf("First elem in stack = '0")
	}
	if st.stack[st.Size()-1] != "1" {
		t.Fatalf("Last elem in stack after pop = '1'")
	}
}

func TestPushR(t *testing.T) {
	st := &StackR[int]{}

	if st.Size() != 0 {
		t.Fatalf("Expected empty stack")
	}

	st.Push(0)
	if st.Size() != 1 {
		t.Fatalf("Expected stack with len 1")
	}
	if st.tail.value != 0 {
		t.Fatalf("First elem in stack = 0")
	}

	st.Push(1)
	if st.Size() != 2 {
		t.Fatalf("Expected stack with len 2")
	}
	if st.head.value != 0 {
		t.Fatalf("First elem in stack = 0")
	}
	if st.tail.value != 1 {
		t.Fatalf("Last elem in stack = 1")
	}

	st.Push(2)
	if st.Size() != 3 {
		t.Fatalf("Expected stack with len 3")
	}
	if st.head.value != 0 {
		t.Fatalf("First elem in stack = 0")
	}
	if st.tail.value != 2 {
		t.Fatalf("Last elem in stack = 2")
	}
}

func TestPeekR(t *testing.T) {
	st := &StackR[int]{}

	if st.Size() != 0 {
		t.Fatalf("Expected empty stack")
	}
	peek, err := st.Peek()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if peek != 0 {
		t.Fatalf("Peek elem in empty stack = zero (0 for int)")
	}

	st.Push(0)
	st.Push(1)
	st.Push(2)
	if st.Size() != 3 {
		t.Fatalf("Expected stack with len 3")
	}
	if st.head.value != 0 {
		t.Fatalf("First elem in stack = 0")
	}
	if st.tail.value != 2 {
		t.Fatalf("Last elem in stack = 2")
	}

	peek, err = st.Peek()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if peek != 0 {
		t.Fatalf("Peek elem in stack = 0")
	}
}

func TestPopR(t *testing.T) {
	st := &StackR[string]{}

	if st.Size() != 0 {
		t.Fatalf("Expected empty stack")
	}
	pop, err := st.Pop()
	if err == nil {
		t.Fatalf("Expected not nil error")
	}
	if pop != "" {
		t.Fatalf("Pop elem in empty stack = zero (empty string for int)")
	}

	st.Push("0")
	st.Push("1")
	st.Push("2")
	if st.Size() != 3 {
		t.Fatalf("Expected stack with len 3")
	}
	if st.head.value != "0" {
		t.Fatalf("First elem in stack = '0")
	}
	if st.tail.value != "2" {
		t.Fatalf("Last elem in stack = '2'")
	}

	pop, err = st.Pop()
	if err != nil {
		t.Fatalf("Expected nil error")
	}
	if pop != "0" {
		t.Fatalf("Peek elem in stack = '0'")
	}

	if st.Size() != 2 {
		t.Fatalf("Expected stack with len 2")
	}
	if st.head.value != "1" {
		t.Fatalf("First elem in stack = '0")
	}
	if st.tail.value != "2" {
		t.Fatalf("Last elem in stack after pop = '2'")
	}
}

func TestBrackets(t *testing.T) {
	bracketsLine := "()"

	if bracketsCons(bracketsLine) != true {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = ")("

	if bracketsCons(bracketsLine) != false {
		t.Fatalf("Expected false bracket consequence")
	}

	bracketsLine = "("

	if bracketsCons(bracketsLine) != false {
		t.Fatalf("Expected false bracket consequence")
	}

	bracketsLine = ")"

	if bracketsCons(bracketsLine) != false {
		t.Fatalf("Expected false bracket consequence")
	}

	bracketsLine = ""

	if bracketsCons(bracketsLine) != true {
		t.Fatalf("Expected false bracket consequence")
	}

	//
	bracketsLine = "())())"

	if bracketsCons(bracketsLine) != false {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = "(()((())()))"

	if bracketsCons(bracketsLine) != true {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = "(()()(()"

	if bracketsCons(bracketsLine) != false {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = "((())()()(()(())))()(()((())))()(()())()()(((())))(()()())()(()(()))(())()(())()()(()())()()(()())()"

	if bracketsCons(bracketsLine) != true {
		t.Fatalf("Expected true bracket consequence")
	}
}

func TestBracketsExt(t *testing.T) {
	bracketsLine := "{}"

	if bracketsConsExt(bracketsLine) != true {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = ")("

	if bracketsConsExt(bracketsLine) != false {
		t.Fatalf("Expected false bracket consequence")
	}

	bracketsLine = "["

	if bracketsConsExt(bracketsLine) != false {
		t.Fatalf("Expected false bracket consequence")
	}

	bracketsLine = "]"

	if bracketsConsExt(bracketsLine) != false {
		t.Fatalf("Expected false bracket consequence")
	}

	bracketsLine = ""

	if bracketsConsExt(bracketsLine) != true {
		t.Fatalf("Expected false bracket consequence")
	}

	//
	bracketsLine = "(}"

	if bracketsConsExt(bracketsLine) != false {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = "(({})[{()}()])"

	if bracketsConsExt(bracketsLine) != true {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = "((){})[()"

	if bracketsConsExt(bracketsLine) != false {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = "()(){}[](){}[](){}[]({[(){}[]()]})(){}[]()[]{}{()}[[]]{}()()({})([{}])[]((){})[](){{}}[[()]]{}[](){}[({})](){}[]()[]{}(){[()]}()[]{}()[]{}()"

	if bracketsConsExt(bracketsLine) != true {
		t.Fatalf("Expected true bracket consequence")
	}

	bracketsLine = "()(}{)[](){}[](){}[]({[(){}[]())]})(){}[()[]{}{()}[[]]{}()(}({)}([{}])[]((){})[](){{}}[[())]}{}[](){}[({})](){)[}[]()[]{}(){[()]](}[]{}()[]{}()(((())))}}{{{[[[]]]]([)]{}}{)([]{}[)(){}()(){}[](){}[](}{]()"

	if bracketsConsExt(bracketsLine) != false {
		t.Fatalf("Expected true bracket consequence")
	}
}

func TestMin(t *testing.T) {
	st := NewStackWithMin()

	if st.Size() != 0 {
		t.Fatalf("Expected empty stack")
	}

	st.Push(10)
	st.Push(5)
	st.Push(7)
	if st.Size() != 3 {
		t.Fatalf("Expected stack with len 3")
	}

	minimum, _ := st.Minimum()
	if minimum != 5 {
		t.Fatalf("Minimum expected = 5")
	}

	st.Push(17)
	st.Push(2)
	st.Push(23)
	minimum, _ = st.Minimum()
	if minimum != 2 {
		t.Fatalf("Minimum expected = 2")
	}

	st.Push(0)
	minimum, _ = st.Minimum()
	if minimum != 0 {
		t.Fatalf("Minimum expected = 0")
	}

	st.Pop()
	minimum, _ = st.Minimum()
	if minimum != 2 {
		t.Fatalf("Minimum expected = 2")
	}

	st.Pop()
	st.Pop()
	minimum, _ = st.Minimum()
	if minimum != 5 {
		t.Fatalf("Minimum expected = 5")
	}

	st.Pop()
	st.Pop()
	st.Pop()
	minimum, _ = st.Minimum()
	if minimum != 10 {
		t.Fatalf("Minimum expected = 5")
	}

	st.Pop()
	_, err := st.Minimum()
	if err == nil {
		t.Fatalf("Err expected")
	}
}

func TestAvg(t *testing.T) {
	st := NewStackWithAvg()

	if st.Size() != 0 {
		t.Fatalf("Expected empty stack")
	}

	st.Push(10)
	st.Push(6)
	st.Push(5)
	if st.Size() != 3 {
		t.Fatalf("Expected stack with len 3")
	}

	avg, _ := st.Average()
	if avg != 7.0 {
		t.Fatalf("Minimum expected = 7")
	}

	st.Pop()
	avg, _ = st.Average()
	if avg != 8.0 {
		t.Fatalf("Minimum expected = 8")
	}
}

func TestPostfix(t *testing.T) {
	res := calculatePostfix("8 2 + 5 * 9 + =")

	if res != 59 {
		t.Fatalf("Expected 59, got %d", res)
	}
}
