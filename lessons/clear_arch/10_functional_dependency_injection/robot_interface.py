from collections.abc import Callable
from typing import Protocol

RobotMessage = str
RobotTransfer = Callable[[RobotMessage], None]
RobotStateView = tuple[float, float, int, int]


class RobotStateProtocol(Protocol):
    @property
    def x(self) -> float: ...

    @property
    def y(self) -> float: ...

    @property
    def angle(self) -> int: ...

    @property
    def state(self) -> int: ...


class RobotInterface(Protocol):
    def create_robot(self) -> RobotStateProtocol: ...

    def get_robot_transfer(self) -> RobotTransfer: ...

    def perform_action(
        self,
        transfer: RobotTransfer,
        command: str,
        robot: RobotStateProtocol,
    ) -> RobotStateProtocol: ...


class RobotAPIInterface(Protocol):
    def __init__(self, robot: RobotInterface) -> None: ...

    def create_robot(self) -> RobotStateProtocol: ...

    def get_robot_state(self, robot: RobotStateProtocol) -> RobotStateView: ...

    def get_robot_transfer(self) -> RobotTransfer: ...

    def perform_action(
        self,
        transfer: RobotTransfer,
        command: str,
        robot: RobotStateProtocol,
    ) -> RobotStateProtocol: ...

    def get_commands(self) -> list[str]: ...

    def get_equipments(self) -> list[str]: ...
