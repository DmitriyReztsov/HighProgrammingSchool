from enum import Enum
import math
from collections import namedtuple

from robot_interface import RobotMessage, RobotStateProtocol, RobotTransfer


RobotState = namedtuple("RobotState", "x y angle state")

# режимы работы устройства очистки
class Equipment(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"


def make_robot() -> RobotState:
    return RobotState(0.0, 0.0, 0, Equipment.WATER)


# взаимодействие с роботом вынесено в отдельную функцию
def transfer_to_cleaner(message: RobotMessage) -> None:
    print (message)


# перемещение
def move(transfer,dist,state):
    angle_rads = state.angle * (math.pi/180.0)   
    new_state = RobotState(
        state.x + dist * math.cos(angle_rads),
        state.y + dist * math.sin(angle_rads),
        state.angle,
        state.state)  
    transfer(f"POS {new_state.x} {new_state.y}")
    return new_state


# поворот
def turn(transfer, turn_angle, state):
    new_state = RobotState(
        state.x,
        state.y,
        state.angle + turn_angle,
        state.state)
    transfer(f"ANGLE {new_state.angle}")
    return new_state


# установка режима работы
def set_state(transfer, new_internal_state, state):
    if new_internal_state=='water':
        self_state = Equipment.WATER  
    elif new_internal_state=='soap':
        self_state = Equipment.SOAP
    elif new_internal_state=='brush':
        self_state = Equipment.BRUSH
    else:
        return state  
    new_state = RobotState(
        state.x,
        state.y,
        state.angle,
        self_state)
    transfer(f"STATE {self_state.value}")
    return new_state


# начало чистки
def start(transfer,state):
    transfer(f"START WITH {state.state.value}")
    return state


# конец чистки
def stop(transfer,state):
    transfer("STOP")
    return state


# интерпретация набора команд
def make(
    transfer: RobotTransfer,
    code: list[str],
    state: RobotStateProtocol,
) -> RobotStateProtocol:
    for command in code:
        cmd = command.split(' ')
        if cmd[0]=='move':
            state = move(transfer,int(cmd[1]),state) 
        elif cmd[0]=='turn':
            state = turn(transfer,int(cmd[1]),state)
        elif cmd[0]=='set':
            state = set_state(transfer,cmd[1],state) 
        elif cmd[0]=='start':
            state = start(transfer,state)
        elif cmd[0]=='stop':
            state = stop(transfer,state)
    return state


def get_commands():
    return {
        "make_robot": make_robot,
        "transfer_to_cleaner": transfer_to_cleaner,
        "make": make, 
    }
