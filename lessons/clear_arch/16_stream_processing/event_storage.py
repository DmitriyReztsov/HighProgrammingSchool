from collections.abc import Callable


class EventStore:
    """Журнал событий + шина: хранит все события и уведомляет подписчиков."""

    def __init__(self):
        self._events: list = []
        self._subscribers: dict[type, list[Callable]] = {}

    def subscribe(self, event_type: type, handler: Callable) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def append(self, event) -> None:
        self._events.append(event)
        for handler in self._subscribers.get(type(event), []):
            handler(event)

    def events_of(self, event_types: tuple[type]) -> list:
        return [e for e in self._events if isinstance(e, event_types)]

    @property
    def events(self) -> tuple:
        return tuple(self._events)
