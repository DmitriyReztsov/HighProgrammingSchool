def is_palindrome_by_char(string: str, left_index: int, right_index: int) -> bool:
    if left_index >= right_index:
        return True
    if string[left_index] != string[right_index]:
        return False
    return is_palindrome_by_char(string, left_index + 1, right_index - 1)


def is_palindrome(string: str) -> bool:
    right_index = len(string) - 1
    return is_palindrome_by_char(string, 0, right_index)
