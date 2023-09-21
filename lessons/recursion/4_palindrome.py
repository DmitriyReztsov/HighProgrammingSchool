def is_palindrome(string: str) -> bool:
    if len(string) <= 1:
        return True
    if string[0] != string[-1]:
        return False
    return True and is_palindrome(string[1:-1])
