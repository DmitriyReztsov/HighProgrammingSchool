from typing import Callable, TypeVar, Generic

import pure_robot
from robot_interface import RobotStateView

StateType = TypeVar("StateType")
AnyType = TypeVar("AnyType")
AnotherAnyType = TypeVar("AnotherAnyType")


# Обёртка над функцией изменения состояния
class State(Generic[StateType]):
    def __init__(self, run: Callable[[StateType], StateType]):
        self.run = run

    # Создание монады, которая возвращает значение, не меняя состояние
    @staticmethod
    def pure(value: AnyType) -> "State[StateType]":
        return State(
            lambda state: (value, state)
        )

    def bind(self, func: Callable[[], "State[StateType]"]
    ) -> "State[StateType]":

        def new_run(robot_state: RobotStateView):
            new_robot_state = self.run(robot_state)
            next_state = func()
            return next_state.run(new_robot_state)

        return State(new_run)

    def __rshift__(self, other):
        return self.bind(lambda: other)


def move(distance: float) -> State[RobotStateView]:
    return State(
        lambda robot_state: pure_robot.move(pure_robot.transfer_to_cleaner, distance, robot_state)
    )


def turn(angle: float) -> State[RobotStateView]:
    return State(
        lambda robot_state: pure_robot.turn(pure_robot.transfer_to_cleaner, angle, robot_state)
    )


def set_state(value: str) -> State[RobotStateView]:
    return State(
        lambda robot_state: pure_robot.set_state(pure_robot.transfer_to_cleaner, value, robot_state)
    )


def start() -> State[RobotStateView]:
    return State(
        lambda robot_state: pure_robot.start(pure_robot.transfer_to_cleaner, robot_state)
    )


def stop() -> State[RobotStateView]:
    return State(
        lambda robot_state: pure_robot.stop(pure_robot.transfer_to_cleaner, robot_state)
    )


def compose_program_from_cmds(cmd_list: list[str]) -> State[RobotStateView]:
    commands: list[State[RobotStateView]] = []

    for command in cmd_list:
        cmd = command.split(" ")
        match cmd:
            case "move", arg:
                commands.append(move(float(arg)))
            case "turn", arg:
                commands.append(turn(float(arg)))
            case "set", arg:
                commands.append(set_state(arg))
            case ["start"]:
                commands.append(start())
            case ["stop"]:
                commands.append(stop())

    program = commands[0]
    for command in commands[1:]:
        program = program >> command
    return program
