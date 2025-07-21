class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        anagrams_dict = {}
        for word in strs:
            sorted_word = "".join(sorted(word))
            if sorted_word in anagrams_dict:
                anagrams_dict[sorted_word].append(word)
            else:
                anagrams_dict[sorted_word] = [word]
        return list(anagrams_dict.values())


if __name__ == "__main__":
    # strs = ["eat","tea","tan","ate","nat","bat"]
    # strs = [""]
    strs = ["a"]
    print(Solution().groupAnagrams(strs))
