from command_handler import CommandHandler
from event_processors import CleaningProcessor, MovementProcessor, TransferProcessor
from event_storage import EventStore
from pure_robot import make_robot, transfer_to_cleaner


def main():
    cmd_list = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]

    event_store = EventStore()
    init_robot = make_robot()

    MovementProcessor(event_store, init_robot)
    CleaningProcessor(event_store, init_robot)
    TransferProcessor(event_store, transfer_to_cleaner)

    command_handler = CommandHandler(event_store)
    for cmd in cmd_list:
        command_handler.handle(cmd)

    # print("\n--- event log ---")
    # for event in event_store.events:
    #     print(event)


if __name__ == "__main__":
    main()
