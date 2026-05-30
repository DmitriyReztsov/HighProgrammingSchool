import sqlite3
from typing import Protocol, override


class Storage(Protocol):
    def save(self, data: str) -> None: ...
    def retrieve(self, id: int) -> str: ...


class DBStorage(Storage):
    _instance = None
    _connection: sqlite3.Connection = None

    def __new__(cls, db_path=":memory:"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._connection = sqlite3.connect(db_path)
            cls._connection.row_factory = sqlite3.Row

        return cls._instance

    def __init__(self, table: str | None = None):
        if table is None:
            table = "interface"

        # skip 'table' validation

        self.table = table
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT
                )
                """
            )

    @override
    def save(self, data: str) -> None:
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {self.table} (data) VALUES (?)", (data,))

    @override
    def retrieve(self, id: int) -> str:
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT data FROM {self.table} WHERE id = ?", (id,))
            row = cursor.fetchone()
            return row["data"] if row else None


if __name__ == "__main__":
    interface_storage = DBStorage()
    interface_storage.save("first data")
    interface_storage.save("second data")
    interface_storage.save("third data")

    print(interface_storage.retrieve(3))
    print(interface_storage.retrieve(2))
    print(interface_storage.retrieve(1))

    another_table_storage = DBStorage("a_table")
    another_table_storage.save("a first data")
    another_table_storage.save("a second data")
    another_table_storage.save("a third data")

    print(another_table_storage.retrieve(3))
    print(another_table_storage.retrieve(2))
    print(another_table_storage.retrieve(1))
