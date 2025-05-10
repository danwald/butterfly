import os
from typing import Any

import requests

from interfaces.auth import BearerAuth
from utils import setup_logger


class Mastodon:
    def __init__(
        self,
        auth: BearerAuth = BearerAuth(access_token=os.environ["MASTODON_BEARER_TOKEN"]),
        debug: bool = False,
    ) -> None:
        self.name = "mastodon"
        self.auth = auth
        self.api_base_url = "https://techhub.social/api"
        self.logger = setup_logger(f"plugins.{self.name}", debug)

    def get_name(self) -> str:
        return self.name

    def get_user_info(self) -> bool | Any:
        endpoint = f"{self.api_base_url}/v1/accounts/verify_credentials"
        try:
            response = requests.get(endpoint, headers=self.auth.header, timeout=10)
            # Check if the request was successful
            if response.status_code == 200:
                self.logger.info("Mastodon API connection successful!")
                return response.json()
            else:
                error_msg = (
                    response.json()
                    .get("errors", [{}])[0]
                    .get("message", "Unknown error")
                )
                self.logger.error(
                    f"Mastodon API connection failed: {response.status_code} - {error_msg}"
                )
                return False

        except requests.RequestException as e:
            self.logger.error(f"Request to Mastodon API failed: {e}")
            return False

    def authorize(self, *args: tuple[Any]) -> bool:
        return bool(self.auth)

    def validate(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        if not self.auth:
            self.logger.error("Invalid Credentials")
            return False
        return self.get_user_info()

    def execute(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        endpoint = f"{self.api_base_url}/v1/statuses"

        try:
            response = requests.post(
                endpoint,
                headers=self.auth.header,
                data={"status": args[0]},
                timeout=10,
            )

            # Check if the request was successful
            if response.status_code == 200:
                self.logger.info("Successfully posted to Mastodon")
                return True
            else:
                error_msg = (
                    response.json()
                    .get("errors", [{}])[0]
                    .get("message", "Unknown error")
                )
                self.logger.error(
                    f"Mastodon API connection failed: {response.status_code} - {error_msg}"
                )
                return False

        except requests.RequestException as e:
            self.logger.error(f"Request to Mastodon API failed: {e}")
            return False
