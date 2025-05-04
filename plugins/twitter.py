from typing import Any

import requests

from interfaces import auth


class Twitter:
    def __init__(self, auth: auth.OAuth1 = auth.OAuth1()) -> None:
        self.name = "twitter"
        self.auth = auth
        self.api_base_url = "https://api.twitter.com/2"

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
                print("Twitter API connection successful!")
                return response.json()
            else:
                error_msg = (
                    response.json()
                    .get("errors", [{}])[0]
                    .get("message", "Unknown error")
                )
                print(
                    f"Twitter API connection failed: {response.status_code} - {error_msg}"
                )
                return False

        except requests.RequestException as e:
            print(f"Request to Twitter API failed: {e}")
            return False

    def authorize(self, *args: tuple[Any]) -> bool:
        if self.auth:
            return self.auth.authorize()
        return False

    def validate(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> bool:
        if not self.authorize():
            print("Invalid Credentials")
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
                return True
            else:
                error_msg = (
                    response.json()
                    .get("errors", [{}])[0]
                    .get("message", "Unknown error")
                )
                print(
                    f"Twitter API connection failed: {response.status_code} - {error_msg}"
                )
                return False

        except requests.RequestException as e:
            print(f"Request to Twitter API failed: {e}")
            return False
