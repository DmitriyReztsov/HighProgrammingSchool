from robot_interface import Command, Next, RobotStateView


class Move(Command):
    def __init__(self, distance: float, next_cmd: Next) -> None:
        self.distance = distance
        self.next_cmd = next_cmd

    def interpret(self, robot, robot_state: RobotStateView) -> RobotStateView:
        response, new_state = robot.move(self.distance, robot_state)
        return self.next_cmd(response).interpret(robot, new_state)


class Turn(Command):
    def __init__(self, angle: float, next_cmd: Next) -> None:
        self.angle = angle
        self.next_cmd = next_cmd

    def interpret(self, robot, robot_state: RobotStateView) -> RobotStateView:
        response, new_state = robot.turn(self.angle, robot_state)
        return self.next_cmd(response).interpret(robot, new_state)


class SetState(Command):
    def __init__(self, new_state: str, next_cmd: Next) -> None:
        self.new_state = new_state
        self.next_cmd = next_cmd

    def interpret(self, robot, robot_state: RobotStateView) -> RobotStateView:
        response, new_state = robot.set_state(self.new_state, robot_state)
        return self.next_cmd(response).interpret(robot, new_state)


class Start(Command):
    def __init__(self, next_cmd: Next) -> None:
        self.next_cmd = next_cmd

    def interpret(self, robot, robot_state: RobotStateView) -> RobotStateView:
        response, new_state = robot.start(robot_state)
        return self.next_cmd(response).interpret(robot, new_state)


class Stop(Command):
    def interpret(self, robot, robot_state: RobotStateView) -> RobotStateView:
        return robot.stop(robot_state)
