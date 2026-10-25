from collections.abc import Callable
from typing import Protocol

RobotMessage = str
RobotTransfer = Callable[[RobotMessage], None]
RobotStateView = tuple[float, float, int, int]


class RobotInterface(Protocol):
    def move(transfer: Callable, dist: float, state: RobotStateView):
        ...

    def turn(transfer: Callable, turn_angle: float, state: RobotStateView):
        ...

    def set_state(transfer: Callable, new_internal_state: int, state: RobotStateView):
        ...

    def start(transfer: Callable, state: RobotStateView):
        ...

    def stop(transfer: Callable, state: RobotStateView):
        ...
