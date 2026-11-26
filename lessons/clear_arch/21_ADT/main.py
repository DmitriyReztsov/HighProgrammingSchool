from robot_api import RobotApi


def main():
    cmd_list = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]

    robot_api = RobotApi()
    for cmd in cmd_list:
        robot_api.make(cmd)


if __name__ == "__main__":
    main()
