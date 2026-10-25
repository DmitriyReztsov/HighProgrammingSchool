from collections.abc import Callable
from typing import Any

import pure_robot
import robot_interface


class RobotApi:
    def __init__(self, executor):
        self.executor = executor
        self.cleaner_state = pure_robot.RobotState(
            0.0, 0.0, 0, pure_robot.Equipment.WATER
        )

    def make(self, command):
        cmd = command.split()

        if cmd[0] == "move":
            args = (int(cmd[1]),)
        elif cmd[0] == "turn":
            args = (int(cmd[1]),)
        elif cmd[0] == "set":
            args = (cmd[1],)
        elif cmd[0] in ("start", "stop"):
            args = ()
        else:
            raise ValueError(f"Unknown command: {cmd[0]}")

        self.cleaner_state = self.executor(cmd[0], *args, self.cleaner_state)

        return self.cleaner_state

    def __call__(self, command):
        return self.make(command)


def transfer_to_cleaner(message: robot_interface.RobotMessage) -> None:
    print(message)


def create_robot_executor(robot: robot_interface.RobotInterface, transfer: robot_interface.RobotTransfer) -> Callable:
    # подход через замыкания. Создадим функцию, которая уже содержит все необходимые зависимости
    # внутри замыкания и возвращает одну функцию для выполнения команд.
    # Требуется выполнение модулем, котрый передается в robot определенного согласованного интерфейса.
    operations = {
        "move": robot.move,
        "turn": robot.turn,
        "set": robot.set_state,
        "start": robot.start,
        "stop": robot.stop,
    }

    def execute(operation: dict[str, Callable], *args) -> Any:
        func = operations[operation]
        return func(transfer, *args)

    return execute


executor = create_robot_executor(
    pure_robot,
    transfer_to_cleaner,
)

api = RobotApi(executor)

# executor = create_robot_executor(
#     double_pure_robot,  <--- нам нужен будет модуль, наследуемый от pure_robot с измененными фунециями / методами
#     transfer_to_cleaner,
# )

# api = RobotApi(executor)
