from lessons.ads.Bloom_filter import BloomFilter


def test_add():
    bloom_filter = BloomFilter(32)
    char_set = [chr(c) for c in range(48, 58)]
    start_ind = 0
    for _ in range(10):
        str1 = ""
        for i in range(start_ind, start_ind + 10):
            str1 += char_set[i % 10]
        bloom_filter.add(str1)
        start_ind += 1
    assert bloom_filter.is_value("0123456789") is True
    assert bloom_filter.is_value("01234567890") is False
