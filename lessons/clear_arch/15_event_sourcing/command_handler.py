from typing import Callable

from event_storage import EVENT_STORAGE
from robot_interface import CommandBase, EventType, RobotStateView
import pure_robot 


class RobotCommand(CommandBase):
    def __init__(self, api_func: Callable):
        self.api_func = api_func

    def execute(self, robot: RobotStateView, arg: float | str | None = None):
        self._calculate_state(pure_robot.transfer_to_cleaner, robot, arg)

    def calculate_state(self, robot: RobotStateView, arg: float | str | None = None) -> RobotStateView:
        return self._calculate_state(self._dummy_transfer, robot, arg)

    def _dummy_transfer(self, *args, **kwargs) -> None:
        pass

    def _calculate_state(
        self, transfer: Callable, state: RobotStateView, arg: int | float | str | None = None
    ) -> RobotStateView:
        if arg is None:
            return self.api_func(transfer, state)
        return self.api_func(transfer, arg, state)


class CommandHandler:
    def __init__(self, robot_api: Callable):
        self.move_robot_cmd = RobotCommand(robot_api.move)
        self.turn_robot_cmd = RobotCommand(robot_api.turn)
        self.set_state_robot_cmd = RobotCommand(robot_api.set_state)
        self.start_robot_cmd = RobotCommand(robot_api.start)
        self.stop_robot_cmd = RobotCommand(robot_api.stop)

    def handle(self, init_robot: RobotStateView, command_str: str) -> None:
        cmd = command_str.split(" ")
        if cmd[0] == "move":
            self.move_robot(init_robot, int(cmd[1]))
        elif cmd[0] == "turn":
            self.turn_robot(init_robot, int(cmd[1]))
        elif cmd[0] == "set":
            self.set_state_robot(init_robot, cmd[1])
        elif cmd[0] == "start":
            self.start_robot(init_robot)
        elif cmd[0] == "stop":
            self.stop_robot(init_robot)
        else:
            raise ValueError("Unknown command")

    def _restore_robot(self, init_robot: RobotStateView) -> RobotStateView:
        robot = init_robot
        for event in EVENT_STORAGE:
            if event.event == "move":
                robot = self.move_robot_cmd.calculate_state(robot, event.arg)
            elif event.event == "turn":
                robot = self.turn_robot_cmd.calculate_state(robot, event.arg)
            elif event.event == "set":
                robot = self.set_state_robot_cmd.calculate_state(robot, event.arg)
            elif event.event == "start":
                robot = self.start_robot_cmd.calculate_state(robot)
            elif event.event == "stop":
                robot = self.stop_robot_cmd.calculate_state(robot)

        return robot

    def move_robot(self, init_robot: RobotStateView, dist: float) -> None:
        current_robot = self._restore_robot(init_robot)
        self.move_robot_cmd.execute(current_robot, dist)
        EVENT_STORAGE.append(EventType("move", dist))

    def turn_robot(self, init_robot: RobotStateView, angle: float) -> None:
        current_robot = self._restore_robot(init_robot)
        self.turn_robot_cmd.execute(current_robot, angle)
        EVENT_STORAGE.append(EventType("turn", angle))

    def set_state_robot(self, init_robot: RobotStateView, equipment: str) -> None:
        current_robot = self._restore_robot(init_robot)
        self.set_state_robot_cmd.execute(current_robot, equipment)
        EVENT_STORAGE.append(EventType("set", equipment))

    def start_robot(self, init_robot: RobotStateView) -> None:
        current_robot = self._restore_robot(init_robot)
        self.start_robot_cmd.execute(current_robot)
        EVENT_STORAGE.append(EventType("start", None))

    def stop_robot(self, init_robot: RobotStateView) -> None:
        current_robot = self._restore_robot(init_robot)
        self.stop_robot_cmd.execute(current_robot)
        EVENT_STORAGE.append(EventType("stop", None))


command_handler = CommandHandler(pure_robot)
