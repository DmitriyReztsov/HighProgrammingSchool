from lessons.ads.native_dict import NativeDictionary


def test_put():
    dictionary = NativeDictionary(19)
    dictionary.put("asd", "value")
    assert "asd" in dictionary.slots
    assert "value" in dictionary.values
    assert dictionary.slots.index("asd") == dictionary.values.index("value")

    dictionary.put("dsa", "value")
    assert "dsa" in dictionary.slots
    assert dictionary.slots.index("asd") != dictionary.slots.index("dsa")

    dictionary.put("dsa", "another value")
    assert "another value" in dictionary.values
    assert dictionary.slots.index("dsa") == dictionary.values.index("another value")


def test_is_key():
    dictionary = NativeDictionary(5)
    dictionary.put("a", "value")
    dictionary.put("f", "another value")
    dictionary.put("1", 2)

    assert dictionary.is_key("a") is False  # due to collision "a":"value" was overidden by "f":"another value"
    assert dictionary.is_key("f") is True
    assert dictionary.is_key("1") is True
    assert dictionary.is_key("asd1") is False


def test_get():
    dictionary = NativeDictionary(19)
    dictionary.put("asd", "value")
    dictionary.put("dsa", "another value")
    dictionary.put("1", 2)

    assert dictionary.get("asd") == "value"
    assert dictionary.get("dsa") == "another value"
    assert dictionary.get("1") == 2
    assert dictionary.get("no key") is None
