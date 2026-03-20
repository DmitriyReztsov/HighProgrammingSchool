// 8.3 динамическая хэш-таблица, которая автоматически увеличивает свой размер, если места перестаёт хватать.
package main

import (
	"math/rand"
)

type DynamicHashTable struct {
	HashTable
	// для сбора статистики, добавил в 8.4 задании
	collisions int
	probeStats int
}

func NewDynamicHashTable(sz int, stp int) *DynamicHashTable {
	return &DynamicHashTable{HashTable: Init(sz, stp), collisions: 0, probeStats: 0}
}

func (dht *DynamicHashTable) SeekSlot(value string) int {
	hash := dht.HashFun(value)

	for i := 0; i < dht.size; i++ {
		index := (hash + i*dht.step) % dht.size
		dht.probeStats++ // Счётчик для статистики

		if !dht.occupied[index] {
			if i > 0 {
				dht.collisions++ // если потребовалось более одного зондирования - это коллизия
			}
			return index
		}
	}
	return -1
}

func (dht *DynamicHashTable) Rehash() {
	oldSlots := dht.slots
	oldOccupied := dht.occupied
	oldSize := dht.size

	dht.size = dht.size * 2

	dht.slots = make([]string, dht.size)
	dht.occupied = make([]bool, dht.size)

	for i := 0; i < oldSize; i++ {
		if oldOccupied[i] {
			value := oldSlots[i]
			index := dht.SeekSlot(value)

			if index != -1 {
				dht.slots[index] = value
				dht.occupied[index] = true
			}
		}
	}
}

func (dht *DynamicHashTable) Put(value string) int {
	index := dht.SeekSlot(value)

	// если нет свободных слотов - пробуем увеличить таблицу и вставить еще раз
	if index == -1 {
		dht.Rehash()
		dht.collisions = 0
		dht.probeStats = 0

		index = dht.SeekSlot(value)
		if index == -1 {
			return -1
		}
	}

	dht.slots[index] = value
	dht.occupied[index] = true
	return index
}

// два тестовых метода
func (dht *DynamicHashTable) Size() int {
	return dht.size
}

func (dht *DynamicHashTable) Count() int {
	count := 0
	for i := 0; i < dht.size; i++ {
		if dht.occupied[i] {
			count++
		}
	}
	return count
}

// возвращает текущий load factor (занятые слоты / размер)
func (dht *DynamicHashTable) LoadFactor() float64 {
	return float64(dht.Count()) / float64(dht.size)
}

// возвращает количество обнаруженных коллизий
func (dht *DynamicHashTable) CollisionCount() int {
	return dht.collisions
}

// возвращает общее число попыток зондирования
func (dht *DynamicHashTable) ProbeStats() int {
	return dht.probeStats
}

// возвращает среднее число попыток per Put
func (dht *DynamicHashTable) AverageProbeDepth() float64 {
	if dht.Count() == 0 {
		return 0
	}
	return float64(dht.probeStats) / float64(dht.Count())
}

// обнуляет счётчики для началаново измерения
func (dht *DynamicHashTable) ResetStats() {
	dht.collisions = 0
	dht.probeStats = 0
}

// 8.4 хэш-таблица, которая использует несколько хэш-функций для каждой операции вставки, чтобы уменьшить вероятность коллизий.
type MultiHashTable struct {
	*DynamicHashTable
}

func NewMultiHashTable(sz int, stp int) *MultiHashTable {
	return &MultiHashTable{
		DynamicHashTable: NewDynamicHashTable(sz, stp),
	}
}

// hash2Fun вычисляет вторую хеш-функцию для определения шага зондирования
func (mht *MultiHashTable) hash2Fun(value string) int {
	sum := 0
	for _, b := range []byte(value) {
		sum += int(b)
	}

	// Вторая функция: size - (sum % (size-1)) + 1
	second := mht.size - (sum % (mht.size - 1))
	if second == 0 || second > mht.size {
		second = mht.size / 2
	}
	return second
}

func (mht *MultiHashTable) SeekSlot(value string) int {
	hash1 := mht.HashFun(value)  // исходная позиция
	hash2 := mht.hash2Fun(value) // размер шага

	for i := 0; i < mht.size; i++ {
		// каждый шаг использует разный offset
		index := (hash1 + i*hash2) % mht.size
		mht.probeStats++ // Счётчик для статистики

		if !mht.occupied[index] {
			if i > 0 {
				mht.collisions++ // если потребовалось более одного зондирования - это коллизия
			}
			return index
		}
	}
	return -1
}

func (mht *MultiHashTable) Put(value string) int {
	index := mht.SeekSlot(value)

	// нет свободных слотов - увеличиваем таблицу (как в предыдущем задании)
	if index == -1 {
		mht.Rehash()
		mht.collisions = 0
		mht.probeStats = 0

		index = mht.SeekSlot(value)
		if index == -1 {
			return -1
		}
	}

	mht.slots[index] = value
	mht.occupied[index] = true
	return index
}

func (mht *MultiHashTable) Find(value string) int {
	hash1 := mht.HashFun(value)
	hash2 := mht.hash2Fun(value)

	for i := 0; i < mht.size; i++ {
		index := (hash1 + i*hash2) % mht.size

		if mht.occupied[index] && mht.slots[index] == value {
			return index
		}

		if !mht.occupied[index] {
			return -1
		}
	}
	return -1
}

func (mht *MultiHashTable) Rehash() {
	oldSlots := mht.slots
	oldOccupied := mht.occupied
	oldSize := mht.size

	mht.size = mht.size * 2

	mht.slots = make([]string, mht.size)
	mht.occupied = make([]bool, mht.size)

	for i := 0; i < oldSize; i++ {
		if oldOccupied[i] {
			value := oldSlots[i]
			index := mht.SeekSlot(value)

			if index != -1 {
				mht.slots[index] = value
				mht.occupied[index] = true
			}
		}
	}
}

// Анализ производительности и коллизий. На таблицах с маленьким количеством элементов разницы почти не видно.
// На таблицах размером в 170 элементов и загрузкой в 150 элементов видно, что в таблице с двойным хэшированием колиизий
// стало меньше, попыток размещения тоже. Но время заполнения при линейном пробировании меньше. Полагаю, что время поиска
// тут еще менее значимо, чем время высчитывания хэшей:

// >>> COMPARATIVE ANALYSIS: Double Hashing vs Linear Probing <<<
//     DOUBLE HASHING (MultiHashTable):
//        Size: 340, Count: 150, LoadFactor: 44.12%
//        Collisions: 81, TotalProbes: 505, AvgProbeDepth: 3.37
//        Execution time: 13.668µs

//     LINEAR PROBING (DynamicHashTable):
//        Size: 170, Count: 150, LoadFactor: 88.24%
//        Collisions: 131, TotalProbes: 2316, AvgProbeDepth: 15.44
//        Execution time: 6.924µs

// Если же взять следующий порядок (1700 - емкость таблицы и 1550 - элементов для заполнения), то подтягивается и выигрыш
// по времени в пользу двойного хэширования, и по коллизиям разница еще более явная, и попыток размещения еще меньше:

// >>> COMPARATIVE ANALYSIS: Double Hashing vs Linear Probing <<<
// DOUBLE HASHING (MultiHashTable):
//   Size: 13600, Count: 1550, LoadFactor: 11.40%
//   Collisions: 666, TotalProbes: 17609, AvgProbeDepth: 11.36
//   Execution time: 437.464µs
//
// LINEAR PROBING (DynamicHashTable):
//   Size: 1700, Count: 1550, LoadFactor: 91.18%
//   Collisions: 1531, TotalProbes: 358858, AvgProbeDepth: 231.52
//   Execution time: 767.3µs

// 8.5 защищённая хэш-таблица с солью для защиты от DDoS-атак
type SaltHashTable struct {
	*DynamicHashTable
	salt uint32
}

func NewSaltHashTable(sz int, stp int) *SaltHashTable {
	return &SaltHashTable{
		DynamicHashTable: NewDynamicHashTable(sz, stp),
		salt:             rand.Uint32(),
	}
}

func (sht *SaltHashTable) HashFun(value string) int {
	sum := 0
	for _, b := range []byte(value) {
		sum += int(b)
	}
	return (sum ^ int(sht.salt)) % sht.size
}

// далее в соответствии с радужными таблицами злоумышленник мог бы пытаться найти значение по хешу
// Например, все строки из ",", "=", "N", "_", "p", ")z", ":z", "Kz", "\\z", "mz" имеют хеш 10 (в текущей функции).
// Если мы добавим солью случайное число - то уже по этому хешу найти не получится.

// Рефлексия по заданию 6
// 6.4 провека на палиндром. Решение совпадает с эталонным - строку в деку, за тем с каждого конца берем символы.
// Отдельно проверяем случай, когда взяли последний центральный элемент.
//
// 6.5 Эталонный алгоритм вроде понял, но есть вопрос. Если мы удаляем из дополнительной деки элементы, большие текущего
// элемента, то как мы их получим после удаления минимального элемента. Мне кажется, что удалять нельзя, а если всегда
// вставлять в конец, а в голове дежать минимум - то это уже сортировка и операция вставки будет нам стоит О(n) на
// перебор (даже если удаление) элементов дополнительной деки. Мой вариант, котоый синхронно хранит на соответствующих
// позициях миниму для позиции кажется более правильным.
//
// 6.6 В моем случае в веке в качестве хранилища используется слайсы - что как раз и есть реализация динамического
// массива.
