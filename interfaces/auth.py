from dataclasses import dataclass
from typing import Any, Protocol


class Creds(Protocol):
    def validate(self) -> bool: ...


class Auth(Protocol):
    def authorize(self, *args: tuple[Any]) -> bool: ...


@dataclass
class BearerAuth:
    auth_header: dict[str, Any]

    def authorize(self, *args: tuple[Any]) -> bool:
        return True
