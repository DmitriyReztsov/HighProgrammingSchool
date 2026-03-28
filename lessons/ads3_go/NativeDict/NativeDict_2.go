package main

import (
	"constraints"
	"errors"
)

// 9.5 словарь с использованием упорядоченного списка по ключу. Рассматривал два варианта:
// двунаправленный список как в одном из предыдущих заданий и на слайсах. Двунаправленный список давал бы
// O(n) практически по всем операциям. Поиск, вставка (в основе которой снова поиск места), получение.
//
// Слайсы дают нам быстрый поиск O(log n) через бинарный поиск в двух упорядоченных слайсах
// Один слайс для ключей, второй для значений

// Сложности:
// Get(key): O(log n) - бинарный поиск
// Put (обновление): O(log n) на поиск
// Put (вставка нового): O(n) на сдвиг (копирование слайса в новый)
// IsKey(key): O(log n)
// Delete(key): O(n) на сдвиг

type OrderedListDictionary[K constraints.Ordered, V any] struct {
	keys   []K
	values []V
}

func NewOrderedListDictionary[K constraints.Ordered, V any]() *OrderedListDictionary[K, V] {
	return &OrderedListDictionary[K, V]{
		keys:   make([]K, 0),
		values: make([]V, 0),
	}
}

// Сложность: O(log n)
func (od *OrderedListDictionary[K, V]) findIndex(key K) int {
	left, right := 0, len(od.keys)

	for left < right {
		mid := (left + right) / 2

		if od.keys[mid] == key {
			return mid
		} else if od.keys[mid] < key {
			left = mid + 1
		} else {
			right = mid
		}
	}

	return -1
}

// Сложность: O(log n)
func (od *OrderedListDictionary[K, V]) findInsertPosition(key K) int {
	left, right := 0, len(od.keys)

	for left < right {
		mid := (left + right) / 2

		if od.keys[mid] < key {
			left = mid + 1
		} else {
			right = mid
		}
	}

	return left
}

func (od *OrderedListDictionary[K, V]) IsKey(key K) bool {
	return od.findIndex(key) != -1
}

func (od *OrderedListDictionary[K, V]) Get(key K) (V, error) {
	var result V

	idx := od.findIndex(key)
	if idx == -1 {
		return result, errors.New("key not found")
	}

	return od.values[idx], nil
}

func (od *OrderedListDictionary[K, V]) Put(key K, value V) {
	idx := od.findIndex(key)

	if idx != -1 {
		od.values[idx] = value
		return
	}

	insertIdx := od.findInsertPosition(key)

	od.keys = append(od.keys, key)
	copy(od.keys[insertIdx+1:], od.keys[insertIdx:])
	od.keys[insertIdx] = key

	od.values = append(od.values, value)
	copy(od.values[insertIdx+1:], od.values[insertIdx:])
	od.values[insertIdx] = value
}

// Сложность: O(n) - поиск O(log n) + сдвиг O(n)
func (od *OrderedListDictionary[K, V]) Delete(key K) error {
	idx := od.findIndex(key)
	if idx == -1 {
		return errors.New("key not found")
	}

	od.keys = append(od.keys[:idx], od.keys[idx+1:]...)

	od.values = append(od.values[:idx], od.values[idx+1:]...)

	return nil
}

// 9.6 словарь, в котором ключи представлены битовыми строками фиксированной длины.
// Плотная таблица размера 2^bitWidth: индекс = (key & keyMask). Занятость хранится в битсете (сдвиги и маски по слоту).
// Память Θ(2^bitWidth)
//
// Сложности: Put, Get, IsKey, Delete — O(1) после нормализации ключа одной побитовой маской.

type BitStringDictionary[V any] struct {
	bitWidth      int
	keyMask       uint64
	values        []V
	occupiedSlots []uint64 // битовая карта занятых слотов
}

func keyMaskForBitWidth(bitWidth int) uint64 {
	// строим маску чтобы отрезать от битового представления ключа лишние старшие биты
	if bitWidth == 64 {
		// ^uint64(0) — побитовое НЕ от нуля: получается все биты = 1, то есть маска на весь uint64.
		return ^uint64(0)
	}
	return (uint64(1) << uint(bitWidth)) - 1 // сдвиг дает число 10000, вычитание 1 дает число 1111
}

// Каждый слот словаря — один бит «занято/свободно».
// Вместо []bool на все слоты использую плотный битсет из []uint64;
// occWordsForSlots вычисляет длину этого слайса в словах.
func occWordsForSlots(nSlots int) int {
	return (nSlots + 63) / 64
}

func NewBitStringDictionary[V any](bitWidth int) *BitStringDictionary[V] {
	nSlots := 1 << bitWidth // число возможных ключей длины bitWidth бит, число слотов в словаре
	return &BitStringDictionary[V]{
		bitWidth:      bitWidth,
		keyMask:       keyMaskForBitWidth(bitWidth),
		values:        make([]V, nSlots),
		occupiedSlots: make([]uint64, occWordsForSlots(nSlots)),
	}
}

func (d *BitStringDictionary[V]) normalizeKey(key uint64) uint64 {
	return key & d.keyMask
}

func (d *BitStringDictionary[V]) slotOccupied(slot int) bool {
	// slot>>6 - находим слово в массиве занятых слотов (каждые 64 бита - одно слово)
	// slot&63 - находим номер бита в слове (если слот 69 - то во втором слове 5 бит от 0)
	// (uint64(1)<<uint(slot&63)) - сдвигаем 1 на нужное количество бит, создаем маску
	// & - побитовое И, если в маске есть 1, то слот занят
	return d.occupiedSlots[slot>>6]&(uint64(1)<<uint(slot&63)) != 0
}

func (d *BitStringDictionary[V]) setOccupied(slot int) {
	// находим слово в массиве занятых слотов
	// находим номер бита в слове и делаем маску
	// | - побитовое ИЛИ, устанавливаем бит в 1
	d.occupiedSlots[slot>>6] |= uint64(1) << uint(slot&63)
}

func (d *BitStringDictionary[V]) clearOccupied(slot int) {
	// &^ - побитовое И НЕ, очищаем бит в 0
	d.occupiedSlots[slot>>6] &^= uint64(1) << uint(slot&63)
}

func (d *BitStringDictionary[V]) Put(key uint64, value V) {
	idx := int(d.normalizeKey(key))
	d.values[idx] = value
	d.setOccupied(idx)
}

func (d *BitStringDictionary[V]) Get(key uint64) (V, error) {
	var zero V

	idx := int(d.normalizeKey(key))
	if !d.slotOccupied(idx) {
		return zero, errors.New("key not found")
	}
	return d.values[idx], nil
}

func (d *BitStringDictionary[V]) IsKey(key uint64) bool {
	return d.slotOccupied(int(d.normalizeKey(key)))
}

func (d *BitStringDictionary[V]) Delete(key uint64) error {
	var zero V

	idx := int(d.normalizeKey(key))
	if !d.slotOccupied(idx) {
		return errors.New("key not found")
	}
	d.clearOccupied(idx)
	d.values[idx] = zero
	return nil
}

// рефлексия задания 7
// 7.9. я воспользовался подходом из сортировки слиянием, только тут списки уже отсотированы. Подход как в эталоне
//
// 7.10. в целом подход как в эталоне, за исключением того, что я не смотрел на длины оставшихся подсписков.
// С одной стороны это алгоритмичный подход, с другой реализация нашего списка не хранит длины подсписков, а значит
// для проверки надо каждый раз дополнительно проходить n элементов на каждом подсписке.
//
// 7.11. В целом подход по подсчету наиболее часто встречающегося элемента у мнея схож. Отличия в том, что я фиксирую
// элемент, с которым сравниваю текущий. Действительно, можно было бы не фиксировать, а смещать окно из двух элементов
// синхронно.
//
// 7.12. Решение совпало с эталонным - применил слайсы для доступа по индексу и прошелся бинарным поиском.
