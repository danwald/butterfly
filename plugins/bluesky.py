import os
from typing import Any

from interfaces.auth import UsernameAuth


class BlueSky:
    def __init__(
        self,
        auth: UsernameAuth = UsernameAuth(
            username=os.environ["BSKY_USERNAME"], password=os.environ["BSKY_PASSWORD"]
        ),
    ) -> None:
        self.name = "bluesky"
        self.auth = auth

    def get_name(self) -> str:
        return self.name

    def authorize(self, *args: tuple[Any]) -> bool:
        return bool(self.auth.username and self.auth.password)

    def validate(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        if not self.authorize():
            print("Invalid Credentials")
            return False
        _ = self.auth.get_client()
        return True

    def execute(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        if not self.authorize():
            print("Invalid Credentials")
            return False
        return True
