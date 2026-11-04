import pure_robot
from monade import compose_program_from_cmds


def main():
    cmd_list = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]

    program = compose_program_from_cmds(cmd_list)
    initial_robot_state = pure_robot.make_robot()
    program.run(initial_robot_state)


if __name__ == "__main__":
    main()