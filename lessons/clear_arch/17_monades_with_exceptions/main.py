import robot_monad


def main():
    initial_state = robot_monad.StateMonad(
        robot_monad.RobotState(0.0, 0.0, 0, robot_monad.WATER)
    )
    result = (
        initial_state.bind(robot_monad.move(100))
        .bind(robot_monad.turn(-90))
        .bind(robot_monad.set_state(robot_monad.SOAP))
        .bind(robot_monad.start)
        .bind(robot_monad.move(50))
        .bind(robot_monad.stop)
    )

    print(f"Final state: {result.state}")
    print(f"Log: {result.log}")
    print(f"First error: {result.error}")


if __name__ == "__main__":
    main()
