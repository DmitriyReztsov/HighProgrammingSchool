from event_storage import EventStore
from robot_interface import (
    MoveRequested,
    SetEquipmentRequested,
    StartRequested,
    StopRequested,
    TurnRequested,
)


class CommandHandler:
    """Только парсинг и валидация команды -> событие-запрос в EventStore.
    """

    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def handle(self, command_str: str) -> None:
        cmd = command_str.split(" ")
        if cmd[0] == "move":
            self.event_store.append(MoveRequested(float(cmd[1])))
        elif cmd[0] == "turn":
            self.event_store.append(TurnRequested(float(cmd[1])))
        elif cmd[0] == "set":
            self.event_store.append(SetEquipmentRequested(cmd[1]))
        elif cmd[0] == "start":
            self.event_store.append(StartRequested())
        elif cmd[0] == "stop":
            self.event_store.append(StopRequested())
        else:
            raise ValueError("Unknown command")
