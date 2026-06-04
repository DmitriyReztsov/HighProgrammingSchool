class GradeCalculator:
    @staticmethod
    def calculate_average(grades: list[int]) -> tuple[bool, float]:
        if not isinstance(grades, list):
            return False, 0

        if len(grades) == 0:
            return False, 0

        if not all(isinstance(g, int) and not isinstance(g, bool) for g in grades):
            return False, 0

        return True, sum(grades) / len(grades)


if __name__ == "__main__":
    calc = GradeCalculator()

    assert calc.calculate_average([1]) == (True, 1.0)
    assert calc.calculate_average([1, 2]) == (True, 1.5)

    # краевые случаи
    assert calc.calculate_average([]) == (False, 0)

    # ошибочные данные
    assert calc.calculate_average(None) == (False, 0)
    assert calc.calculate_average([None, None, 1]) == (False, 0)
    assert calc.calculate_average([True, False, 1]) == (False, 0)
    assert calc.calculate_average("string") == (False, 0)
    assert calc.calculate_average(["string", "string"]) == (False, 0)

    print("All done")
