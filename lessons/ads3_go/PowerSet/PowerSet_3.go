// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import (
	"strconv"
	"testing"
	"time"
)

func TestAddPowerSet(t *testing.T) {
	ps := Init[int]()

	ps.Put(1)
	if ps.Size() != 1 {
		t.Fatalf("PowerSet should be size of 1")
	}

	if !ps.Get(1) {
		t.Fatalf("PowerSet should contain element 1")
	}

	// добавляем уже присутствующий элемент, не должно ничего поменяться
	ps.Put(1)
	if ps.Size() != 1 {
		t.Fatalf("PowerSet should be size of 1")
	}

	if !ps.Get(1) {
		t.Fatalf("PowerSet should contain element 1")
	}
}

func TestRemovePowerSet(t *testing.T) {
	ps := Init[int]()

	ps.Put(1)
	ps.Put(2)
	ps.Put(3)
	if ps.Size() != 3 {
		t.Fatalf("PowerSet should be size of 3")
	}

	if !ps.Remove(2) {
		t.Fatalf("PowerSet should remove element 2")
	}

	if ps.Remove(2) {
		t.Fatalf("PowerSet should NOT remove already removed element 2")
	}
}

func TestIntersectionPowerSet(t *testing.T) {
	// два непустых множества имеют общие элементы - пересечение дает новое множество
	ps1 := Init[int]()
	ps1.Put(1)
	ps1.Put(2)
	ps1.Put(3)

	ps2 := Init[int]()
	ps2.Put(2)
	ps2.Put(3)
	ps2.Put(4)

	result := ps1.Intersection(ps2)
	if result.Size() != 2 {
		t.Fatalf("Intersection of {1,2,3} and {2,3,4} should have size 2")
	}
	if !result.Get(2) || !result.Get(3) {
		t.Fatalf("Intersection should contain elements 2 and 3")
	}

	// два непустых множества без общихх элементов - пересечение дает пустое множество
	ps3 := Init[int]()
	ps3.Put(1)
	ps3.Put(2)

	ps4 := Init[int]()
	ps4.Put(3)
	ps4.Put(4)

	result = ps3.Intersection(ps4)
	if result.Size() != 0 {
		t.Fatalf("Intersection of {1,2} and {3,4} should be empty")
	}

	// два множества - одно пустое - пересечение дает пустое множество
	ps5 := Init[int]()
	ps5.Put(1)
	ps5.Put(2)

	ps6 := Init[int]()

	result = ps5.Intersection(ps6)
	if result.Size() != 0 {
		t.Fatalf("Intersection with empty set should be empty")
	}

	// два пустых множества - пересеение дает пустое множество
	ps7 := Init[int]()
	ps8 := Init[int]()

	result = ps7.Intersection(ps8)
	if result.Size() != 0 {
		t.Fatalf("Intersection of two empty sets should be empty")
	}
}

func TestUnionPowerSet(t *testing.T) {
	// объединение двух непустых множеств с общими элементами
	ps1 := Init[int]()
	ps1.Put(1)
	ps1.Put(2)
	ps1.Put(3)

	ps2 := Init[int]()
	ps2.Put(2)
	ps2.Put(3)
	ps2.Put(4)

	result := ps1.Union(ps2)
	if result.Size() != 4 {
		t.Fatalf("Union of {1,2,3} and {2,3,4} should have size 4")
	}
	if !result.Get(1) || !result.Get(2) || !result.Get(3) || !result.Get(4) {
		t.Fatalf("Union should contain elements 1, 2, 3, and 4")
	}

	// объединение двух непустых множеств без общих элементов
	ps3 := Init[int]()
	ps3.Put(1)
	ps3.Put(2)

	ps4 := Init[int]()
	ps4.Put(3)
	ps4.Put(4)

	result = ps3.Union(ps4)
	if result.Size() != 4 {
		t.Fatalf("Union of {1,2} and {3,4} should have size 4")
	}
	if !result.Get(1) || !result.Get(2) || !result.Get(3) || !result.Get(4) {
		t.Fatalf("Union should contain all elements 1, 2, 3, and 4")
	}

	// объединение непустого и пустого множеств
	ps5 := Init[int]()
	ps5.Put(1)
	ps5.Put(2)

	ps6 := Init[int]()

	result = ps5.Union(ps6)
	if result.Size() != 2 {
		t.Fatalf("Union with empty set should have size 2")
	}
	if !result.Get(1) || !result.Get(2) {
		t.Fatalf("Union should contain elements 1 and 2")
	}

	// пустое и пустое множесва - пустое множество
	ps7 := Init[int]()
	ps8 := Init[int]()

	result = ps7.Union(ps8)
	if result.Size() != 0 {
		t.Fatalf("Union of two empty sets should be empty")
	}
}

func TestDifferencePowerSet(t *testing.T) {
	// два непустых с общими элементами
	ps1 := Init[int]()
	ps1.Put(1)
	ps1.Put(2)
	ps1.Put(3)

	ps2 := Init[int]()
	ps2.Put(2)
	ps2.Put(3)
	ps2.Put(4)

	result := ps1.Difference(ps2)
	if result.Size() != 1 {
		t.Fatalf("Difference of {1,2,3} and {2,3,4} should have size 1")
	}
	if !result.Get(1) {
		t.Fatalf("Difference should contain only element 1")
	}

	// два непустых множества без общих элементов
	ps3 := Init[int]()
	ps3.Put(1)
	ps3.Put(2)

	ps4 := Init[int]()
	ps4.Put(3)
	ps4.Put(4)

	result = ps3.Difference(ps4)
	if result.Size() != 2 {
		t.Fatalf("Difference of {1,2} and {3,4} should have size 2")
	}
	if !result.Get(1) || !result.Get(2) {
		t.Fatalf("Difference should contain elements 1 and 2")
	}

	// два непустых множества полностью с одинаковыми элементами
	ps5 := Init[int]()
	ps5.Put(1)
	ps5.Put(2)

	ps6 := Init[int]()
	ps6.Put(1)
	ps6.Put(2)

	result = ps5.Difference(ps6)
	if result.Size() != 0 {
		t.Fatalf("Difference of {1,2} and {1,2} should be empty")
	}

	// пустое и непустое множество
	ps7 := Init[int]()

	ps8 := Init[int]()
	ps8.Put(1)
	ps8.Put(2)

	result = ps7.Difference(ps8)
	if result.Size() != 0 {
		t.Fatalf("Difference of empty set and {1,2} should be empty")
	}

	// непустое и пустое
	ps9 := Init[int]()
	ps9.Put(1)
	ps9.Put(2)

	ps10 := Init[int]()

	result = ps9.Difference(ps10)
	if result.Size() != 2 {
		t.Fatalf("Difference of {1,2} and empty set should have size 2")
	}
	if !result.Get(1) || !result.Get(2) {
		t.Fatalf("Difference should contain elements 1 and 2")
	}
}

func TestIsSubsetPowerSet(t *testing.T) {
	// все элементы параметра входят в текущее множество
	ps1 := Init[int]()
	ps1.Put(1)
	ps1.Put(2)
	ps1.Put(3)

	ps2 := Init[int]()
	ps2.Put(2)
	ps2.Put(3)

	if !ps1.IsSubset(ps2) {
		t.Fatalf("{2,3} should be subset of {1,2,3}")
	}

	// все элементы текущего множества входят в параметр
	ps3 := Init[int]()
	ps3.Put(1)
	ps3.Put(2)

	ps4 := Init[int]()
	ps4.Put(1)
	ps4.Put(2)
	ps4.Put(3)
	ps4.Put(4)

	if ps3.IsSubset(ps4) {
		t.Fatalf("{1,2,3,4} should NOT be subset of {1,2}")
	}

	// не все элементы параметра входят в текущее множество
	ps5 := Init[int]()
	ps5.Put(1)
	ps5.Put(2)
	ps5.Put(3)
	ps5.Put(4)

	ps6 := Init[int]()
	ps6.Put(2)
	ps6.Put(3)
	ps6.Put(5)

	if ps5.IsSubset(ps6) {
		t.Fatalf("{2,3,5} should NOT be subset of {1,2,3,4}")
	}
}

func TestEqualsPowerSet(t *testing.T) {
	// два множества с одинаковыми элементами - равны
	ps1 := Init[int]()
	ps1.Put(1)
	ps1.Put(2)
	ps1.Put(3)

	ps2 := Init[int]()
	ps2.Put(1)
	ps2.Put(2)
	ps2.Put(3)

	if !ps1.Equals(ps2) {
		t.Fatalf("{1,2,3} should be equal to {1,2,3}")
	}

	// два множества с разными элементами - не равны
	ps3 := Init[int]()
	ps3.Put(1)
	ps3.Put(2)

	ps4 := Init[int]()
	ps4.Put(1)
	ps4.Put(2)
	ps4.Put(3)

	if ps3.Equals(ps4) {
		t.Fatalf("{1,2} should NOT be equal to {1,2,3}")
	}

	// два пустых множества - равны
	ps5 := Init[int]()
	ps6 := Init[int]()

	if !ps5.Equals(ps6) {
		t.Fatalf("Empty sets should be equal")
	}

	// одно пустое, одно непустое - не равны
	ps7 := Init[int]()
	ps7.Put(1)

	ps8 := Init[int]()

	if ps7.Equals(ps8) {
		t.Fatalf("{1} should NOT be equal to empty set")
	}
}

func TestPerformancePowerSet(t *testing.T) {
	// операции над множествами из десятков тысяч элементов должны укладываться в пару секунд

	// Intersection
	start := time.Now()
	ps1 := Init[string]()
	ps2 := Init[string]()

	for i := 0; i < 50000; i++ {
		ps1.Put(strconv.Itoa(i))
	}

	for i := 25000; i < 75000; i++ {
		ps2.Put(strconv.Itoa(i))
	}

	result := ps1.Intersection(ps2)
	intersectionTime := time.Since(start)

	if intersectionTime > 2*time.Second {
		t.Fatalf("Intersection of 50K and 50K elements took %v, should be < 2 seconds", intersectionTime)
	}
	if result.Size() != 25000 {
		t.Fatalf("Intersection should have size 25000")
	}

	// Union
	start = time.Now()
	ps3 := Init[string]()
	ps4 := Init[string]()

	for i := 0; i < 50000; i++ {
		ps3.Put(strconv.Itoa(i))
	}

	for i := 50000; i < 100000; i++ {
		ps4.Put(strconv.Itoa(i))
	}

	result = ps3.Union(ps4)
	unionTime := time.Since(start)

	if unionTime > 2*time.Second {
		t.Fatalf("Union of 50K and 50K elements took %v, should be < 2 seconds", unionTime)
	}
	if result.Size() != 100000 {
		t.Fatalf("Union should have size 100000")
	}

	// Difference
	start = time.Now()
	ps5 := Init[string]()
	ps6 := Init[string]()

	for i := 0; i < 50000; i++ {
		ps5.Put(strconv.Itoa(i))
	}

	for i := 25000; i < 75000; i++ {
		ps6.Put(strconv.Itoa(i))
	}

	result = ps5.Difference(ps6)
	differenceTime := time.Since(start)

	if differenceTime > 2*time.Second {
		t.Fatalf("Difference of 50K and 50K elements took %v, should be < 2 seconds", differenceTime)
	}
	if result.Size() != 25000 {
		t.Fatalf("Difference should have size 25000")
	}
}

func TestCartezianPowerSet(t *testing.T) {
	ps1 := Init[int]()
	ps1.Put(1)
	ps1.Put(2)
	ps1.Put(3)

	ps2 := Init[int]()
	ps2.Put(11)
	ps2.Put(22)
	ps2.Put(33)

	result := ps1.CartesianProduct(ps2)

	expectedElements := []CartesianElement[int]{
		NewCartesianElement(1, 11),
		NewCartesianElement(1, 22),
		NewCartesianElement(1, 33),
		NewCartesianElement(2, 11),
		NewCartesianElement(2, 22),
		NewCartesianElement(2, 33),
		NewCartesianElement(3, 11),
		NewCartesianElement(3, 22),
		NewCartesianElement(3, 33),
	}

	for _, elem := range expectedElements {
		if !result.Get(elem) {
			t.Fatalf("CartesianProduct should contain element %v", elem)
		}
	}
}

func TestIntersectionMultiple(t *testing.T) {
	// 3 множества с частичным пересечением
	ps1 := Init[int]()
	ps1.Put(1)
	ps1.Put(2)
	ps1.Put(3)
	ps1.Put(4)
	ps1.Put(5)

	ps2 := Init[int]()
	ps2.Put(2)
	ps2.Put(3)
	ps2.Put(4)
	ps2.Put(5)
	ps2.Put(6)

	ps3 := Init[int]()
	ps3.Put(3)
	ps3.Put(4)
	ps3.Put(5)
	ps3.Put(6)
	ps3.Put(7)

	result := IntersectionMultiple([]*PowerSet[int]{&ps1, &ps2, &ps3})

	// Ожидаемое пересечение: {3, 4, 5}
	if !result.Get(3) || !result.Get(4) || !result.Get(5) {
		t.Fatalf("IntersectionMultiple should contain elements 3, 4, and 5")
	}

	if result.Get(1) || result.Get(2) || result.Get(6) || result.Get(7) {
		t.Fatalf("IntersectionMultiple should NOT contain elements 1, 2, 6, or 7")
	}

	// 4 множества без пересечения
	ps4 := Init[int]()
	ps4.Put(1)
	ps4.Put(2)

	ps5 := Init[int]()
	ps5.Put(3)
	ps5.Put(4)

	ps6 := Init[int]()
	ps6.Put(5)
	ps6.Put(6)

	ps7 := Init[int]()
	ps7.Put(7)
	ps7.Put(8)

	result2 := IntersectionMultiple([]*PowerSet[int]{&ps4, &ps5, &ps6, &ps7})

	if result2.Size() != 0 {
		t.Fatalf("IntersectionMultiple of disjoint sets should be empty, got size %d", result2.Size())
	}
}

func TestGetAllFrequents(t *testing.T) {
	bag := InitBag[int]()

	bag.Put(10)
	bag.Put(10)
	bag.Put(10)
	bag.Put(20)
	bag.Put(20)
	bag.Put(30)

	result := bag.GetAllFrequents()

	if len(result) != 3 {
		t.Errorf("ожидали 3 уникальных элемента")
	}

	freqMap := make(map[int]int)
	for _, pair := range result {
		freqMap[pair.Value] = pair.Freq
	}

	expectedFreqs := map[int]int{10: 3, 20: 2, 30: 1}
	for val, expectedFreq := range expectedFreqs {
		if freq, exists := freqMap[val]; !exists || freq != expectedFreq {
			t.Errorf("для элемента %d ожидали частоту %d, получили %d", val, expectedFreq, freq)
		}
	}
}
