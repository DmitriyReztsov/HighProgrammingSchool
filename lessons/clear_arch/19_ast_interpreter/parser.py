import commands
from robot_interface import Command, Response


def _chain(next_node: Command):
    def next_cmd(response: Response) -> Command:
        return next_node if response.success else commands.Stop()

    return next_cmd


def parse(cmd_list: list[str]) -> Command:
    program: Command = commands.Stop()
    for line in reversed(cmd_list):
        cmd = line.split(" ")
        if cmd[0] == "move":
            program = commands.Move(int(cmd[1]), _chain(program))
        elif cmd[0] == "turn":
            program = commands.Turn(int(cmd[1]), _chain(program))
        elif cmd[0] == "set":
            program = commands.SetState(cmd[1], _chain(program))
        elif cmd[0] == "start":
            program = commands.Start(_chain(program))
        elif cmd[0] == "stop":
            program = commands.Stop()
        else:
            raise ValueError(f"unknown command: {line}")
    return program
