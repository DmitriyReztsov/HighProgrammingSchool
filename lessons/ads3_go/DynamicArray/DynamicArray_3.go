// for testing the file name must support Go format like ..._test.go
// rename if it's needed
package main

import "testing"

func TestGetItem(t *testing.T) {
	da := &DynArray[int]{}
	da.Init()
	da.array = []int{1, 2, 3, 4, 5}
	da.count = len(da.array)

	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}

	elem, err := da.GetItem(0)
	if elem != 1 {
		t.Fatalf("Expected ind 0 value 1, got %d", elem)
	}
	if err != nil {
		t.Fatalf("Expected ind 0 error nil")
	}

	elem, err = da.GetItem(-1)
	if err == nil {
		t.Fatalf("Expected error for -1 index")
	}

	elem, err = da.GetItem(5)
	if elem != 0 {
		t.Fatalf("Expected ind 5 value zero, got %d", elem)
	}
	if err == nil {
		t.Fatalf("Expected error out of range")
	}

	// for string
	da2 := &DynArray[string]{}
	da2.Init()
	da2.array = []string{"1", "2", "3", "4", "5"}
	da2.count = len(da2.array)

	if da2.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}

	elem2, err2 := da2.GetItem(0)
	if elem2 != "1" {
		t.Fatalf("Expected ind 0 value '1', got %s", elem2)
	}
	if err2 != nil {
		t.Fatalf("Expected ind 0 error nil")
	}

	elem2, err2 = da2.GetItem(-1)
	if err2 == nil {
		t.Fatalf("Expected error for -1 index")
	}

	elem2, err2 = da2.GetItem(5)
	if elem2 != "" {
		t.Fatalf("Expected ind 5 value zero, got %s", elem2)
	}
	if err2 == nil {
		t.Fatalf("Expected error out of range")
	}
}

func TestAppend(t *testing.T) {
	da := &DynArray[int]{}
	da.Init()
	da.Append(1)

	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}

	count := da.count
	if count != 1 {
		t.Errorf("Expected count 1, got %d", count)
	}
	lastElem, err := da.GetItem(da.count - 1)
	if err != nil || lastElem != 1 {
		t.Errorf("Expected err == nil and lastElem == 1, got %d", lastElem)
	}

	for i := range 15 {
		da.Append(i + 2)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}
	if da.array[15] != 16 {
		t.Fatalf("Expected the last element 16, got %d", da.array[15])
	}

	da.Append(17)
	if da.capacity != 32 {
		t.Fatalf("Expected capacity of the array 32, got %d", da.capacity)
	}
	if da.array[16] != 17 {
		t.Fatalf("Expected the last element 17, got %d", da.array[16])
	}
	if da.count != 17 {
		t.Fatalf("Expected count of the array 17, got %d", da.count)
	}

}

func TestInsert(t *testing.T) {
	da := &DynArray[int]{}
	da.Init()
	da.array = []int{1, 2, 3, 4, 5}
	da.count = len(da.array)

	count := da.count
	if count != 5 {
		t.Errorf("Expected count 5, got %d", count)
	}

	err := da.Insert(11, 0)
	if err != nil {
		t.Errorf("Expected Insert with nil error")
	}
	count = da.count
	if count != 6 {
		t.Errorf("Expected count 6, got %d", count)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}
	if da.array[0] != 11 {
		t.Fatalf("Expected the 0 element 11, got %d", da.array[0])
	}

	err = da.Insert(55, 6)
	if err != nil {
		t.Errorf("Expected Insert with nil error")
	}
	count = da.count
	if count != 7 {
		t.Errorf("Expected count 7, got %d", count)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}
	if da.array[6] != 55 {
		t.Fatalf("Expected the 6 element 55, got %d", da.array[6])
	}

	err = da.Insert(33, 3)
	if err != nil {
		t.Errorf("Expected Insert with nil error")
	}
	count = da.count
	if count != 8 {
		t.Errorf("Expected count 8, got %d", count)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}
	if da.array[3] != 33 {
		t.Fatalf("Expected the 3 element 33, got %d", da.array[3])
	}

	err = da.Insert(33, 9)
	if err == nil {
		t.Errorf("Expected Insert with error")
	}
	count = da.count
	if count != 8 {
		t.Errorf("Expected count 8, got %d", count)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}

	err = da.Insert(33, -1)
	if err == nil {
		t.Errorf("Expected Insert with error")
	}
	count = da.count
	if count != 8 {
		t.Errorf("Expected count 8, got %d", count)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}

	for ind, val := range []int{11, 1, 2, 33, 3, 4, 5, 55} {
		if val != da.array[ind] {
			t.Fatalf("Expected value %d on index %d, got %d", val, ind, da.array[ind])
		}
	}
}

func TestRemove(t *testing.T) {
	da := &DynArray[int]{}
	da.Init()
	da.array = []int{1, 2, 3, 4, 5}
	da.count = len(da.array)

	count := da.count
	if count != 5 {
		t.Errorf("Expected count 5, got %d", count)
	}

	err := da.Remove(0)
	if err != nil {
		t.Errorf("Expected Remove with nil error")
	}
	count = da.count
	if count != 4 {
		t.Errorf("Expected count 4, got %d", count)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}
	if da.array[0] != 2 {
		t.Fatalf("Expected the 0 element 2, got %d", da.array[0])
	}

	err = da.Remove(3)
	if err != nil {
		t.Errorf("Expected Remove with nil error")
	}
	count = da.count
	if count != 3 {
		t.Errorf("Expected count 3, got %d", count)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}
	if da.array[2] != 4 {
		t.Fatalf("Expected the 2 element 4, got %d", da.array[0])
	}

	err = da.Remove(0)
	if err != nil {
		t.Errorf("Expected Remove with nil error")
	}
	count = da.count
	if count != 2 {
		t.Errorf("Expected count 2, got %d", count)
	}

	err = da.Remove(0)
	if err != nil {
		t.Errorf("Expected Remove with nil error")
	}
	count = da.count
	if count != 1 {
		t.Errorf("Expected count 1, got %d", count)
	}

	err = da.Remove(0)
	if err != nil {
		t.Errorf("Expected Remove with nil error")
	}
	count = da.count
	if count != 0 {
		t.Errorf("Expected count 0, got %d", count)
	}
	if da.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da.capacity)
	}

	err = da.Remove(0)
	if err == nil {
		t.Errorf("Expected Remove with error")
	}
	count = da.count
	if count != 0 {
		t.Errorf("Expected count 0, got %d", count)
	}

	da2 := &DynArray[int]{}
	da2.Init()
	da2.capacity = 32

	arr := []int{}
	for i := 1; i <= 32; i++ {
		arr = append(arr, i)
	}
	da2.array = arr
	da2.count = len(da2.array)

	count2 := da2.count
	if count2 != 32 {
		t.Errorf("Expected count 5, got %d", count2)
	}

	da2.Remove(31)
	da2.Remove(25)
	da2.Remove(20)
	da2.Remove(15)
	da2.Remove(10)
	da2.Remove(5)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	count2 = da2.count
	if count2 != 16 {
		t.Errorf("Expected count 16, got %d", count2)
	}
	if da2.capacity != 32 {
		t.Fatalf("Expected capacity of the array 32, got %d", da2.capacity)
	}

	da2.Remove(0)
	count2 = da2.count
	if count2 != 15 {
		t.Errorf("Expected count 15, got %d", count2)
	}
	if da2.capacity != 21 {
		t.Fatalf("Expected capacity of the array 21, got %d", da2.capacity)
	}

	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	count2 = da2.count
	if count2 != 8 {
		t.Errorf("Expected count 8, got %d", count2)
	}
	if da2.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da2.capacity)
	}

	da2.Remove(0)
	count2 = da2.count
	if count2 != 7 {
		t.Errorf("Expected count 7, got %d", count2)
	}
	if da2.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da2.capacity)
	}

	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	da2.Remove(0)
	count2 = da2.count
	if count2 != 3 {
		t.Errorf("Expected count 3, got %d", count2)
	}
	if da2.capacity != 16 {
		t.Fatalf("Expected capacity of the array 16, got %d", da2.capacity)
	}

	expectedArray := []int{29, 30, 31}
	for i := range da2.count {
		if expectedArray[i] != da2.array[i] {
			t.Fatalf("Expected %d on index %d, got %d", expectedArray[i], i, da2.array[i])
		}
	}

}

func TestNDimension(t *testing.T) {
	da := &NDimensionDynArray[int]{}
	da.Init([]int{2, 3})
	elemArr, err := da.GetItem(1)
	if err != nil {
		t.Fatalf("Expected err nil")
	}
	_, ok := elemArr.(*DynArray[any])
	if !ok {
		t.Fatalf("Expected array")
	}

	da.Append(10, 1)
	itm, er := da.GetItem(1, 0)
	if er != nil {
		t.Fatalf("Expected err nil")
	}
	if itm != 10 {
		t.Fatalf("Expected 10, got %d", itm)
	}
}
