from enum import Enum
from math import cos, radians, sin


class Position:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def calculate_new_position(self, azimuth: float, distance: float) -> None:
        angle = radians(azimuth)
        self.x += distance * sin(angle)
        self.y += distance * cos(angle)


class Equipment(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"


class Robot:
    def __init__(self, x: float = 0, y: float = 0, direction: float = 0, state: Equipment | None = None):
        self.pos = Position(x, y)
        self.azimuth = direction
        self.state = state

    def perform_action(self, cmd: str) -> None:
        match cmd.split():
            case ["move", distance]:
                self._move(float(distance))
            case ["turn", angle]:
                self._turn(float(angle))
            case ["set", equipment]:
                try:
                    equipment_enum = Equipment(equipment)
                    self._set(equipment_enum)
                except ValueError:
                    print("Неизвестное оборудование")
            case ["start"]:
                self._start()
            case ["stop"]:
                self._stop()
            case _:
                print("Неизвестная команда")

    def _move(self, distance: float) -> None:
        self.pos.calculate_new_position(self.azimuth, distance)
        print(f"POS {self.pos.x} {self.pos.y}")

    def _turn(self, angle: float) -> None:
        self.azimuth += angle
        print(f"ANGLE {self.azimuth}")

    def _set(self, equipment: Equipment) -> None:
        self.state = equipment
        print(f"STATE {equipment.value}")

    def _start(self) -> None:
        if self.state is None:
            print("NO STATE SET")
        else:
            print(f"START WITH {self.state.value}")

    def _stop(self) -> None:
        print("STOP")


def start(robot: Robot) -> None:
    while True:
        cmd = input("Input command: ")
        robot.perform_action(cmd)


if __name__ == "__main__":
    robot = Robot()
    start(robot)