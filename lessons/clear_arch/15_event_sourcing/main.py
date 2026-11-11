from functools import reduce

from command_handler import command_handler
from pure_robot import make_robot


def main():
    cmd_list = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]

    init_robot = make_robot()
    for cmd in cmd_list:
        command_handler.handle(init_robot, cmd)


if __name__ == "__main__":
    main()
