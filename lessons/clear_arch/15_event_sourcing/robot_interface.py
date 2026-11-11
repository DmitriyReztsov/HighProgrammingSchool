from dataclasses import dataclass
from collections.abc import Callable
from functools import partial
from typing import Any, Protocol


RobotMessage = str
RobotTransfer = Callable[[RobotMessage], None]
RobotStateView = tuple[float, float, int, int]

@dataclass
class EventType:
    event: str
    arg: float | str


class CommandBase(Protocol):
    def execute(self): ...

    def calculate_state(self): ...
