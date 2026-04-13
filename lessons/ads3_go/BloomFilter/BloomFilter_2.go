// 11
package main

import (
	"fmt"
)

// 11.2 слияние нескольких фильтров Блюма.
// В этом случае мы должны проверить вхождение бита хотя бы в один фильтр (логическое ИЛИ)
// При таком подходе вероятность ложно положительного срабатывания увеличивается
func Merge(filters []*BloomFilter) *BloomFilter {
	if len(filters) == 0 {
		return &BloomFilter{filterLen: 32, bitArray: 0}
	}

	// Создаём новый фильтр с параметрами первого
	merged := &BloomFilter{
		filterLen: filters[0].filterLen,
		bitArray:  0,
	}

	// Объединяем все битовые массивы через ИЛИ
	for _, bf := range filters {
		merged.bitArray |= bf.bitArray
	}

	return merged
}

// 11.3  фильтр Блюма, предусматривающий удаление элементов
// заведем два битовых массива:
// - mainArray: биты добавленных элементов
// - deletedArray: биты элементов, помеченных как удаленные. Очищать биты mainArray при удалении нельзя, поскольку они
// могут использоваться другими элементами, остающимимся в массиве.
//
// проверка наличия элемента: (Hash1 И Hash2 в mainArray) И НЕ (в deletedArray)
//
// также заведем массив (мапу) для элементов в массиве по значению. Это нужно для того, чтобы при попытке удалить элемент
// с ложноположительным совпадением (когда биты совпадают с добавленным элементом, но данный элемент не был явно добавлен),
// функция возвращала ошибку, чтобы избежать нарушения структуры.
type DeletableBloomFilter struct {
	filterLen     int
	mainArray     uint32
	deletedArray  uint32
	addedElements map[string]bool
}

func NewDeletableBloomFilter() *DeletableBloomFilter {
	return &DeletableBloomFilter{
		filterLen:     32,
		mainArray:     0,
		deletedArray:  0,
		addedElements: make(map[string]bool),
	}
}

func (dbf *DeletableBloomFilter) hashHelper(value string, salt int) uint32 {
	var sum uint32 = 0
	for _, char := range value {
		sum = (sum*uint32(salt) + uint32(char)) % uint32(dbf.filterLen)
	}
	return 1 << sum
}

func (dbf *DeletableBloomFilter) Hash1(s string) uint32 {
	return dbf.hashHelper(s, 17)
}

func (dbf *DeletableBloomFilter) Hash2(s string) uint32 {
	return dbf.hashHelper(s, 223)
}

// Устанавливает соответствующие биты в mainArray и регистрирует элемент в addedElements.
// Если элемент был ранее удален, очищает его из deletedArray.
func (dbf *DeletableBloomFilter) Add(s string) {
	mask1 := dbf.Hash1(s)
	mask2 := dbf.Hash2(s)

	dbf.mainArray |= mask1
	dbf.mainArray |= mask2

	if dbf.addedElements[s] == false && dbf.isValueInDeleted(s) {
		dbf.deletedArray &= ^mask1
		dbf.deletedArray &= ^mask2
	}

	dbf.addedElements[s] = true
}

func (dbf *DeletableBloomFilter) isValueInDeleted(s string) bool {
	mask1 := dbf.Hash1(s)
	mask2 := dbf.Hash2(s)
	return (mask1&dbf.deletedArray == mask1) && (mask2&dbf.deletedArray == mask2)
}

// IsValue проверяет наличие элемента в фильтре
// Возвращает true если:
// 1. Оба хеша установлены в mainArray
// 2. И оба НЕ установлены в deletedArray
func (dbf *DeletableBloomFilter) IsValue(s string) bool {
	mask1 := dbf.Hash1(s)
	mask2 := dbf.Hash2(s)

	inMain := (mask1&dbf.mainArray == mask1) && (mask2&dbf.mainArray == mask2)

	inDeleted := (mask1&dbf.deletedArray == mask1) && (mask2&dbf.deletedArray == mask2)

	return inMain && !inDeleted
}

// Remove удаляет элемент из фильтра
// Возвращает ошибку если:
// - Элемент не был явно добавлен (возможно ложноположительное совпадение)
//
// При успешном удалении:
// - Очищает биты в mainArray
// - Устанавливает биты в deletedArray
// - Удаляет элемент из addedElements
func (dbf *DeletableBloomFilter) Remove(s string) error {
	if !dbf.addedElements[s] {
		return fmt.Errorf("deletion error: cannot remove element %s", s)
	}

	mask1 := dbf.Hash1(s)
	mask2 := dbf.Hash2(s)

	dbf.mainArray &= ^mask1
	dbf.mainArray &= ^mask2

	dbf.deletedArray |= mask1
	dbf.deletedArray |= mask2

	delete(dbf.addedElements, s)

	return nil
}

func (dbf *DeletableBloomFilter) Clear() {
	dbf.mainArray = 0
	dbf.deletedArray = 0
	dbf.addedElements = make(map[string]bool)
}

// 11.4 Восстановление исходного множества для фильтра.
// Напишу честно: я пытался обсуждать с ИИ, гуглить и размышлять. Даже какой-то код нагенерировал,
// но не хочу его предоставлять - он не рабочий (т.е. он что-то делает, но в результате все равно не получается восстановить единственное значение).
// Алгоритм сводится в любом случае к перебору битов и попыткам подобрать под
// этот бит комбинацию символов. Потом оценка совпадения символов после регенерации одной хэш-функцией и второй.
// Если ввести еще и третью функцию, то задача становится вообще непредставимой. Плюс мы не знаем длины строк,
// которые хотим восстановить. У меня на длине 3 код просто вис, поскольку глубина рекурсии при переборе всех комбинаций
// хотя бы базовых символов, плюс время на анализ каждой комбинации по хэшу плюс по не одному хэшу все тормозило.
// На длине 2 выдавался список кандидатов довольно большой. В общем, тут я видимо не справился с реализацией.
// Или именно в этом и состоит задумка фильтра и хэширования - сделать восстановление значений крайне затруднительной задачей

// Рефлексия (забыл сразу)
// 9.5 я использовал два упорядоченных списка. Отличие от предложенного эталона - в том, что бинарный поиск осуществляется
// два раза - для ключей и значений.