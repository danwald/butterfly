from typing import Protocol


class Creds(Protocol):
    def validate(self) -> bool: ...


class Auth(Protocol):
    def authorize(self) -> bool: ...
