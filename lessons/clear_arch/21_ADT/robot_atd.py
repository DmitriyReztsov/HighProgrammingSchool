import math
from enum import Enum

from robot_interface import RobotATD, RobotMessage, RobotState


class Equipment(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"


class Robot(RobotATD):
    def __init__(self, robot_state: RobotState | None = None):
        if robot_state is None:
            robot_state = RobotState(0.0, 0.0, 0, Equipment.WATER)
        self._robot_state = robot_state

    def _transfer_to_cleaner(self, message: RobotMessage) -> None:
        print(message)

    def move(self, distance: float) -> "Robot":
        angle_rads = self._robot_state.angle * (math.pi / 180.0)
        new_state = RobotState(
            self._robot_state.x + distance * math.cos(angle_rads),
            self._robot_state.y + distance * math.sin(angle_rads),
            self._robot_state.angle,
            self._robot_state.state,
        )
        self._transfer_to_cleaner(f"POS {new_state.x} {new_state.y}")
        return Robot(new_state)

    def turn(self, angle: float) -> "Robot":
        new_state = RobotState(
            self._robot_state.x,
            self._robot_state.y,
            self._robot_state.angle + angle,
            self._robot_state.state,
        )
        self._transfer_to_cleaner(f"ANGLE {new_state.angle}")
        return Robot(new_state)

    def set_state(self, new_state: str) -> "Robot":
        if new_state == "water":
            self_state = Equipment.WATER
        elif new_state == "soap":
            self_state = Equipment.SOAP
        elif new_state == "brush":
            self_state = Equipment.BRUSH
        else:
            return Robot(self._robot_state)

        new_state = RobotState(
            self._robot_state.x,
            self._robot_state.y,
            self._robot_state.angle,
            self_state,
        )
        self._transfer_to_cleaner(f"STATE {self_state.value}")
        return Robot(new_state)

    def start(self) -> "Robot":
        self._transfer_to_cleaner(f"START WITH {self._robot_state.state.value}")
        return Robot(self._robot_state)

    def stop(self) -> "Robot":
        self._transfer_to_cleaner("STOP")
        return Robot(self._robot_state)
