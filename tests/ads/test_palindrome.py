from lessons.ads.palindrome import is_palindrome


def test_palindrome():
    assert is_palindrome("asddsa") is True
    assert is_palindrome("aasddsa") is False
    assert is_palindrome("asd dsa") is True
