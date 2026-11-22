from robot_api import RobotApi
from robot_interface import Command, RobotStateView


class RobotInterpreter:
    def __init__(self):
        self.robot_api = RobotApi()

    def interpret(self, program: Command, robot_init: RobotStateView) -> RobotStateView:
        return program.interpret(self.robot_api, robot_init)


robot_interpreter = RobotInterpreter()
