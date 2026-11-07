from functools import reduce

from commands import compose_program_from_cmds
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

    commands = compose_program_from_cmds(cmd_list)
    reduce(lambda state, command: command.execute(state), commands, make_robot())


if __name__ == "__main__":
    main()
