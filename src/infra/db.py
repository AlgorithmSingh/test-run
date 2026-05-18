"""Stub persistence module. In a real codebase this would wrap a real DB driver."""


class Database:
    def save(self, key: str, value: dict) -> None:
        # pretend to persist
        pass

    def load(self, key: str) -> dict | None:
        return None


db = Database()
