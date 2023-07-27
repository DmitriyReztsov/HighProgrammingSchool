import random

from lessons.ads.native_cache import NativeCache


def test_native_cache_put():
    cache = NativeCache(5)
    cache.put("1", "value")
    assert "1" in cache.slots
    assert "value" in cache.values
    assert 1 in cache.hits

    assert cache.slots.index("1") == cache.values.index("value") == cache.hits.index(1)

    cache.put("2", "value2")
    cache.put("1", "value")
    assert cache.hits[(cache.slots.index("1"))] == 2

    for _ in range(5):
        inp = random.randint(1, 10)
        cache.put(str(inp), f"value{inp}")

    free_num = [i for i in range(10) if str(i) not in cache.slots][0]
