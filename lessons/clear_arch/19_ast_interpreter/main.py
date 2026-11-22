from pure_robot import make_robot
from parser import parse
from interpreter import robot_interpreter


def main():
    cmd_list = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]

    program = parse(cmd_list)
    final_state = robot_interpreter.interpret(program, make_robot())
    print(final_state)


if __name__ == "__main__":
    main()
