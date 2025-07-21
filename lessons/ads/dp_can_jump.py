class Solution:
    def canJump(self, nums: list[int]) -> bool:
        check_array = [False] * len(nums)
        check_array[0] = True
        for i in range(len(nums)):
            if check_array[i]:
                if nums[i] >= len(nums) - 1 - i:
                    return True
                for j in range(1, nums[i] + 1):
                    if i + j < len(nums):
                        check_array[i + j] = True
                    else:
                        break

        return check_array[-1]

    def _canJump(self, nums: list[int]) -> bool:
        """Imagine you have a car, and you have some distance to travel (the
        length of the array). This car has some amount of gasoline, and as
        long as it has gasoline, it can keep traveling on this road (the
        array). Every time we move up one element in the array, we subtract
        one unit of gasoline. However, every time we find an amount of
        gasoline that is greater than our current amount, we "gas up" our car
        by replacing our current amount of gasoline with this new amount. We
        keep repeating this process until we either run out of gasoline (and
        return false), or we reach the end with just enough gasoline (or more
        to spare), in which case we return true.

        Note: We can let our gas tank get to zero as long as we are able to gas
        up at that immediate location (element in the array) that our car is
        currently at.
        """

        gas = 0
        for n in nums:
            if gas < 0:
                return False
            elif n > gas:
                gas = n
            gas -= 1

        return True


if __name__ == "__main__":
    # nums = [2, 1, 1, 2]
    # nums = [2,3,1,1,4]
    # nums = [3,2,1,0,4]
    # nums = [2,0,0]
    # nums = [2, 0]
    nums = [0]
    print(Solution().canJump(nums))
