class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        cursor_start = 0
        cursor_end = 0
        max_length = 0
        while cursor_end <= len(s):
            if (
                len(s[cursor_start:cursor_end])
                == len(set(s[cursor_start:cursor_end]))
            ):
                max_length = max(max_length, len(s[cursor_start:cursor_end]))
                cursor_end += 1
            else:
                cursor_start += 1
                cursor_end = cursor_start
        return max_length


if __name__ == "__main__":
    # s = "abcabcbb"
    s = "bbbbb"
    # s = "pwwkew"
    # s = " "
    print(Solution().lengthOfLongestSubstring(s))
