import os
import re
from typing import Any

from atproto import client_utils

from interfaces.auth import BlueSkyAuth


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

    def authorize(self, *args: tuple[Any]) -> bool:
        return bool(self.auth.username and self.auth.password)

    def validate(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        if not self.authorize():
            print("Invalid Credentials")
            return False
        return True

    def execute(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        if not self.authorize():
            print("Invalid Credentials")
            return False
        if not args and args[0]:
            print("Invalid Text")
            return False

        text = str(args[0])
        text, urls = self.extract_urls(text)
        builder = client_utils.TextBuilder()
        builder.text(text)
        for url in urls:
            builder.link(url, url)
        client = self.auth.get_client()
        client.send_post(builder)
        return True

    def extract_urls(self, text: str) -> tuple[str, list[str]]:
        # Regular expression pattern for matching URLs
        url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"

        # Find all URLs in the text
        urls = re.findall(url_pattern, text)

        # Remove all URLs from the text
        text_without_urls = re.sub(url_pattern, "", text)

        return text_without_urls, urls
