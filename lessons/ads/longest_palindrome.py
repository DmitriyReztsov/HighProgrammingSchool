class Solution:
    def longestPalindrome(self, s: str) -> str:
        length_subtr = (1, s[0])
        for cursor in range(len(s)):
            cursor_left = cursor - 1
            while cursor_left >= 0 and s[cursor_left] == s[cursor]:
                if length_subtr[0] < len(s[cursor_left:cursor+1]):
                    length_subtr = (
                        len(s[cursor_left:cursor+1]),
                        s[cursor_left:cursor+1]
                    )
                cursor_left -= 1

            cursor_right = cursor + 1
            while (
                cursor_left >= 0
                and cursor_right < len(s)
                and s[cursor_left] == s[cursor_right]
            ):
                if length_subtr[0] < len(s[cursor_left:cursor_right+1]):
                    length_subtr = (
                        len(s[cursor_left:cursor_right+1]),
                        s[cursor_left:cursor_right+1]
                    )
                cursor_left -= 1
                cursor_right += 1

        return length_subtr[1]


if __name__ == "__main__":
    # s = "babad"
    # s = "cbbd"
    # s = "aaaa"
    # s = "baccab"
    # s = "ccc"
    s = "xaabacxcabaaxcabaax"
    print(Solution().longestPalindrome(s))
