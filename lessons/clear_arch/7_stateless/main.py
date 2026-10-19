# клиент робота, хранит состояние робота у себя
from robot_api import Equipment, RobotAPI, RobotState


def turn_robot_on():
    return RobotState(0.0, 0.0, 0, Equipment.WATER)


def main():
    robot = turn_robot_on()
    robot_api = RobotAPI()
    while True:
        cmd = input("Input command: ")
        robot = robot_api.perform_action(cmd, robot)


if __name__ == "__main__":
    main()
