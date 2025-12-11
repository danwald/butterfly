import re
from urllib.parse import urlsplit


def extract_urls(text: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Extract URLs from text and return the text without URLs and a list of path and url.

    Args:
        text: The text to extract URLs from

    Returns:
        A tuple of (text_without_urls, list_of_urls)
    """
    # Regular expression pattern for matching URLs
    # Matches http(s):// followed by domain and optional path/query/fragment
    url_pattern = re.compile(
        r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:[:\d]*)?(?:[/?#](?:[^\s])*)?"
    )

    # Find all URLs in the text
    urls = re.findall(url_pattern, text)

    # Remove all URLs from the text
    text_without_urls = re.sub(url_pattern, "", text)

    return text_without_urls, [
        (urlsplit(url).path or str(idx), url) for idx, url in enumerate(urls)
    ]
