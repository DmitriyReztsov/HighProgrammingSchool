from pymonad.state import State
from pymonad.tools import curry


"""
Задача: моделирование движения робота по сетке координат в соответствии с программой движения.
Описание: Робот получает список команд типа [("up", 2), ("up", 1), ("left", 5)]. Стартует с координат (0, 0).
Рассчитаем его конечное положение.

Состояние (State): (x, y) координаты робота.
Каждая команда обновляет состояние.
Результат выполнения команды - запись в стек вызовов.

"""

robot_state = State.insert([])  # initial value of result, commands stack in this case


@curry(2)
def perform_command(command: tuple[str, int], command_stack: list[tuple]) -> State:
    def compute_new_position(position: tuple[int, int]) -> tuple[list, tuple[int, int]]:
        stack = command_stack + [command]
        match command:
            case "up", steps:
                return stack, (position[0], position[1] + steps)
            case "down", steps:
                return stack, (position[0], position[1] - steps)
            case "right", steps:
                return stack, (position[0] + steps, position[1])
            case "left", steps:
                return stack, (position[0] - steps, position[1])

    return State(compute_new_position)


command_list = [("up", 2), ("up", 1), ("left", 5)]
robot_movements = robot_state

for command in command_list:
    robot_movements = robot_movements.then(perform_command(command))

print(robot_movements.run((0, 0)))  # запуск с первоначального состояния
# поведение повторилось, т.е. состояние не запоминается, важно только начальное состояние
# и последовательность его изменений
print(robot_movements.run((0, 0)))

command_list = [("up", 2), ("up", 1), ("left", 5), ("down", 5), ("right", 10), ("up", 2), ("left", 5)]
# необходимо сбросить состояние, иначе новые команды будут ДОБАВЛЕНЫ к уже занесенным в предыдущем цикле
robot_movements = robot_state

for command in command_list:
    robot_movements = robot_movements.then(perform_command(command))

print(robot_movements.run((0, 0)))  # должен вернуться в 0
