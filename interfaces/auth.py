import base64
import hashlib
import hmac
import os
import time
import urllib.parse
from dataclasses import dataclass
from typing import Any, Protocol

from requests.auth import AuthBase


class Auth(Protocol):
    def authorize(self, *args: tuple[Any]) -> bool: ...


@dataclass
class BearerAuth:
    key: str = "Authorization"
    access_token: str = ""

    @property
    def header(self) -> dict[str, str]:
        if not self:
            raise ValueError("Invalid BearerToken")
        return {self.key: f"Bearer {self.access_token}"}

    def __bool__(self) -> bool:
        return bool(self.key and self.access_token)


class OAuth1(AuthBase):
    """
    Twitter OAuth 1.0a implementation for use with the requests library.
    """

    def __init__(
        self,
        consumer_key: str = os.environ.get("TWITTER_CONSUMER_KEY", ""),
        consumer_secret: str = os.environ.get("TWITTER_CONSUMER_SECRET", ""),
        access_token: str = os.environ.get("TWITTER_ACCESS_TOKEN", ""),
        access_token_secret: str = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", ""),
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def __call__(self, request: Any) -> Any:
        # Add OAuth parameters
        oauth_params = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_nonce": self._generate_nonce(),
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_token": self.access_token,
            "oauth_version": "1.0",
        }

        # Get request method and URL
        method = request.method
        url = request.url
        url_parts = urllib.parse.urlparse(url)
        base_url = f"{url_parts.scheme}://{url_parts.netloc}{url_parts.path}"

        # Extract and encode request parameters
        params: dict[str, str | None] = {}
        if url_parts.query:
            query_params = urllib.parse.parse_qsl(url_parts.query)
            params.update(query_params)

        # Add body parameters if this is a form request
        if request.body and isinstance(request.body, bytes):
            content_type = request.headers.get("Content-Type", "")
            if "application/x-www-form-urlencoded" in content_type:
                body_params = urllib.parse.parse_qsl(request.body.decode("utf-8"))
                params.update(body_params)

        # Add OAuth parameters to the signature base
        params.update(oauth_params)

        # Create signature base string
        param_string = "&".join(
            f"{urllib.parse.quote(key, safe='')}={urllib.parse.quote(str(value), safe='')}"
            for key, value in sorted(params.items())
        )
        signature_base = (
            f"{method}&{urllib.parse.quote(base_url, safe='')}"
            f"&{urllib.parse.quote(param_string, safe='')}"
        )

        # Create signing key
        signing_key = (
            f"{urllib.parse.quote(self.consumer_secret, safe='')}"
            f"&{urllib.parse.quote(self.access_token_secret, safe='')}"
        )

        # Calculate signature
        signature = base64.b64encode(
            hmac.new(
                signing_key.encode("utf-8"),
                signature_base.encode("utf-8"),
                hashlib.sha1,
            ).digest()
        ).decode("utf-8")

        # Add signature to OAuth parameters
        oauth_params["oauth_signature"] = signature

        # Create Authorization header
        auth_header = "OAuth " + ", ".join(
            f'{urllib.parse.quote(key, safe="")}="{urllib.parse.quote(value, safe="")}"'
            for key, value in sorted(oauth_params.items())
        )

        request.headers["Authorization"] = auth_header
        return request

    def _generate_nonce(self) -> str:
        return hashlib.sha1(str(time.time()).encode("utf-8")).hexdigest()

    def authorize(self, *_: tuple[Any]) -> bool:
        return all(
            [
                self.consumer_key,
                self.consumer_secret,
                self.access_token,
                self.access_token_secret,
            ]
        )
