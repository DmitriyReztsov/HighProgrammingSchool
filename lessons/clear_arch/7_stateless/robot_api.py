from collections import namedtuple
from collections.abc import Callable
from enum import Enum
import math


RobotState = namedtuple("RobotState", "x y angle state")


class Equipment(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"


def calculate_new_position(x: float, y:float, azimuth: float, distance: float) -> None:
        angle = math.radians(azimuth)
        x += distance * math.sin(angle)
        y += distance * math.cos(angle)
        return x, y


class RobotAPI:
    def __init__(self):
        self.robot = get_robot_from_fabric()

    def get_robot_transfer(self) -> Callable:
        return self.robot.func

    def perform_action(self, command: str, robot: RobotState) -> RobotState:
        return self.robot.perform_action(command, robot)

    def get_commands(self) -> list:
        return [
            "move dist",
            "turn turn_angle",
            "set_state new_internal_equipment",
            "start",
            "stop",
        ]

    def get_equipments(self) -> list:
        return [
            "water",
            "soap",
            "brush",
        ]


def transfer_to_cleaner(message: str) -> None:
        print (message)


class Robot:
    def __init__(self, transfer_to_cleaner: Callable):
        self.func = transfer_to_cleaner

    def perform_action(self, cmd: str, robot: RobotState) -> RobotState:
        match cmd.split():
            case ["move", distance]:
                return self._move(float(distance), robot)
            case ["turn", angle]:
                return self._turn(float(angle), robot)
            case ["set", equipment]:
                try:
                    equipment_enum = Equipment(equipment)
                    return self._set(equipment_enum, robot)
                except ValueError:
                    print("Неизвестное оборудование")
            case ["start"]:
                return self._start(robot)
            case ["stop"]:
                return self._stop(robot)
            case _:
                print("Неизвестная команда")

    def _move(self, distance: float, robot: RobotState) -> RobotState:
        x, y = calculate_new_position(robot.x, robot.y, robot.angle, distance)
        self.func(f"POS {x} {y}")
        return RobotState(x, y, robot.angle, robot.state)

    def _turn(self, angle: float, robot: RobotState) -> RobotState:
        azimuth = robot.angle + angle
        self.func(f"ANGLE {azimuth}")
        return RobotState(robot.x, robot.y, azimuth, robot.state)

    def _set(self, equipment: Equipment, robot: RobotState) -> RobotState:
        self.func(f"STATE {equipment.value}")
        return RobotState(robot.x, robot.y, robot.angle, equipment)

    def _start(self, robot: RobotState) -> RobotState:
        if robot.state is None:
            self.func("NO STATE SET")
        else:
            self.func(f"START WITH {robot.state.value}")
        return robot

    def _stop(self, robot: RobotState) -> RobotState:
        self.func("STOP")
        return robot


def get_robot_from_fabric():
    return Robot(transfer_to_cleaner)
