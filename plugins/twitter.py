from typing import Any

import requests

from interfaces.auth import OAuth1


class Twitter:
    def __init__(self, auth: OAuth1) -> None:
        self.name = "twitter"
        self.auth = auth
        self.api_base_url = "https://api.twitter.com/2"

    def get_name(self) -> str:
        return self.name

    def validate(self) -> bool:
        if not self.auth:
            print("No credentials to validate")
            return False
        return True

    def get_user_info(self) -> bool | Any:
        """
        Test the API connection by making a simple request.
        Twitter API v2 endpoint for getting user details
        """
        if not self.validate():
            return False

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
