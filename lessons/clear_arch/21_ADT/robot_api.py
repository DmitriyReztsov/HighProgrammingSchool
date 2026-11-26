from robot_atd import Robot
from robot_interface import RobotApiProtocol, RobotATD


class RobotApi(RobotApiProtocol):
    def make(self, command: str) -> None:
        cmd = command.split(" ")
        if cmd[0] == "move":
            self._robot.move(int(cmd[1]))
        elif cmd[0] == "turn":
            self._robot.turn(int(cmd[1]))
        elif cmd[0] == "set":
            self._robot.set_state(cmd[1])
        elif cmd[0] == "start":
            self._robot.start()
        elif cmd[0] == "stop":
            self._robot.stop()

    def _create_robot(self) -> RobotATD:
        return Robot()
