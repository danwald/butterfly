#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from interfaces.auth import OAuth1
from plugins.twitter import Twitter


def run_twitter_oauth_example() -> bool:
    # Get OAuth credentials from environment variables
    consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("One or more Twitter OAuth environment variables not set.")
        print("Required environment variables:")
        print("  TWITTER_CONSUMER_KEY")
        print("  TWITTER_CONSUMER_SECRET")
        print("  TWITTER_ACCESS_TOKEN")
        print("  TWITTER_ACCESS_TOKEN_SECRET")
        return False

    # Create Twitter plugin instance
    twitter = Twitter(
        OAuth1(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
    )

    # Now we can execute commands
    result = twitter.get_user_info()
    print(f"Execute result: {result}")
    return True


if __name__ == "__main__":
    run_twitter_oauth_example()
