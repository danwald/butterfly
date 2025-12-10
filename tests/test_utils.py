import pytest

from src.utils import extract_urls


@pytest.mark.parametrize(
    "input_text,expected_text,expected_urls",
    [
        # Basic URL extraction
        (
            "Check out https://example.com/example for more info",
            "Check out  for more info",
            [("/example", "https://example.com/example")],
        ),
        # Multiple URLs
        (
            "Visit https://example.com and http://test.org/foobar",
            "Visit  and ",
            [("0", "https://example.com"), ("/foobar", "http://test.org/foobar")],
        ),
        # No URLs
        (
            "This is just plain text without any URLs",
            "This is just plain text without any URLs",
            [],
        ),
    ],
)
def test_extract_urls(
    input_text: str, expected_text: str, expected_urls: list[tuple[str, str]]
) -> None:
    """Test extract_urls function with various input scenarios."""
    text_without_urls, urls = extract_urls(input_text)
    assert text_without_urls == expected_text
    assert urls == expected_urls
