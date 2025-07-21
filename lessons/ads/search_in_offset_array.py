class Solution:
    def search(self, nums: list[int], target: int) -> bool:
        pivot_ind = len(nums) // 2
        pivot = nums[pivot_ind]
        left_ind = 0
        left = nums[left_ind]
        right_ind = len(nums) - 1
        right = nums[right_ind]

        while left == pivot and left_ind != pivot_ind:
            left_ind += 1
            left = nums[left_ind]

        while right == pivot and right_ind != pivot_ind:
            right_ind -= 1
            right = nums[right_ind]

        if any(x == target for x in (left, pivot, right)):
            return True

        if (
            (pivot > left and left < target < pivot)
            or (pivot < left and (target > left or target < pivot))
        ):
            # go left
            return self.search(nums[left_ind:pivot_ind], target)

        if (
            (pivot < right and pivot < target < right)
            or (pivot > right and (target > pivot or target < right))
        ):
            # go right
            return self.search(nums[pivot_ind:right_ind], target)

        return False


if __name__ == "__main__":
    nums = [2, 5, 6, 0, 0, 1, 2]
    target = 0
    # nums = [2, 2, 2, 2, 2, 1, 2]
    # target = 1
    # nums = [4, 5, 6, 7, 0, 1, 2]
    # target = 0

    p = Solution().search(nums, target)
    print(p)
