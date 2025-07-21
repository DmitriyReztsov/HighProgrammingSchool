class Solution:
    def maxArea(self, height: list[int]) -> int:
        cursor_left = 0
        cursor_right = len(height) - 1
        max_capacity = 0

        while cursor_left != cursor_right:
            max_capacity = max(
                max_capacity,
                (
                    (cursor_right - cursor_left)
                    * min(height[cursor_left], height[cursor_right])
                )
            )
            if height[cursor_left] <= height[cursor_right]:
                cursor_left += 1
            elif height[cursor_left] > height[cursor_right]:
                cursor_right -= 1
        return max_capacity


if __name__ == "__main__":
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

    p = Solution().maxArea(height)
    print(p)
