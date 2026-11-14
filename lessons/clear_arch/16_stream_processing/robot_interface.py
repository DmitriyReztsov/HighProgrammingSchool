from dataclasses import dataclass
from collections.abc import Callable


RobotMessage = str
RobotTransfer = Callable[[RobotMessage], None]
RobotStateView = tuple[float, float, int, int]


# запросы, которые будут обрабатываться в процессорах
@dataclass(frozen=True)
class MoveRequested:
    distance: float


@dataclass(frozen=True)
class TurnRequested:
    angle: float


@dataclass(frozen=True)
class SetEquipmentRequested:
    equipment: str


@dataclass(frozen=True)
class StartRequested:
    pass


@dataclass(frozen=True)
class StopRequested:
    pass


# результаты, генерируют процессоры
# new_state - сохранение состояния робота. Чтобы не восстанавливать расчетом
@dataclass(frozen=True)
class RobotMoved:
    distance: float
    new_state: RobotStateView


@dataclass(frozen=True)
class RobotTurned:
    angle: float
    new_state: RobotStateView


@dataclass(frozen=True)
class EquipmentChanged:
    equipment: str
    new_state: RobotStateView


@dataclass(frozen=True)
class CleaningStarted:
    equipment: str


@dataclass(frozen=True)
class CleaningStopped:
    pass


# как пример для бизнес-логики
@dataclass(frozen=True)
class RequestFailed:
    reason: str
