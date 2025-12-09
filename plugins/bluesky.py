import os
from typing import Any

from atproto import client_utils

from interfaces.auth import BlueSkyAuth
from utils import extract_urls


class BlueSky:
    def __init__(
        self,
        auth: BlueSkyAuth = BlueSkyAuth(
            username=os.environ["BSKY_USERNAME"], password=os.environ["BSKY_PASSWORD"]
        ),
    ) -> None:
        self.name = "bluesky"
        self.auth = auth

    def get_name(self) -> str:
        return self.name

    def authorize(self, *_: tuple[Any]) -> bool:
        return bool(self.auth.username and self.auth.password)

    def validate(self, *_: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        if not self.authorize():
            print("Invalid Credentials")
            return False
        return True

    def execute(self, *args: tuple[Any], **_: dict[str, Any]) -> bool:
        if not self.authorize():
            print("Invalid Credentials")
            return False
        if not args and args[0]:
            print("Invalid Text")
            return False

        text = str(args[0])
        text, urls = extract_urls(text)
        builder = client_utils.TextBuilder()
        builder.text(text)
        for upath, url in urls:
            builder.link(upath, url)
        client = self.auth.get_client()
        client.send_post(builder)
        return True
