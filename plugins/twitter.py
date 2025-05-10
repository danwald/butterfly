from typing import Any

import requests

from interfaces import auth
from utils import setup_logger


class Twitter:
    def __init__(self, auth: auth.OAuth1 = auth.OAuth1(), debug: bool = False) -> None:
        self.name = "twitter"
        self.auth = auth
        self.api_base_url = "https://api.twitter.com/2"
        self.logger = setup_logger(f"plugins.{self.name}", debug)

    def get_name(self) -> str:
        return self.name

    def get_user_info(self) -> bool | Any:
        """
        Test the API connection by making a simple request.
        Twitter API v2 endpoint for getting user details
        """
        # Using the /2/users/me endpoint which requires a valid token
        endpoint = f"{self.api_base_url}/users/me"

        try:
            response = requests.get(endpoint, auth=self.auth, timeout=10)

            # Check if the request was successful
            if response.status_code == 200:
                self.logger.info("Twitter API connection successful!")
                return response.json()
            else:
                error_msg = (
                    response.json()
                    .get("errors", [{}])[0]
                    .get("message", "Unknown error")
                )
                self.logger.error(
                    f"Twitter API connection failed: {response.status_code} - {error_msg}"
                )
                return False

        except requests.RequestException as e:
            self.logger.error(f"Request to Twitter API failed: {e}")
            return False

    def authorize(self, *args: tuple[Any]) -> bool:
        if self.auth:
            return self.auth.authorize()
        return False

    def validate(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        if not self.authorize():
            self.logger.error("Invalid Credentials")
            return False
        return self.get_user_info()

    def execute(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        endpoint = f"{self.api_base_url}/tweets"

        try:
            response = requests.post(
                endpoint, auth=self.auth, json={"text": args[0]}, timeout=10
            )

            # Check if the request was successful
            if response.status_code == 201:
                self.logger.info("Successfully posted to Twitter")
                return True
            else:
                error_msg = (
                    response.json()
                    .get("errors", [{}])[0]
                    .get("message", "Unknown error")
                )
                self.logger.error(
                    f"Twitter API connection failed: {response.status_code} - {error_msg}"
                )
                return False

        except requests.RequestException as e:
            self.logger.error(f"Request to Twitter API failed: {e}")
            return False
