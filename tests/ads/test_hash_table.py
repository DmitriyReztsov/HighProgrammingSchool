from lessons.ads.hash_table import HashTable


def test_put():
    table = HashTable(19, 3)
    chr_id = 97
    cont = True
    while cont is not None:
        cont = table.put(chr(chr_id))
        chr_id += 1
    assert None not in table.slots


def test_seek_slot():
    table = HashTable(19, 3)
    for i in range(97, 107):
        cont = table.put(chr(i))

    slot = table.seek_slot(chr(i))  # the same as the last inserted item
    assert slot is not None
    assert slot == 14  # it shows on 11th element and add step= 3

    slot = table.seek_slot(chr(i + 1))
    assert slot == 12


def test_find():
    table = HashTable(19, 3)
    for i in range(97, 107):
        cont = table.put(chr(i))

    slot = table.find(chr(i - 2))
    assert slot is not None
    assert slot == cont - 2

    slot = table.find(chr(i + 2))
    assert slot is None
