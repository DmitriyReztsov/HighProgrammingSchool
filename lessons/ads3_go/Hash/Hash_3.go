// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import (
	"fmt"
	// "strconv"
	"testing"
	"time"
)

func TestHashFunConsistency(t *testing.T) {
	ht := Init(17, 3)

	value := "hello"
	hash1 := ht.HashFun(value)
	hash2 := ht.HashFun(value)

	if hash1 != hash2 {
		t.Fatalf("HashFun not consistent: got %d and %d for same input", hash1, hash2)
	}

	if hash1 < 0 || hash1 >= ht.size {
		t.Fatalf("HashFun returned out of range: %d, size: %d", hash1, ht.size)
	}
}

func TestHashFunRange(t *testing.T) {
	ht := Init(19, 3)

	testValues := []string{"", "a", "hello", "world", "test123", "abcdefghijk"}

	for _, val := range testValues {
		hash := ht.HashFun(val)
		if hash < 0 || hash >= ht.size {
			t.Fatalf("HashFun out of range for %q: got %d, size: %d", val, hash, ht.size)
		}
	}
}

func TestHashFunDifferentValues(t *testing.T) {
	ht := Init(17, 3)

	hashes := make(map[int]string)
	testValues := []string{"apple", "banana", "cherry", "date", "elderberry"}

	for _, val := range testValues {
		hash := ht.HashFun(val)
		if existing, found := hashes[hash]; found {
			t.Fatalf("Collision: %q and %q both hash to %d", existing, val, hash)
		}
		hashes[hash] = val
	}
}

func TestPutSingleValue(t *testing.T) {
	ht := Init(17, 3)

	value := "hello"
	index := ht.Put(value)

	if index == -1 {
		t.Fatalf("Put failed")
	}

	if index < 0 || index >= ht.size {
		t.Fatalf("Put out of range index: %d", index)
	}

	if ht.slots[index] != value {
		t.Fatalf("Wrong value at index %d", index)
	}
}

func TestPutMultipleValues(t *testing.T) {
	ht := Init(19, 3)

	testValues := []string{"first", "second", "third"}
	indices := make(map[int]bool)

	for _, val := range testValues {
		index := ht.Put(val)

		if index == -1 {
			t.Fatalf("Put failed for %q", val)
			continue
		}

		if indices[index] {
			t.Fatalf("Put returned duplicate index %d", index)
		}

		indices[index] = true

		if ht.slots[index] != val {
			t.Fatalf("Value %q not found at index %d", val, index)
		}
	}

	if len(indices) != len(testValues) {
		t.Fatalf("Expected %d unique indices, got %d", len(testValues), len(indices))
	}
}

func TestSeekSlotCollisionHandling(t *testing.T) {
	ht := Init(11, 3)

	// Insert first value
	val1 := "test1"
	index1 := ht.SeekSlot(val1)
	if index1 == -1 {
		t.Fatal("SeekSlot failed for first value")
	}
	ht.slots[index1] = val1
	ht.occupied[index1] = true

	val2 := "test2"
	index2 := ht.SeekSlot(val2)

	if index2 == -1 {
		t.Fatalf("SeekSlot failed to find slot despite available space")
	}

	if index2 == index1 {
		t.Fatalf("SeekSlot returned same index for different values")
	}

	ht.slots[index2] = val2
	ht.occupied[index2] = true

	if ht.slots[index1] != val1 {
		t.Fatalf("First value not stored correctly")
	}
	if ht.slots[index2] != val2 {
		t.Fatalf("Second value not stored correctly")
	}
}

func TestPutCollisionResolution(t *testing.T) {
	ht := Init(11, 2)

	testValues := []string{"a", "b", "c", "d", "e"}
	insertedIndices := make([]int, 0)

	for _, val := range testValues {
		index := ht.Put(val)

		if index == -1 {
			t.Fatalf("Put failed for %q", val)
			continue
		}

		for _, prevIdx := range insertedIndices {
			if index == prevIdx {
				t.Fatalf("Put returned duplicate index")
			}
		}

		insertedIndices = append(insertedIndices, index)
	}

	for _, val := range testValues {
		found := false
		for _, idx := range insertedIndices {
			if ht.slots[idx] == val {
				found = true
				break
			}
		}
		if !found {
			t.Fatalf("Value %q not found after insertion", val)
		}
	}
}

func TestFindExistingValues(t *testing.T) {
	ht := Init(17, 3)

	testValues := []string{"apple", "banana", "cherry"}
	insertedIndices := make(map[string]int)

	for _, val := range testValues {
		index := ht.Put(val)
		if index == -1 {
			t.Fatalf("Put failed for %q", val)
		}
		insertedIndices[val] = index
	}

	for val, expectedIdx := range insertedIndices {
		foundIdx := ht.Find(val)

		if foundIdx == -1 {
			t.Fatalf("Find failed to locate %q", val)
			continue
		}

		if foundIdx != expectedIdx {
			t.Fatalf("Find returned wrong index for %q: expected %d, got %d", val, expectedIdx, foundIdx)
		}
	}
}

func TestFindNonExistent(t *testing.T) {
	ht := Init(17, 3)

	ht.Put("hello")
	ht.Put("world")

	nonExistent := []string{"foo", "bar", "baz"}

	for _, val := range nonExistent {
		index := ht.Find(val)
		if index != -1 {
			t.Fatalf("Find should be -1")
		}
	}
}

func TestFindEmpty(t *testing.T) {
	ht := Init(17, 3)

	index := ht.Find("anything")

	if index != -1 {
		t.Fatalf("Find in empty table returned %d instead of -1", index)
	}
}

func TestDuplicateInsertion(t *testing.T) {
	ht := Init(17, 3)

	value := "duplicate"

	index1 := ht.Put(value)
	index2 := ht.Put(value)

	if index1 == -1 {
		t.Fatalf("First Put failed")
	}

	if index2 == -1 {
		t.Fatalf("Second Put failed (table full or slot not found)")
	}

	if index1 == index2 {
		t.Logf("Duplicates inserted at same slot (overwrites): indices %d", index1)
	} else {
		t.Logf("Duplicates inserted at different slots: %d and %d", index1, index2)
	}

	found := ht.Find(value)
	if found == -1 {
		t.Fatalf("Find failed to locate duplicate")
	}
}

func TestTableCapacity(t *testing.T) {
	size := 11
	ht := Init(size, 3)

	for i := 0; i < size; i++ {
		val := "value" + string(rune('0'+i))
		ht.Put(val)
	}

	overflowVal := "overflow"
	index := ht.Put(overflowVal)

	if index != -1 {
		t.Fatalf("Put on full table")
	}
}

func TestSeekSlotFull(t *testing.T) {
	ht := Init(5, 1)

	for i := 0; i < 5; i++ {
		ht.slots[i] = "full"
		ht.occupied[i] = true
	}

	index := ht.SeekSlot("anything")

	if index != -1 {
		t.Fatalf("SeekSlot should return -1 on full table")
	}
}

func TestEmptyStringValue(t *testing.T) {
	ht := Init(17, 3)

	emptyStr := ""

	index := ht.Put(emptyStr)

	if index == -1 {
		t.Fatalf("Put failed to insert empty string")
	}

	if ht.slots[index] != emptyStr {
		t.Fatalf("Empty string not stored correctly")
	}

	if !ht.occupied[index] {
		t.Fatalf("Occupied flag not set for empty string")
	}

	foundIdx := ht.Find(emptyStr)

	if foundIdx == -1 {
		t.Fatalf("Find failed to locate empty string")
	}

	if foundIdx != index {
		t.Fatalf("Find returned wrong index: expected %d, got %d", index, foundIdx)
	}
}

func TestMixedEmptyAndNonEmpty(t *testing.T) {
	ht := Init(19, 3)

	idx1 := ht.Put("hello")
	if idx1 == -1 {
		t.Fatalf("Put failed for 'hello'")
	}

	idx2 := ht.Put("")
	if idx2 == -1 {
		t.Fatalf("Put failed for empty string")
	}

	idx3 := ht.Put("world")
	if idx3 == -1 {
		t.Fatalf("Put failed for 'world'")
	}

	if ht.Find("hello") != idx1 {
		t.Fatalf("Find failed for 'hello'")
	}

	if ht.Find("") != idx2 {
		t.Fatalf("Find failed for empty string")
	}

	if ht.Find("world") != idx3 {
		t.Fatalf("Find failed for 'world'")
	}
}

func TestDynamicHashTableSingleResize(t *testing.T) {
	dht := NewDynamicHashTable(5, 2)

	if dht.Size() != 5 {
		t.Fatalf("Initial size should be 5, got %d", dht.Size())
	}

	testValues := []string{"apple", "banana", "cherry", "date", "fig"}
	insertedIndices := make(map[string]int)

	for i, val := range testValues {
		index := dht.Put(val)
		if index == -1 {
			t.Fatalf("Failed to insert value %d : %q before resize", i+1, val)
		}
		insertedIndices[val] = index
	}

	for _, val := range testValues {
		if dht.Find(val) == -1 {
			t.Fatalf("Value %q not found after initial inserts", val)
		}
	}

	if dht.Count() != 5 {
		t.Fatalf("Count should be 5 after initial inserts, got %d", dht.Count())
	}

	newValue := "grapefruit"
	index := dht.Put(newValue)
	if index == -1 {
		t.Fatalf("Put failed for new value after resize trigger")
	}

	if dht.Size() != 10 {
		t.Fatalf("Size should be 10, got %d", dht.Size())
	}

	for _, val := range testValues {
		foundIdx := dht.Find(val)
		if foundIdx == -1 {
			t.Fatalf("Original value %q lost after resize", val)
		}

		if dht.slots[foundIdx] != val {
			t.Fatalf("Value at found index : expected %q, got %q", val, dht.slots[foundIdx])
		}
	}

	if dht.Find(newValue) == -1 {
		t.Fatalf("New value %q not found after resize", newValue)
	}

	if dht.slots[index] != newValue {
		t.Fatalf("New value at found index incorrect: expected %q, got %q", newValue, dht.slots[index])
	}
}

// MultiHashTable
func TestMultiHashTableBasics(t *testing.T) {
	mht := NewMultiHashTable(17, 3)

	if mht.Size() != 17 {
		t.Fatalf("Initial size should be 17, got %d", mht.Size())
	}

	if mht.Count() != 0 {
		t.Fatalf("Initial count should be 0, got %d", mht.Count())
	}

	index := mht.Put("hello")
	if index == -1 {
		t.Fatalf("Put failed")
	}

	found := mht.Find("hello")
	if found == -1 {
		t.Fatalf("Find failed for inserted value")
	}

	if found != index {
		t.Fatalf("Find returned different index: expected %d, got %d", index, found)
	}

	if mht.Find("world") != -1 {
		t.Fatalf("Find should return -1 for non-existent value")
	}

	if mht.Count() != 1 {
		t.Fatalf("Count should be 1, got %d", mht.Count())
	}
}

func TestHashingAnalyzes(t *testing.T) {
	// Сравнение Double Hashing vs Linear Probing
	// Double hashing должен показать меньше коллизий в среднем

	t.Logf("\n>>> COMPARATIVE ANALYSIS: Double Hashing vs Linear Probing <<<\n")

	testValues := make([]string, 1550)
	for i := range testValues {
		testValues[i] = fmt.Sprintf("value%d", i+1)
	}

	// DOUBLE HASHING
	mht := NewMultiHashTable(1700, 3)
	mht.ResetStats()

	startDouble := time.Now()
	for _, val := range testValues {
		mht.Put(val)
	}
	durationDouble := time.Since(startDouble)

	t.Logf("DOUBLE HASHING (MultiHashTable):")
	t.Logf("  Size: %d, Count: %d, LoadFactor: %.2f%%",
		mht.Size(), mht.Count(), mht.LoadFactor()*100)
	t.Logf("  Collisions: %d, TotalProbes: %d, AvgProbeDepth: %.2f",
		mht.CollisionCount(), mht.ProbeStats(), mht.AverageProbeDepth())
	t.Logf("  Execution time: %v", durationDouble)

	// LINEAR PROBING
	dht := NewDynamicHashTable(1700, 3)

	startLinear := time.Now()
	for _, val := range testValues {
		dht.Put(val)
	}
	durationLinear := time.Since(startLinear)

	t.Logf("\nLINEAR PROBING (DynamicHashTable):")
	t.Logf("  Size: %d, Count: %d, LoadFactor: %.2f%%",
		dht.Size(), dht.Count(), dht.LoadFactor()*100)
	t.Logf("  Collisions: %d, TotalProbes: %d, AvgProbeDepth: %.2f",
		dht.CollisionCount(), dht.ProbeStats(), dht.AverageProbeDepth())
	t.Logf("  Execution time: %v", durationLinear)
}
