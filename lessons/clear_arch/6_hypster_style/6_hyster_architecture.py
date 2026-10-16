from collections.abc import Callable

import pure_robot


class RobotAPI:
    def create_robot() -> pure_robot.RobotState:
        return pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

    def get_robot_state(robot: pure_robot.RobotState) -> tuple:
        return (robot.x, robot.y, robot.angle, robot.state)

    def get_robot_transfer() -> Callable:
        return pure_robot.transfer_to_cleaner

    def perform_action(transfer: Callable, command: str, robot: pure_robot.RobotState) -> None:
        pure_robot.make(transfer, command, robot)

    def get_commands() -> list:
        return [
            "move dist",
            "turn turn_angle",
            "set_state new_internal_equipment",
            "start",
            "stop",
        ]

    def get_equipments() -> list:
        return [
            "water",
            "soap",
            "brush",
        ]
