from lessons.ads2.heap import Heap


def test_make():
    input_list = [11, 9, 4, 7, 8, 3, 1, 2, 5, 6]
    heap = Heap()

    heap.MakeHeap(input_list, 3)
    assert heap.HeapArray[0] == 11
    assert heap.HeapArray[1] == 9


def test_get_max():
    heap = Heap()

    input_list = []
    heap.MakeHeap(input_list, 2)
    assert heap.GetMax() == -1

    input_list = [10, 2, 5, 30]
    heap.MakeHeap(input_list, 1)
    assert heap.GetMax() == 10  # поскольку 30 окажется за пределами кучи при формировании

    input_list = [1, 2, 3, 4, 5, 11, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    heap.MakeHeap(input_list, 4)
    assert heap.GetMax() == 15
    assert heap.GetMax() == 14
    assert heap.GetMax() == 13
    assert heap.GetMax() == 12
    assert heap.GetMax() == 11
    assert heap.GetMax() == 11
    assert heap.GetMax() == 10
    assert heap.GetMax() == 9
    assert heap.GetMax() == 8
    assert heap.GetMax() == 7
    assert heap.GetMax() == 6
    assert heap.GetMax() == 5
    assert heap.GetMax() == 4
    assert heap.GetMax() == 3
    assert heap.GetMax() == 2
    assert heap.GetMax() == 1
    assert heap.GetMax() == -1
    assert heap.GetMax() == -1

    input_list = [110, 90, 40, 70, 80, 30, 10, 20, 50, 60, 65, 31, 29, 11, 9]
    heap.MakeHeap(input_list, 3)
    assert heap.GetMax() == 110