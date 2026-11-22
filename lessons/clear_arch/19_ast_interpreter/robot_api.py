import pure_robot
from robot_interface import MoveResponse, TurnResponse, StateResponse


class RobotApi:
    @staticmethod
    def move(dist, state):
        new_state = pure_robot.move(pure_robot.transfer_to_cleaner, dist, state)
        return MoveResponse(dist, success=True), new_state

    @staticmethod
    def turn(turn_angle, state):
        new_state = pure_robot.turn(pure_robot.transfer_to_cleaner, turn_angle, state)
        return TurnResponse(turn_angle, success=True), new_state

    @staticmethod
    def set_state(new_internal_state, state):
        new_internal_state = new_internal_state.lower()
        new_state = pure_robot.set_state(
            pure_robot.transfer_to_cleaner, new_internal_state, state
        )
        # pure_robot.set_state возвращает прежнее состояние, если режим неизвестен
        # как пример обработки ошибки
        success = new_state is not state
        return StateResponse(new_internal_state, success), new_state

    @staticmethod
    def start(state):
        new_state = pure_robot.start(pure_robot.transfer_to_cleaner, state)
        return StateResponse(state.state.value, success=True), new_state

    @staticmethod
    def stop(state):
        return pure_robot.stop(pure_robot.transfer_to_cleaner, state)
