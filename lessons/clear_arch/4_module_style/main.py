from .robot_interface import robot


def main():
    while True:
        cmd = input("Input command: ")
        robot.perform_action(cmd)
