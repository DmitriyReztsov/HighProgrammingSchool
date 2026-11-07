from collections.abc import Callable
from functools import partial
from typing import Any, Protocol


RobotMessage = str
RobotTransfer = Callable[[RobotMessage], None]
RobotStateView = tuple[float, float, int, int]


class CommandBase(Protocol):
    def __init__(self, func: Callable[[Any], RobotStateView], func_args: list | None = None):
        if func_args is None:
            func_args = []
        self.func = partial(func, *func_args)

    def add_arg(self, arg: Any) -> None:
        self.func = partial(self.func, arg)

    def execute(self, state: RobotStateView) -> RobotStateView: ...
