import pure_robot
import robot_interface


class PureRobotAdapter:
    def create_robot(self) -> robot_interface.RobotStateProtocol:
        return pure_robot.make_robot()

    def get_robot_transfer(self) -> robot_interface.RobotTransfer:
        return pure_robot.transfer_to_cleaner

    def perform_action(
        self,
        transfer: robot_interface.RobotTransfer,
        command: str,
        robot: robot_interface.RobotStateProtocol,
    ) -> robot_interface.RobotStateProtocol:
        return pure_robot.make(transfer, [command], robot)


class RobotAPI:
    def __init__(self, robot: robot_interface.RobotInterface) -> None:
        self._robot = robot

    def create_robot(self) -> robot_interface.RobotStateProtocol:
        return self._robot.create_robot()

    def get_robot_state(
        self,
        robot: robot_interface.RobotStateProtocol,
    ) -> robot_interface.RobotStateView:
        return (robot.x, robot.y, robot.angle, robot.state)

    def get_robot_transfer(self) -> robot_interface.RobotTransfer:
        return self._robot.get_robot_transfer()

    def perform_action(
        self,
        transfer: robot_interface.RobotTransfer,
        command: str,
        robot: robot_interface.RobotStateProtocol,
    ) -> robot_interface.RobotStateProtocol:
        return self._robot.perform_action(transfer, command, robot)

    def get_commands(self) -> list[str]:
        return [
            "move dist",
            "turn turn_angle",
            "set_state new_internal_equipment",
            "start",
            "stop",
        ]

    def get_equipments(self) -> list[str]:
        return [
            "water",
            "soap",
            "brush",
        ]
