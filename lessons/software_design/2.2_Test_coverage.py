class AverageCalculator:
    @staticmethod
    def calculate_average(numbers: list[int]) -> float:
        return sum(numbers) / len(numbers)


if __name__ == "__main__":
    calc = AverageCalculator()

    assert calc.calculate_average([1]) == 1
    assert calc.calculate_average([1, 2]) == 1.5

    # забыли проверить на пустой список, а такая реализация при calc.calculate_average([]) упадет с делением на 0
    assert calc.calculate_average([]) == 0
