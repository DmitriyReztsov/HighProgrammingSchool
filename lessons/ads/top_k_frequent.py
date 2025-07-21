import heapq
from collections import defaultdict


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        frq_dict = defaultdict(int)

        for n in nums:
            frq_dict[n] += 1

        most_frq_heap = []
        for value, priority in frq_dict.items():
            heapq.heappush(most_frq_heap, (-priority, value))

        return_list = []
        for _ in range(k):
            most_frq = heapq.heappop(most_frq_heap)
            return_list.append(most_frq[1])

        return return_list


if __name__ == "__main__":
    # nums = [1, 1, 1, 2, 2, 3]
    # k = 2
    nums = [-1, -1]
    k = 1

    p = Solution().topKFrequent(nums, k)
    print(p)
