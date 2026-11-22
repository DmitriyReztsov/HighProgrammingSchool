from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any
from dataclasses import dataclass

RobotMessage = str
RobotTransfer = Callable[[RobotMessage], None]
RobotStateView = Any


@dataclass
class MoveResponse:
    distance: float
    success: bool


@dataclass
class TurnResponse:
    angle: float
    success: bool


@dataclass
class StateResponse:
    state: str
    success: bool


Response = MoveResponse | TurnResponse | StateResponse


class Command(ABC):
    @abstractmethod
    def interpret(self, robot, robot_state: RobotStateView) -> RobotStateView:
        ...


# продолжение: по ответу команды выбираем следующий узел AST
Next = Callable[[Response], Command]
