from collections.abc import Callable

from .equipment import Equipment
from .position import Position
from .robot_operations import perform_command


class Robot:
    def __init__(
            self,
            perform_func: Callable,
            x: float = 0,
            y: float = 0,
            direction: float = 0,
            state: Equipment | None = None
        ):
        self.perform_func = perform_func
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
        self.perform_func("POS", self.pos.x, self.pos.y)

    def _turn(self, angle: float) -> None:
        self.azimuth += angle
        self.perform_func("ANGLE", self.azimuth)

    def _set(self, equipment: Equipment) -> None:
        self.state = equipment
        self.perform_func("STATE", equipment.value)

    def _start(self) -> None:
        if self.state is None:
            self.perform_func("NO STATE SET")
        else:
            self.perform_func("START WITH", self.state.value)

    def _stop(self) -> None:
        self.perform_func("STOP")

robot = Robot(perform_func=perform_command)