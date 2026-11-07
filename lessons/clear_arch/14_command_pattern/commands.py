from typing import Callable

import pure_robot
from robot_interface import CommandBase, RobotStateView


class Command(CommandBase):
    def execute(self, state: RobotStateView) -> RobotStateView:
        return self.func(state)


def command_fabric_with_transfer(func: Callable, func_arg: float | str | None = None) -> CommandBase:
    if func_arg is not None:
        return Command(func=func, func_args=[pure_robot.transfer_to_cleaner, func_arg])
    return Command(func=func, func_args=[pure_robot.transfer_to_cleaner,])


def compose_program_from_cmds(cmd_list: list[str]) -> list[CommandBase]:
    commands: list[CommandBase] = []

    for command in cmd_list:
        cmd = command.split(" ")
        match cmd:
            case "move", arg:
                commands.append(command_fabric_with_transfer(pure_robot.move, float(arg)))
            case "turn", arg:
                commands.append(command_fabric_with_transfer(pure_robot.turn, float(arg)))
            case "set", arg:
                commands.append(command_fabric_with_transfer(pure_robot.set_state, arg))
            case ["start"]:
                commands.append(command_fabric_with_transfer(pure_robot.start))
            case ["stop"]:
                commands.append(command_fabric_with_transfer(pure_robot.stop))

    return commands
