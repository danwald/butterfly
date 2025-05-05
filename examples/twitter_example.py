#!/usr/bin/env python3

import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from plugins.twitter import Twitter


def run_twitter_oauth_example() -> bool:
    # Create Twitter plugin instance
    twitter = Twitter()
    if not twitter.validate():
        print("One or more Twitter OAuth environment variables not set.")
        print("Required environment variables:")
        print("  TWITTER_CONSUMER_KEY")
        print("  TWITTER_CONSUMER_SECRET")
        print("  TWITTER_ACCESS_TOKEN")
        print("  TWITTER_ACCESS_TOKEN_SECRET")
        return False

    # Now we can execute commands
    result = twitter.validate()
    print(f"Execute result: {result}")
    return True


if __name__ == "__main__":
    run_twitter_oauth_example()
