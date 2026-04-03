//10

package main

import (
	"constraints"
	"os"
	"strconv"
)

type IPowerSet[T any] interface {
	Size() int
	Remove(value T) bool
	Get(value T) bool
	Put(value T)
	Intersection(set2 IPowerSet[T]) IPowerSet[T]
	Union(set2 IPowerSet[T]) IPowerSet[T]
	Difference(set2 IPowerSet[T]) IPowerSet[T]
	IsSubset(set2 IPowerSet[T]) bool
	Equals(set2 IPowerSet[T]) bool
}

type PowerSet[T constraints.Ordered] struct {
	// ваша реализация хранилища
	// я искал в Go решение для использования нормальной хэш-функции и наткнулся на распространенный прием - мапа с пустой структурой в качестве значения.
	// Не совсем сет, подход такой: проверяем по ключу налчие значения в мапе. Мапа под капотом применяет встроенную хэш-функцию и на ее основе однозначно возвращает наличие или отсутствие значения в словаре.
	setSlots map[T]struct{}
	size     int
}

// создание экземпляра множества
func Init[T constraints.Ordered]() PowerSet[T] {
	return PowerSet[T]{setSlots: make(map[T]struct{}), size: 0}
}

func (p *PowerSet[T]) Size() int {
	// количество элементов в множестве
	return p.size
}

// О(1)
func (p *PowerSet[T]) Put(value T) {
	if _, exists := p.setSlots[value]; !exists {
		p.setSlots[value] = struct{}{}
		p.size++
	}
}

// О(1)
func (p *PowerSet[T]) Get(value T) bool {
	// возвращает true если value имеется в множестве
	_, exists := p.setSlots[value]
	return exists
}

// О(1)
func (p *PowerSet[T]) Remove(value T) bool {
	// возвращает true если value удалено
	if _, exists := p.setSlots[value]; exists {
		delete(p.setSlots, value)
		p.size--
		return true
	}
	return false
}

// О(n) на создание нового множества, O(n) по времени на итерацию по множеству
func (p *PowerSet[T]) Intersection(set2 PowerSet[T]) PowerSet[T] {
	// пересечение текущего множества и set2
	var result PowerSet[T]

	result = Init[T]()
	for key := range p.setSlots {
		if set2.Get(key) {
			result.Put(key)
		}
	}
	return result
}

// О(n+m) на создание нового множества, O(n+m) по времени на итерацию по множествам
func (p *PowerSet[T]) Union(set2 PowerSet[T]) PowerSet[T] {
	// объединение текущего множества и set2
	var result PowerSet[T]

	result = Init[T]()
	for key := range p.setSlots {
		result.Put(key)
	}
	for key := range set2.setSlots {
		result.Put(key)
	}
	return result
}

// О(n) на создание нового множества, O(n) по времени на итерацию по множеству
func (p *PowerSet[T]) Difference(set2 PowerSet[T]) PowerSet[T] {
	// разница текущего множества и set2
	var result PowerSet[T]

	result = Init[T]()
	for key := range p.setSlots {
		if !set2.Get(key) {
			result.Put(key)
		}
	}
	return result
}

// O(n) по времени на итерацию по множеству
func (p *PowerSet[T]) IsSubset(set2 PowerSet[T]) bool {
	// возвращает true, если set2 есть подмножество текущего множества
	if set2.Size() > p.Size() {
		return false
	}

	for key := range set2.setSlots {
		if !p.Get(key) {
			return false
		}
	}
	return true
}

// O(n) по времени на итерацию по множеству
func (p *PowerSet[T]) Equals(set2 PowerSet[T]) bool {
	// возвращает true, если set2 равно текущему множеству
	if p.Size() != set2.Size() {
		return false
	}
	for key := range p.setSlots {
		if !set2.Get(key) {
			return false
		}
	}
	return true
}
