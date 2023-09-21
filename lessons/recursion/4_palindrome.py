def is_palindrome(string: str) -> bool:
    if len(string) <= 1:
        return True
    if string[0] != string[-1]:
        return False
    string = string.replace(string[0],"").replace(string[-1], "")
    return is_palindrome(string)
