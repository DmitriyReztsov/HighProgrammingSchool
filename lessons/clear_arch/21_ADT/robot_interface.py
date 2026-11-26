from dataclasses import dataclass
from typing import Protocol

RobotMessage = str


@dataclass(frozen=True)
class RobotState:
    x: float
    y: float
    angle: float
    state: str


class RobotATD(Protocol):
    def __init__(self):
        self._robot_state: RobotState = ...

    def move(self, distance: float) -> "RobotATD":
        ...

    def turn(self, angle: float) -> "RobotATD":
        ...

    def set_state(self, new_state: str) -> "RobotATD":
        ...

    def start(self) -> "RobotATD":
        ...

    def stop(self) -> "RobotATD":
        ...


class RobotApiProtocol(Protocol):
    def __init__(self) -> None:
        self._robot: RobotATD = self._create_robot()

    def make(self, command: str) -> None:
        ...

    def _create_robot(self) -> RobotATD:
        ...
