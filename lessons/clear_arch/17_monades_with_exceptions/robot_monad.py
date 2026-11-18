from functools import wraps
from collections import namedtuple
import math

RobotState = namedtuple("RobotState", "x y angle state")


WATER = 1
SOAP = 2
BRUSH = 3


class MoveResponse:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"


class SetStateResponse:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"


class StateMonad:
    def __init__(self, state, log=None, error=None):
        self.state = state
        self.log = log or []
        self.error = error

    def bind(self, func):
        if self.error:
            return StateMonad(self.state, self.log, self.error)

        new_state, new_log, new_error = func(self.state, self.log)
        return StateMonad(new_state, new_log, self.error or new_error)


def move(dist):
    def inner(old_state, log):
        angle_rads = old_state.angle * (math.pi / 180.0)
        new_x = old_state.x + dist * math.cos(angle_rads)
        new_y = old_state.y + dist * math.sin(angle_rads)
        new_x, new_y, error = check_position(new_x, new_y)

        new_state = RobotState(
            new_x,
            new_y,
            old_state.angle,
            old_state.state,
        )
        return (
            new_state,
            log + [f"POS({int(new_state.x)},{int(new_state.y)})"],
            error if error != MoveResponse.OK else None
        )

    return inner


def turn(angle):
    def inner(old_state, log):
        new_state = RobotState(
            old_state.x, old_state.y, old_state.angle + angle, old_state.state
        )
        return new_state, log + [f"ANGLE {new_state.angle}"], None

    return inner


def set_state(new_mode):
    def inner(old_state, log):
        error = check_resources(new_mode)
        new_state = RobotState(old_state.x, old_state.y, old_state.angle, new_mode)
        return new_state, log + [f"STATE {new_mode}"], error if error != SetStateResponse.OK else None

    return inner


def start(old_state, log):
    return old_state, log + ["START"], None


def stop(old_state, log):
    return old_state, log + ["STOP"], None


def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))

    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)
    return (constrained_x, constrained_y, MoveResponse.BARRIER)


def check_resources(new_mode: int) -> SetStateResponse:
    if new_mode == WATER:
        # ....
        return SetStateResponse.NO_WATER
    elif new_mode == SOAP:
        # ....
        return SetStateResponse.NO_SOAP
    return SetStateResponse.OK
