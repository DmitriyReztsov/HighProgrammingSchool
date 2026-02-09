// 4

package main

import (
	"strconv"
	"strings"
	"os"
	"errors"
)

// 4.4 Скобочная последовательность
// по времени сложность - O(n) на перебор элементов строки, операции стека - O(1), по памяти О(1)
func bracketsCons(brackets string) bool {
	brStack := Stack[rune]{}

	for _, br := range brackets {
		if br == '(' {
			brStack.Push(br)
		}
		if br == ')' {
			_, err := brStack.Pop()
			if err != nil {
				return false
			}
		}
	}
	if brStack.Size() == 0 {
		return true
	}
	return false
}

// 4.5 Расширенная скобочная последовательность
// по времени сложность - O(n) на перебор элементов строки, операции стека - O(1), по памяти О(1)
func bracketsConsExt(brackets string) bool {
	brStack := Stack[rune]{}

	mapBrackets := map[rune]rune{
		')': '(',
		']': '[',
		'}': '{',
	}

	for _, br := range brackets {
		openBr, closing := mapBrackets[br]
		if !closing {
			brStack.Push(br)
		} else {
			topBr_, err := brStack.Pop()
			if err != nil {
				return false
			}
			if topBr_ != openBr {
				return false
			}
		}
	}
	if brStack.Size() == 0 {
		return true
	}
	return false
}

// 4.6 Минимальный элемент в стеке
// Заведем второй стек. Дальше два варианта: либо на каждый пуш и поп делать такой же пуш и поп в стек с минимальным
// значением, добавляя текущий минимум. Выглядит как более чистый код, но потребует второго по размерам массива.
// Второй вариант - складывать в стек с минимальными значениями только минимум, при поп из основного стека сравнивать
// с минимумом и делать в минимуме поп только если удаляем текущий минимум. По памяти будет лучше, читаемость будет
// немного страдать
// Сложность такая же как и у основного стека O(1), по памяти +O(n) на второй стек
type StackWithMin[T int] struct {
	stack    *Stack[T]
	stackMin *Stack[T]
}

func NewStackWithMin[T int]() *StackWithMin[T] {
	return &StackWithMin[T]{
		stack:    &Stack[T]{},
		stackMin: &Stack[T]{},
	}
}

func (st *StackWithMin[T]) Size() int {
	return st.stack.Size()
}

func (st *StackWithMin[T]) Peek() (T, error) {
	return st.stack.Peek()
}

func (st *StackWithMin[T]) Pop() (T, error) {
	st.stackMin.Pop()
	return st.stack.Pop()
}

func (st *StackWithMin[T]) Push(itm T) {
	st.stack.Push(itm)

	minValue, err := st.stackMin.Peek()

	if err != nil || minValue > itm {
		st.stackMin.Push(itm)
	} else {
		st.stackMin.Push(minValue)
	}
}

func (st *StackWithMin[T]) Minimum() (T, error) {
	return st.stackMin.Peek()
}

// 4.7 Среднее значение элементов в стеке
// по сложности - так же, +О(n) на третий стек
type StackWithAvg[T int] struct {
	StackWithMin[T]
	stackSum *Stack[T]
}

func NewStackWithAvg[T int]() *StackWithAvg[T] {
	return &StackWithAvg[T]{
		StackWithMin: StackWithMin[T]{
			stack:    &Stack[T]{},
			stackMin: &Stack[T]{},
		},
		stackSum: &Stack[T]{},
	}
}

func (st *StackWithAvg[T]) Pop() (T, error) {
	st.stackSum.Pop()
	return st.StackWithMin.Pop()
}

func (st *StackWithAvg[T]) Push(itm T) {
	st.StackWithMin.Push(itm)

	sumValue, err := st.stackSum.Peek()
	if err != nil {
		st.stackSum.Push(itm)
	} else {
		st.stackSum.Push(sumValue + itm)
	}
}

func (st *StackWithAvg[T]) Average() (float64, error) {
	sumValue, err := st.stackSum.Peek()
	if err != nil {
		return float64(sumValue), err
	}
	return float64(sumValue / T(st.stackSum.Size())), nil
}

// 4.8. постфиксная запись
// время - О(n) на перебор стеков, память - О(n) на стеки
func calculatePostfix(postfix string) int {
	// make Stack1
	s1 := &StackR[string]{}
	for _, elem := range strings.Fields(postfix) {
		s1.Push(elem)
	}

	s2 := &Stack[int]{}
	for el, er := s1.Pop(); er == nil; el, er = s1.Pop() {
		num, err := strconv.Atoi(el)
		if err == nil {
			s2.Push(num)
		} else {
			scndArg, _ := s2.Pop()
			fstArg, _ := s2.Pop()
			switch el {
			case "*":
				s2.Push(fstArg * scndArg)
			case "+":
				s2.Push(fstArg + scndArg)
			case "-":
				s2.Push(fstArg - scndArg)
			case "/":
				s2.Push(fstArg / scndArg)
			case "=":
				return scndArg
			}
		}
	}
	return 0 // без знака = возврат ошибки
}

// Рефлексия по задачам задания 2
// 2.9. Переворачивание списка. Пробежался по спику и поменял направления каждого узла. Голову и хвост поменял местами

// 2.10. Проверка на циклы. Я перемудрил, искал циклы через учет посещенных элементов. Единственное, что я бы добавил
// для двунаправленного списка - пробегаться по списку и считать узлы в обе стороны.const

// 2.11. Сортировка. Абсолютно согласен, что пузырек тут наиболее очевидный метод. Я выпендрился через сортировку
// слиянием. В свою защиту могу только отметить более эффективную сложность по времени, но менее эффективных сложность
// по памяти.const

// 2.12. Слияние сортированных списков. Я не догадался обобщить на произвольное количество списков (список списков), но
// тут мне очень пригодились методы слияния из сортировки слиянием и в целом работа со списком списков в моем случае не
// сильно усложнит код. Главная сложность тут, конечно, даст сортировка. Сортировка слиянием - более эффективная по
// времени и переиспользьзуема для слияния отсортированых списков.

// 2.13. Dummy. Я тут совершил все ошибки, которые вы описали :) Вкорячил флаг в основной тип Node. В оправдание могу
// только написать, что проверку типа в Го я до текущей секунды не умел делать. Но и мысли не пришло поискать аналог
// isinstance(). Про круговой список - интересная идея.
