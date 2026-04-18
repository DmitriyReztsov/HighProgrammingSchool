// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import (
	"testing"
)

func TestNativeCache(t *testing.T) {
	nc := Init[string](4)
	collisionKeys := []string{",", "=", "N", "_", "p", ")z", ":z", "Kz"} // все должны дать 10 на выходе хэш-функции

	keysValuesFrequents := []struct {
		key   string
		value string
		freq  int
	}{
		{collisionKeys[0], "val1", 2},
		{collisionKeys[1], "val2", 3},
		{collisionKeys[2], "val3", 5},
		{collisionKeys[3], "val4", 1},
	}

	for _, kv := range keysValuesFrequents {
		nc.Put(kv.key, kv.value)
	}

	for _, kvf := range keysValuesFrequents {
		for i := 0; i < kvf.freq; i++ {
			cachedVal, err := nc.Get(kvf.key)

			if err != nil {
				t.Errorf("Not expected error on key %s, value %s", kvf.key, kvf.value)
			}
			if cachedVal != kvf.value {
				t.Errorf("Wrong value on key %s, expected value %s, actual value %s", kvf.key, kvf.value, cachedVal)
			}
		}
	}

	nc.Put(collisionKeys[4], "val5")
	nc.Get(collisionKeys[4])
	nc.Get(collisionKeys[4])
	cachedVal, err := nc.Get(collisionKeys[4])

	if err != nil {
		t.Errorf("Not expected error on key %s, value %s", collisionKeys[4], "val5")
	}
	if cachedVal != "val5" {
		t.Errorf("Wrong value on key %s, expected value %s, actual value %s", collisionKeys[4], "val5", cachedVal)
	}
}
