from lessons.ads.brackets import brackets_are_correct


def test_brackets():
    brackets = "(()((())()))"
    result = brackets_are_correct(brackets)

    assert result == True
