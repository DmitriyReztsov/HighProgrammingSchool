class Solution:
    def sortColors(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        count_dict = {}
        for elem in nums:
            if elem in count_dict:
                count_dict[elem] += 1
            else:
                count_dict[elem] = 1

        cursor = 0
        for key in [0, 1, 2]:
            if key not in count_dict:
                continue

            while count_dict[key] > 0:
                nums[cursor] = key
                cursor += 1
                count_dict[key] -= 1


if __name__ == "__main__":
    nums = [2, 1, 1, 2]
    Solution().sortColors(nums)
    print(nums)
