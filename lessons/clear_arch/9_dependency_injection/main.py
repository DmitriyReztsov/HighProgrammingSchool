from hypster_architecture import PureRobotAdapter, RobotAPI


def main():
    api = RobotAPI(PureRobotAdapter())
    robot = api.create_robot()
    transfer = api.get_robot_transfer()

    while True:
        cmd = input("Input command: ")
        robot = api.perform_action(transfer, cmd, robot)


if __name__ == "__main__":
    main()
