// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import (
	"testing"
)

func TestPutNewKeys(t *testing.T) {
	dict := Init[string](16)

	testCases := []struct {
		key   string
		value string
	}{
		{"key1", "value1"},
		{"key2", "value2"},
		{"key3", "value3"},
	}

	for _, tc := range testCases {
		dict.Put(tc.key, tc.value)

		slot := dict.find(tc.key)
		if slot == -1 {
			t.Errorf("Put() failed: key %q not found after insertion", tc.key)
			continue
		}

		if !dict.occupied[slot] {
			t.Errorf("Put() failed: occupied flag not set for key %q at slot %d", tc.key, slot)
		}

		if dict.values[slot] != tc.value {
			t.Errorf("Put() failed: expected value %q, got %q for key %q", tc.value, dict.values[slot], tc.key)
		}

		if dict.slots[slot] != tc.key {
			t.Errorf("Put() failed: key name not stored correctly at slot %d", slot)
		}
	}
}

func TestPutUpdateExisting(t *testing.T) {
	dict := Init[string](16)
	key := "mykey"

	dict.Put(key, "initial_value")

	initialSlot := dict.find(key)
	if initialSlot == -1 {
		t.Fatalf("Initial Put() failed for key %q", key)
	}

	dict.Put(key, "updated_value")

	updatedSlot := dict.find(key)
	if updatedSlot == -1 {
		t.Errorf("Put() update failed: key %q not found after update", key)
	}

	if updatedSlot != initialSlot {
		t.Errorf("Put() update moved key to different slot: initial %d, updated %d", initialSlot, updatedSlot)
	}

	if dict.values[updatedSlot] != "updated_value" {
		t.Errorf("Put() update failed: expected 'updated_value', got %q", dict.values[updatedSlot])
	}

	count := 0
	for i := 0; i < dict.size; i++ {
		if dict.occupied[i] && dict.slots[i] == key {
			count++
		}
	}
	if count != 1 {
		t.Errorf("Put() update created multiple entries: found %d entries for key %q", count, key)
	}
}

func TestIsKeyExists(t *testing.T) {
	dict := Init[string](16)

	testKeys := []struct {
		key   string
		value string
	}{
		{"key1", "exists1"},
		{"key2", "exists2"},
		{"key3", "exists3"},
	}

	for _, tc := range testKeys {
		dict.Put(tc.key, tc.value)
	}

	for _, tc := range testKeys {
		if !dict.IsKey(tc.key) {
			t.Errorf("IsKey() failed: returns false for existing key %q", tc.key)
		}
	}
}

func TestIsKeyNotExists(t *testing.T) {
	dict := Init[string](16)

	dict.Put("key1", "value1")

	nonExistingKeys := []string{"nonexistent", "absent", "missing"}
	for _, key := range nonExistingKeys {
		if dict.IsKey(key) {
			t.Errorf("IsKey() failed: returns true for non-existing key %q", key)
		}
	}
}

func TestIsKeyAfterUpdate(t *testing.T) {
	dict := Init[string](16)
	key := "testkey"

	dict.Put(key, "first")
	if !dict.IsKey(key) {
		t.Errorf("IsKey() failed after initial Put()")
	}

	dict.Put(key, "second")
	if !dict.IsKey(key) {
		t.Errorf("IsKey() failed after Put() update")
	}

	if !dict.IsKey(key) {
		t.Errorf("IsKey() failed: returns false after update for key %q", key)
	}
}

func TestGetExisting(t *testing.T) {
	dict := Init[string](16)

	testCases := []struct {
		key   string
		value string
	}{
		{"key1", "value1"},
		{"key2", "value2"},
		{"key3", "value3"},
	}

	for _, tc := range testCases {
		dict.Put(tc.key, tc.value)
	}

	for _, tc := range testCases {
		val, err := dict.Get(tc.key)
		if err != nil {
			t.Errorf("Get() failed for existing key %q: %v", tc.key, err)
			continue
		}

		if val != tc.value {
			t.Errorf("Get() returned wrong value for key %q: expected %q, got %q", tc.key, tc.value, val)
		}
	}
}

func TestGetNonExisting(t *testing.T) {
	dict := Init[string](16)

	dict.Put("key1", "something")

	nonExistingKeys := []string{"nothere", "absent", "missing"}
	for _, key := range nonExistingKeys {
		val, err := dict.Get(key)
		if err == nil {
			t.Errorf("Get() failed for non-existing key %q: expected error, got none", key)
		}

		if val != "" {
			t.Errorf("Get() failed for non-existing key %q: expected zero value, got %q", key, val)
		}
	}
}

func TestGetAfterUpdate(t *testing.T) {
	dict := Init[string](16)
	key := "updatekey"

	dict.Put(key, "initial")
	val, err := dict.Get(key)
	if err != nil || val != "initial" {
		t.Errorf("Get() failed after initial Put(): expected 'initial', got %q with err %v", val, err)
	}

	dict.Put(key, "updated")
	val, err = dict.Get(key)
	if err != nil || val != "updated" {
		t.Errorf("Get() failed after update: expected 'updated', got %q with err %v", val, err)
	}

	dict.Put(key, "updated_again")
	val, err = dict.Get(key)
	if err != nil || val != "updated_again" {
		t.Errorf("Get() failed after second update: expected 'updated_again', got %q with err %v", val, err)
	}
}

func TestCollisionResolution(t *testing.T) {
	dict := Init[string](16)

	collisionKeys := []string{",", "=", "N", "_", "p", ")z", ":z", "Kz"} // все должны дать 10 на выходе хэш-функции

	keysToInsert := []struct {
		key   string
		value string
	}{
		{collisionKeys[0], "val1"},
		{collisionKeys[1], "val2"},
		{collisionKeys[2], "val3"},
		{collisionKeys[3], "val4"},
	}

	insertedIndices := make(map[string]int)

	for _, tc := range keysToInsert {
		dict.Put(tc.key, tc.value)

		slot := dict.find(tc.key)
		if slot == -1 {
			t.Errorf("Put() collision test failed: key %q not found", tc.key)
			continue
		}

		insertedIndices[tc.key] = slot

		if slot < 0 || slot >= dict.size {
			t.Errorf("Put() collision test: invalid slot %d for key %q", slot, tc.key)
		}
	}

	slotSet := make(map[int]bool)
	for key, slot := range insertedIndices {
		if slotSet[slot] {
			t.Errorf("Put() collision test: multiple keys assigned to same slot %d", slot)
		}
		slotSet[slot] = true

		if dict.slots[slot] != key {
			t.Errorf("Put() collision test: key mismatch at slot %d", slot)
		}
	}

	if len(slotSet) != len(keysToInsert) {
		t.Errorf("Put() collision test: expected %d unique slots, got %d", len(keysToInsert), len(slotSet))
	}

	for _, tc := range keysToInsert {
		val, err := dict.Get(tc.key)
		if err != nil {
			t.Errorf("Collision resolution test failed for Get(): key %q, error: %v", tc.key, err)
			continue
		}

		if val != tc.value {
			t.Errorf("Collision resolution test: for key %q, expected %q, got %q",
				tc.key, tc.value, val)
		}
	}

	for _, tc := range keysToInsert {
		if !dict.IsKey(tc.key) {
			t.Errorf("Collision resolution test: IsKey() returns false for collision key %q", tc.key)
		}
	}
}

func TestOrderedListPutNewKeys(t *testing.T) {
	dict := NewOrderedListDictionary[string, string]()

	testCases := []struct {
		key   string
		value string
	}{
		{"charlie", "value_c"},
		{"alice", "value_a"},
		{"bob", "value_b"},
	}

	for _, tc := range testCases {
		dict.Put(tc.key, tc.value)
	}

	expectedKeys := []string{"alice", "bob", "charlie"}
	if len(dict.keys) != len(expectedKeys) {
		t.Errorf("OrderedList Put() failed: expected %d keys, got %d", len(expectedKeys), len(dict.keys))
	}

	for i, expectedKey := range expectedKeys {
		if dict.keys[i] != expectedKey {
			t.Errorf("OrderedList Put() failed: key at index %d should be %q, got %q", i, expectedKey, dict.keys[i])
		}
	}

	expectedValues := []string{"value_a", "value_b", "value_c"}
	for i, expectedValue := range expectedValues {
		if dict.values[i] != expectedValue {
			t.Errorf("OrderedList Put() failed: value at index %d should be %q, got %q", i, expectedValue, dict.values[i])
		}
	}
}

func TestOrderedListPutUpdateExisting(t *testing.T) {
	dict := NewOrderedListDictionary[string, string]()
	key := "mykey"

	dict.Put(key, "initial_value")
	if len(dict.keys) != 1 {
		t.Fatalf("OrderedList Put() failed: expected 1 key, got %d", len(dict.keys))
	}

	val1, _ := dict.Get(key)
	if val1 != "initial_value" {
		t.Errorf("OrderedList Put() failed: initial value should be 'initial_value', got %q", val1)
	}

	dict.Put(key, "updated_value")

	if len(dict.keys) != 1 {
		t.Errorf("OrderedList Put() update failed: expected 1 key, got %d", len(dict.keys))
	}

	val2, _ := dict.Get(key)
	if val2 != "updated_value" {
		t.Errorf("OrderedList Put() update failed: expected 'updated_value', got %q", val2)
	}
}

func TestOrderedListIsKeyExists(t *testing.T) {
	dict := NewOrderedListDictionary[string, string]()

	testKeys := []struct {
		key   string
		value string
	}{
		{"key1", "value1"},
		{"key2", "value2"},
		{"key3", "value3"},
	}

	for _, tc := range testKeys {
		dict.Put(tc.key, tc.value)
	}

	for _, tc := range testKeys {
		if !dict.IsKey(tc.key) {
			t.Errorf("OrderedList IsKey() failed: returns false for existing key %q", tc.key)
		}
	}
}

func TestOrderedListIsKeyNotExists(t *testing.T) {
	dict := NewOrderedListDictionary[string, string]()

	dict.Put("key1", "value1")

	nonExistingKeys := []string{"nonexistent", "absent", "missing"}
	for _, key := range nonExistingKeys {
		if dict.IsKey(key) {
			t.Errorf("OrderedList IsKey() failed: returns true for non-existing key %q", key)
		}
	}
}

func TestOrderedListIsKeyAfterUpdate(t *testing.T) {
	dict := NewOrderedListDictionary[string, string]()
	key := "testkey"

	dict.Put(key, "first")
	if !dict.IsKey(key) {
		t.Errorf("OrderedList IsKey() failed after initial Put()")
	}

	dict.Put(key, "second")
	if !dict.IsKey(key) {
		t.Errorf("OrderedList IsKey() failed after Put() update")
	}
}

func TestOrderedListGetExisting(t *testing.T) {
	dict := NewOrderedListDictionary[string, string]()

	testCases := []struct {
		key   string
		value string
	}{
		{"key1", "value1"},
		{"key2", "value2"},
		{"key3", "value3"},
	}

	for _, tc := range testCases {
		dict.Put(tc.key, tc.value)
	}

	for _, tc := range testCases {
		val, err := dict.Get(tc.key)
		if err != nil {
			t.Errorf("OrderedList Get() failed for existing key %q: %v", tc.key, err)
			continue
		}

		if val != tc.value {
			t.Errorf("OrderedList Get() returned wrong value for key %q: expected %q, got %q", tc.key, tc.value, val)
		}
	}
}

func TestOrderedListGetNonExisting(t *testing.T) {
	dict := NewOrderedListDictionary[string, string]()

	dict.Put("key1", "something")

	nonExistingKeys := []string{"nothere", "absent", "missing"}
	for _, key := range nonExistingKeys {
		val, err := dict.Get(key)
		if err == nil {
			t.Errorf("OrderedList Get() failed for non-existing key %q: expected error, got none", key)
		}

		var emptyStr string
		if val != emptyStr {
			t.Errorf("OrderedList Get() failed for non-existing key %q: expected zero value, got %q", key, val)
		}
	}
}

func TestOrderedListDeleteAndOrdering(t *testing.T) {
	dict := NewOrderedListDictionary[string, string]()

	keysToInsert := []struct {
		key   string
		value string
	}{
		{"zebra", "val_z"},
		{"apple", "val_a"},
		{"mango", "val_m"},
		{"banana", "val_b"},
		{"dog", "val_d"},
	}

	for _, tc := range keysToInsert {
		dict.Put(tc.key, tc.value)
	}

	expectedOrder := []string{"apple", "banana", "dog", "mango", "zebra"}
	for i, expectedKey := range expectedOrder {
		if dict.keys[i] != expectedKey {
			t.Errorf("OrderedList ordering failed: keys[%d] should be %q, got %q", i, expectedKey, dict.keys[i])
		}
	}

	err := dict.Delete("dog")
	if err != nil {
		t.Errorf("OrderedList Delete() failed for key 'dog': %v", err)
	}

	if dict.IsKey("dog") {
		t.Errorf("OrderedList Delete() failed: key 'dog' still exists after deletion")
	}

	expectedAfterDelete := []string{"apple", "banana", "mango", "zebra"}
	if len(dict.keys) != len(expectedAfterDelete) {
		t.Errorf("OrderedList Delete() failed: expected %d keys, got %d", len(expectedAfterDelete), len(dict.keys))
	}

	for i, expectedKey := range expectedAfterDelete {
		if dict.keys[i] != expectedKey {
			t.Errorf("OrderedList ordering after delete failed: keys[%d] should be %q, got %q", i, expectedKey, dict.keys[i])
		}
	}

	val, err := dict.Get("mango")
	if err != nil || val != "val_m" {
		t.Errorf("OrderedList Get() after delete failed: expected 'val_m', got %q with err %v", val, err)
	}
}

func TestBitStringPutGetIsKey(t *testing.T) {
	d := NewBitStringDictionary[string](4)

	d.Put(0, "z0")
	d.Put(3, "z3")
	d.Put(10, "z10")

	if !d.IsKey(0) || !d.IsKey(3) || !d.IsKey(10) {
		t.Errorf("IsKey: expected true for inserted keys")
	}
	if d.IsKey(7) {
		t.Errorf("IsKey(7): expected false for empty slot")
	}

	v, err := d.Get(10)
	if err != nil || v != "z10" {
		t.Errorf("Get(10): want z10, got %q err %v", v, err)
	}
}

func TestBitStringPutUpdate(t *testing.T) {
	d := NewBitStringDictionary[string](4)

	d.Put(5, "first")
	d.Put(5, "second")
	v, err := d.Get(5)
	if err != nil || v != "second" {
		t.Errorf("after update Get(5): want second, got %q err %v", v, err)
	}
}

func TestBitStringDelete(t *testing.T) {
	d := NewBitStringDictionary[string](4)

	d.Put(2, "two")
	if err := d.Delete(2); err != nil {
		t.Fatalf("Delete: %v", err)
	}
	if d.IsKey(2) {
		t.Errorf("IsKey after Delete: expected false")
	}
	_, err := d.Get(2)
	if err == nil {
		t.Errorf("Get after Delete: expected error")
	}
	if err := d.Delete(2); err == nil {
		t.Errorf("Delete missing key: expected error")
	}
}
