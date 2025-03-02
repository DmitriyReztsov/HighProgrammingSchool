class Window:
    def __init__(self, gamer: "Gamer") -> None:
        self._gamer = gamer
        self._combinations_list: list[Combination]
        self._gamer_score: Score

        self._create_combinations_list()
        self._create_score()
        self._create_step_stack()
        self.run()

    def _create_combinations_list(self) -> None:
        ...

    def _create_score(self) -> None:
        self._gamer_score = Score(self._gamer)

    def _create_step_stack(self) -> None:
        self._step_stack = StepStack()

    def run(self) -> None:
        """команда. Создает сущности игрового поля. Запускает цикл ввод - обработка - вывод результата.
        предусловия: нет
        постусловия: нет
        """
        
        ...

    def _input_step(self):
        """предусловия: введены корректные координаты ячейки
        посусловия: создан объект Step"""
        ...

    def _start_process(self):
        """предусловия: сделан шаг
        постусловия: проведена замена значений в ячейках, проведен цикл анализа поля, нахождения комбинации,
        начисления бонуса, изменения счета, генерация новых ячеек, анализ нового поля. Новых сложившихся
        комбинаций не найдено, возвращаем управление игроку.
        """
        ...

    def _print_result(self):
        """предусловия: поле изменилось
        послусловия: выведено новое состояние игрового поля
        """
        ...


class Score:
    START_POINT = 0

    def __init__(self, gamer: "Gamer"):
        self._score = self.START_POINT
        self._gamer = gamer

    def add_points(self, points: int) -> None:
        self._score += points

    def get_score(self) -> int:
        return self._score


class Bonus:
    POINTS: int = 0

    def __init__(self):
        self._points = self.POINTS

    def bonus_behavior(self):
        """предусловия: сработала комбинация, которая привязана к данному бонусу
        постусловия: бонус поменял поле в соответствии со своим поведением"""
        ...

    def get_points(self) -> int:
        return self._points


class Combination:
    DEFAULT_BONUS: "Bonus" | None = None
    CHECK_STATUS_NULL = 0
    CHECK_STATUS_OK = 1
    CHECK_STATUS_ERR = 2

    def __init__(self):
        self._bonus = self.DEFAULT_BONUS
        self._combi_template = self._default_template
        self._check_status = self.CHECK_STATUS_NULL

    def _default_template(self):
        """функция, описывающая порядок проверки смежных ячеек
        должна быть определена в наследниках
        """
        ...

    def check_combination(self, start_cell: "Cell") -> None:
        """предусловие: передана правильная стартовая ячейка
        постусловие: статус 1 если от стартовой ячейки можно построить комбинацию, иначе - 2"""
        ...

    def get_check_status(self) -> bool:
        return self._check_status == self.CHECK_STATUS_OK

    def get_combi_bonus(self) -> "Bonus":
        return self._bonus


class HorizontalLineCombination(Combination): ...


class VerticalLineCombination(Combination): ...


class CrossCombination(Combination): ...


class PlayGround:
    GET_CELL_NULL = 0
    GET_CELL_OK = 1
    GET_CELL_ERR = 2

    def __init__(self):
        self.a1: Cell = None
        self._get_cell_status = self.GET_CELL_NULL

    def generate_playground(self):
        """предусловия: нет
        постусловия: должен сформироваться список клеток с заполненными значениями и соседями
        """
        ...

    # request
    def get_cell(self, x: str, y: int) -> "Cell":
        """предусловия: координаты находятся в диапазоне допустимых значений
        постусловия: возвращена ячейка по координатам
        """
        ...

    def get_plauground_state(self) -> list["Cell"]:
        """предусловия: поле сгенерировано
        постусловия: сформирован список с копиями ячеек по состоянию на момент запроса
        """
        ...

    # command
    def analyze_playground(self) -> None:
        """предусловия: заполненное поле
        постусловия: поле проанализировано и заполнен список найденных комбинаций
        """
        ...


class Cell:
    def __init__(self):
        self.rignt = None
        self.left = None
        self.up = None
        self.down = None
        self.value = None

    # requests
    def get_up(self) -> "Cell":
        return self.up

    def get_down(self) -> "Cell":
        return self.down

    def get_right(self) -> "Cell":
        return self.rignt

    def get_left(self) -> "Cell":
        return self.left

    def __eq__(self, other: "Cell") -> bool:
        return self.value == other.value

    def set_value(self) -> None:
        ...


class Gamer:
    DEFAULT_NAME = ""

    def __init__(self, name: str | None = None) -> None:
        self.name = name or self.DEFAULT_NAME
        self.score = 0


class Step:
    def __init__(self, cell_a: "Cell", cell_b: "Cell") -> None:
        self.cell_a = cell_a
        self.cell_b = cell_b

    def perform_step(self) -> None:
        """предусловия: введены разные соседние ячейки
        постусловия: значения в ячейках поменяны местами, запущен процесс анализа поля"""
        ...


class StepStack:
    def __init__(self):
        self._stack = []

    def add_step(self, playground_state: list["Cell"], step: "Step") -> None:
        self._stack.append((playground_state, step))

    def pop_step(self) -> "Step":
        return self._stack.pop()
