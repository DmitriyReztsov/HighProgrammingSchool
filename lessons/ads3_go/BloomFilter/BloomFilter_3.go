// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import (
	"testing"
)

func rotations(s string) []string {
	n := len(s)
	res := make([]string, 0, n)

	for i := 0; i < n; i++ {
		res = append(res, s[i:]+s[:i])
	}
	return res
}

func TestBloomFilterAdd(t *testing.T) {
	bf := Init(32)

	values := rotations("0123456789")

	for _, val := range values {
		bf.Add(val)
	}

	if !bf.IsValue("0123456789") {
		t.Fatalf("BloomFilter should contain 0123456789")
	}

	if !bf.IsValue("1234567890") {
		t.Fatalf("BloomFilter should contain 1234567890")
	}

	if !bf.IsValue("8901234567") {
		t.Fatalf("BloomFilter should contain 8901234567")
	}

	if bf.IsValue("89012345670") {
		t.Logf("Warning: BloomFilter gave false positive for 'notadded'")
	}
}

func TestMergeBloomFilters(t *testing.T) {
	bf1 := Init(32)
	bf2 := Init(32)

	bf1.Add("0123456789")
	bf1.Add("1234567890")

	bf2.Add("8901234567")
	bf2.Add("9012345678")

	if !bf1.IsValue("0123456789") {
		t.Fatalf("Filter 1 should contain 0123456789")
	}
	if !bf2.IsValue("8901234567") {
		t.Fatalf("Filter 2 should contain 8901234567")
	}

	merged := Merge([]*BloomFilter{&bf1, &bf2})

	if !merged.IsValue("0123456789") {
		t.Fatalf("Merged should contain 0123456789 from filter 1")
	}
	if !merged.IsValue("1234567890") {
		t.Fatalf("Merged should contain 1234567890 from filter 1")
	}
	if !merged.IsValue("8901234567") {
		t.Fatalf("Merged should contain 8901234567 from filter 2")
	}
	if !merged.IsValue("9012345678") {
		t.Fatalf("Merged should contain 9012345678 from filter 2")
	}
}

func TestDeletableBloomFilter(t *testing.T) {
	dbf := NewDeletableBloomFilter()

	elements := []string{"apple", "banana", "cherry"}

	for _, elem := range elements {
		dbf.Add(elem)
	}

	for _, elem := range elements {
		if !dbf.IsValue(elem) {
			t.Errorf("Expected %s to be in filter, but it was not found", elem)
		}
	}

	err := dbf.Remove("apple")
	if err != nil {
		t.Errorf("Failed to remove existing element: %v", err)
	}

	if dbf.IsValue("apple") {
		t.Errorf("Expected %s to NOT be in filter after removing", "apple")
	}

	// Пытаемся удалить элемент, который уже удален
	err = dbf.Remove("apple")

	if err == nil {
		t.Error("Expected an error when removing non-existent element, but got nil")
	}

	if !dbf.IsValue("banana") {
		t.Errorf("Element banana was affected when trying to remove non-existent element")
	}

	if !dbf.IsValue("cherry") {
		t.Errorf("Element cherry was affected when trying to remove non-existent element")
	}
}
