from lessons.ads.postfix import calculate_postfix


def test_postfix():
    postfix = "8 2 + 5 * 9 + =".split()
    result = calculate_postfix(postfix)

    assert result == "59"
