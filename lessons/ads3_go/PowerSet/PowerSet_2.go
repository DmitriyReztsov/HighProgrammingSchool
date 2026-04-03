// 10
package main

import (
	"constraints"
)

// 10.4 декартово произведение множеств
// элемент Декартова произведения с двумя элементами. Элементы должны быть типа comparable для возможности сравнения
type CartesianElement[T comparable] struct {
	first  T
	second T
}

func NewCartesianElement[T comparable](first, second T) CartesianElement[T] {
	return CartesianElement[T]{first: first, second: second}
}

// также нам нужна новая структура множества с типом comparable вместо Ordered, тем более,
// что множество не должно гарантировать упорядоченность
type CartesianPowerSet[T comparable] struct {
	setSlots map[CartesianElement[T]]struct{}
	size     int
}

// создание экземпляра множества
func CartesianInit[T comparable]() CartesianPowerSet[T] {
	return CartesianPowerSet[T]{setSlots: make(map[CartesianElement[T]]struct{}), size: 0}
}

func (cp *CartesianPowerSet[T]) Size() int {
	return cp.size
}

func (p *CartesianPowerSet[T]) Put(value CartesianElement[T]) {
	if _, exists := p.setSlots[value]; !exists {
		p.setSlots[value] = struct{}{}
		p.size++
	}
}

func (cp *CartesianPowerSet[T]) Get(value CartesianElement[T]) bool {
	_, exists := cp.setSlots[value]
	return exists
}

// функция для декартова произведения множеств
func (p *PowerSet[T]) CartesianProduct(set2 PowerSet[T]) CartesianPowerSet[T] {
	resultSet := CartesianInit[T]()

	for first := range p.setSlots {
		for second := range set2.setSlots {
			// Создаем новый элемент из двух одиночных элементов
			elem := CartesianElement[T]{first: first, second: second}
			resultSet.Put(elem)
		}
	}
	return resultSet
}

// 10.5 функция, которая находит пересечение любых трёх и более множеств (принимает количество множеств >= 3 в качестве списка)
func IntersectionMultiple[T constraints.Ordered](sets []*PowerSet[T]) PowerSet[T] {
	set1 := sets[0]
	for _, set2 := range sets[1:] {
		res := set1.Intersection(*set2)
		set1 = &res
	}
	return *set1
}

// 10.6 мульти-множество (Bag), в котором каждый элемент может присутствовать несколько раз
// тут как раз можно применить структуру мапы, которая до это использовалась только для того, чтоб стандартным
// путем считать хэш. Теперь вместопустой структуры в качестве значения будем использовать счетчик значений
type BagPowerSet[T constraints.Ordered] struct {
	setSlots map[T]int
}

// создание экземпляра множества
func InitBag[T constraints.Ordered]() BagPowerSet[T] {
	return BagPowerSet[T]{setSlots: make(map[T]int)}
}

func (bs *BagPowerSet[T]) Put(value T) {
	if _, exists := bs.setSlots[value]; !exists {
		bs.setSlots[value] = 1
	} else {
		bs.setSlots[value] += 1
	}
}

func (bs *BagPowerSet[T]) Get(value T) bool {
	// возвращает true если value имеется в множестве
	_, exists := bs.setSlots[value]
	return exists
}

func (bs *BagPowerSet[T]) Remove(value T) bool {
	if counter, exists := bs.setSlots[value]; exists {
		if counter > 1 {
			bs.setSlots[value] -= 1
		} else {
			delete(bs.setSlots, value)
		}
		return true
	}
	return false
}

// получение всех элементов с их частотами. Можно было бы отдать весь словарь, но в задании сказано "список" :)
// введу структуру для пары значений элемент-частота
type Pair[T any] struct {
	Value T
	Freq  int
}

func (bs *BagPowerSet[T]) GetAllFrequents() []Pair[T] {
	var result []Pair[T]

	for val, freq := range bs.setSlots {
		result = append(result, Pair[T]{Value: val, Freq: freq})
	}
	return result
}

// Рефлексия по заданиям 8
// 3. Динамическая хэш-тблица
// Я добавил метод Rehash, который увеличивает размер слайса и перекачивает туда значения из старого стлайса.
// По сути слайс и сам по себе динамический массив, но для учебной цели перераспределение описано.
// Тут возникает вопрос - а в учебных заданиях мы можем ли испльзовать структуры уже прошедших заданий?
// Будет ли учебный сервер понимать, что именно я использовал, если я просто импортиирую из прошлого занятия какую-то структуру?
//
// 5. ddos хэш-таблицы и соль
// Я использовал соль хоть и статическукю, но для каждой таблицы свою (через случайные числа). Читал про способы
// организации динамической соли через анализ поступившего значения, согласен, что это было бы более надежно - наверное немного "срезал угол".
