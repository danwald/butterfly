from typing import Protocol


class Creds(Protocol):
    def validate(self):
        ...


class Auth(Protocol):
    def authorize(self) -> bool:
        ...
