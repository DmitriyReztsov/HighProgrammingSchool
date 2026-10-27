from collections.abc import Callable
from functools import partial
from typing import Any

import pure_robot
import robot_interface


class RobotApi:
    def __init__(self, executors: dict[Callable]):
        self.executors = executors
        self.cleaner_state = pure_robot.RobotState(
            0.0, 0.0, 0, pure_robot.Equipment.WATER
        )
        self._args_stack = []

    def make(self, input_str: str, state: robot_interface.RobotStateView | None):
        if not state:
            state = self.cleaner_state

        if input_str not in self.executors:
            self._args_stack.append(input_str)
            return state

        exec_func = self.executors[input_str]
        while len(self._args_stack) > 0:
            arg = self._args_stack.pop()
            try:
                arg = float(arg)
            except ValueError:
                arg = arg

            exec_func = partial(exec_func, arg)

        self.cleaner_state = exec_func(state)

        return self.cleaner_state

    def __call__(self, input_str: str, state: robot_interface.RobotStateView):
        return self.make(input_str, state)


def transfer_to_cleaner(message: robot_interface.RobotMessage) -> None:
    print(message)


def create_robot_executor(robot: robot_interface.RobotInterface, transfer: robot_interface.RobotTransfer) -> dict[Callable]:
    # подход через каррирование. Вернем словарь с частично инициированными функциями. По ключам словаря будем понимать,
    # что перед нами команда
    return {
        "move": partial(robot.move, transfer),
        "turn": partial(robot.turn, transfer),
        "set": partial(robot.set_state, transfer),
        "start": partial(robot.start, transfer),
        "stop": partial(robot.stop, transfer),
    }


executors = create_robot_executor(
    pure_robot,
    transfer_to_cleaner,
)

api = RobotApi(executors)

# executor = create_robot_executor(
#     double_pure_robot,  <--- нам нужен будет модуль, наследуемый от pure_robot с измененными фунециями / методами
#     transfer_to_cleaner,
# )

# api = RobotApi(executor)
