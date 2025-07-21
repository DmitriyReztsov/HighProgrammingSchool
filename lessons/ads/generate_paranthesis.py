class Solution:
    OPEN_P = "("
    CLOSE_P = ")"

    def _gen_p(
        self,
        parant_count: int,
        open_count: int,
        close_count: int,
        combi: str
    ):
        if open_count == parant_count and close_count == parant_count:
            self.result.append(combi)
            return

        if open_count < parant_count:
            self._gen_p(
                parant_count, open_count + 1, close_count, combi+self.OPEN_P
            )

        if close_count < open_count:
            self._gen_p(
                parant_count, open_count, close_count + 1, combi+self.CLOSE_P
            )

    def generateParenthesis(self, n: int) -> list[str]:
        self.result = []
        self._gen_p(n, 0, 0, "")
        return self.result


if __name__ == "__main__":
    n = 3

    p = Solution().generateParenthesis(n)
    print(p)
