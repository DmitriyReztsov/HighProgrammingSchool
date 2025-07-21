class Solution:
    digit_letters_map = {
        "1": (),
        "2": ("a", "b", "c"),
        "3": ("d", "e", "f"),
        "4": ("g", "h", "i"),
        "5": ("j", "k", "l"),
        "6": ("m", "n", "o"),
        "7": ("p", "q", "r", "s"),
        "8": ("t", "u", "v"),
        "9": ("w", "x", "y", "z"),
        "0": (" "),
    }

    def __init__(self):
        self.result = []

    def _combine_letters(self, digits: str, dig_chars: list) -> None:
        # dig_chars = [["a"], ["b"], ["c"]]
        if digits:
            extended_dig_char = []
            dig_first = digits[0]
            for chr in self.digit_letters_map[dig_first]:
                for chars in dig_chars:
                    # new_chars = chars.append(chr)
                    extended_dig_char.append(chars + [chr])
            self._combine_letters(digits[1:], extended_dig_char)
        else:
            self.result.extend(dig_chars)
        return

    def letterCombinations(self, digits: str) -> list[str]:
        if digits:
            dig_first = digits[0]
            dig_chars = []
            for chr in self.digit_letters_map[dig_first]:
                dig_chars.append([chr])
            self._combine_letters(digits[1:], dig_chars)
        return self.trim_result()

    def trim_result(self):
        trimmed_result = []
        for combi in self.result:
            trimmed_result.append("".join(combi))
        return trimmed_result


if __name__ == "__main__":
    # digits = "23"
    digits = "2"
    print(Solution().letterCombinations(digits))
