import pure_robot
from event_storage import EventStore
from robot_interface import (
    CleaningStarted,
    CleaningStopped,
    EquipmentChanged,
    MoveRequested,
    RequestFailed,
    RobotMoved,
    RobotStateView,
    RobotTransfer,
    RobotTurned,
    SetEquipmentRequested,
    StartRequested,
    StopRequested,
    TurnRequested,
)


def _dummy_transfer(message: str) -> None:
    pass


class BaseProcessor:
    def __init__(self, event_store: EventStore, init_robot: RobotStateView):
        self.event_store = event_store
        self.init_robot = init_robot

    def _current_state(self) -> RobotStateView:
        facts = self.event_store.events_of((RobotMoved, RobotTurned, EquipmentChanged))
        return facts[-1].new_state if facts else self.init_robot


class MovementProcessor(BaseProcessor):
    def __init__(self, event_store: EventStore, init_robot: RobotStateView):
        super().__init__(event_store, init_robot)
        event_store.subscribe(MoveRequested, self.on_move_requested)
        event_store.subscribe(TurnRequested, self.on_turn_requested)

    def on_move_requested(self, event: MoveRequested) -> None:
        if event.distance < 0:
            self.event_store.append(RequestFailed("negative distance"))
            return
        state = self._current_state()
        new_state = pure_robot.move(_dummy_transfer, event.distance, state)
        self.event_store.append(RobotMoved(event.distance, new_state))

    def on_turn_requested(self, event: TurnRequested) -> None:
        state = self._current_state()
        new_state = pure_robot.turn(_dummy_transfer, event.angle, state)
        self.event_store.append(RobotTurned(event.angle, new_state))


class CleaningProcessor(BaseProcessor):
    def __init__(self, event_store: EventStore, init_robot: RobotStateView):
        super().__init__(event_store, init_robot)
        event_store.subscribe(SetEquipmentRequested, self.on_set_requested)
        event_store.subscribe(StartRequested, self.on_start_requested)
        event_store.subscribe(StopRequested, self.on_stop_requested)

    def on_set_requested(self, event: SetEquipmentRequested) -> None:
        state = self._current_state()
        new_state = pure_robot.set_state(_dummy_transfer, event.equipment, state)
        if new_state is state:
            self.event_store.append(RequestFailed(f"unknown equipment: {event.equipment}"))
            return
        self.event_store.append(EquipmentChanged(event.equipment, new_state))

    def on_start_requested(self, event: StartRequested) -> None:
        state = self._current_state()
        self.event_store.append(CleaningStarted(state.state.value))

    def on_stop_requested(self, event: StopRequested) -> None:
        self.event_store.append(CleaningStopped())


class TransferProcessor:
    def __init__(self, event_store: EventStore, transfer: RobotTransfer):
        self.transfer = transfer
        event_store.subscribe(RobotMoved, self.on_moved)
        event_store.subscribe(RobotTurned, self.on_turned)
        event_store.subscribe(EquipmentChanged, self.on_equipment_changed)
        event_store.subscribe(CleaningStarted, self.on_started)
        event_store.subscribe(CleaningStopped, self.on_stopped)
        event_store.subscribe(RequestFailed, self.on_failed)

    def on_moved(self, event: RobotMoved) -> None:
        self.transfer(f"POS {event.new_state.x} {event.new_state.y}")

    def on_turned(self, event: RobotTurned) -> None:
        self.transfer(f"ANGLE {event.new_state.angle}")

    def on_equipment_changed(self, event: EquipmentChanged) -> None:
        self.transfer(f"STATE {event.equipment}")

    def on_started(self, event: CleaningStarted) -> None:
        self.transfer(f"START WITH {event.equipment}")

    def on_stopped(self, event: CleaningStopped) -> None:
        self.transfer("STOP")

    def on_failed(self, event: RequestFailed) -> None:
        self.transfer(f"FAILED: {event.reason}")
