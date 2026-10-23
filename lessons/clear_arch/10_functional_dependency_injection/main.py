from collections.abc import Callable

import pure_robot
import robot_interface


def get_robot_commands(robot_type: str) -> dict[str, Callable]:
    return {
        "pure_robot": pure_robot.get_commands(),
        "other_robot": {}
    }.get(robot_type)


def robot_command_adapter(
    commands_system: dict[str, Callable], transfer: Callable, cmd: str, robot: robot_interface.RobotStateView | None
) -> robot_interface.RobotStateView:
    return commands_system["make"](transfer, [cmd], robot)



def main():
    robot_commands = get_robot_commands("pure_robot")

    robot = robot_commands.get("make_robot")()
    transfer = robot_commands.get("transfer_to_cleaner")

    while True:
        cmd = input("Input command: ")
        robot = robot_command_adapter(robot_commands, transfer, cmd, robot)


if __name__ == "__main__":
    main()
