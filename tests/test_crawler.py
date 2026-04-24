"""
test_crawler.py

Unit tests for crawler.py.

These tests avoid hitting the live website by using sample HTML
and mocked request behaviour.
"""

from src.crawler import find_next_page, parse_page


SAMPLE_HTML_WITH_NEXT = """
<html>
    <body>
        <div class="quote">
            <span class="text">“The world as we have created it is a process of our thinking.”</span>
            <small class="author">Albert Einstein</small>
            <div class="tags">
                <a class="tag">change</a>
                <a class="tag">thinking</a>
            </div>
        </div>

        <li class="next">
            <a href="/page/2/">Next</a>
        </li>
    </body>
</html>
"""


SAMPLE_HTML_LAST_PAGE = """
<html>
    <body>
        <div class="quote">
            <span class="text">“A final quote.”</span>
            <small class="author">Final Author</small>
            <div class="tags">
                <a class="tag">final</a>
            </div>
        </div>
    </body>
</html>
"""


def test_parse_page_extracts_quote_text_author_and_tags():
    """
    Check that parse_page extracts quote text, author, tags,
    and combined content correctly.
    """
    result = parse_page(
        SAMPLE_HTML_WITH_NEXT,
        "https://quotes.toscrape.com/",
        1,
    )

    assert result["url"] == "https://quotes.toscrape.com/"
    assert result["page_number"] == 1
    assert len(result["quotes"]) == 1

    quote = result["quotes"][0]

    assert quote["text"] == "“The world as we have created it is a process of our thinking.”"
    assert quote["author"] == "Albert Einstein"
    assert quote["tags"] == ["change", "thinking"]

    assert "Albert Einstein" in result["content"]
    assert "change" in result["content"]
    assert "thinking" in result["content"]


def test_find_next_page_returns_absolute_url():
    """
    Check that find_next_page converts a relative next-page link
    into an absolute URL.
    """
    next_url = find_next_page(
        SAMPLE_HTML_WITH_NEXT,
        "https://quotes.toscrape.com/",
    )

    assert next_url == "https://quotes.toscrape.com/page/2/"


def test_find_next_page_returns_none_on_last_page():
    """
    Check that find_next_page returns None when there is no next link.
    """
    next_url = find_next_page(
        SAMPLE_HTML_LAST_PAGE,
        "https://quotes.toscrape.com/page/10/",
    )

    assert next_url is None


import pytest
import requests

from src.crawler import fetch_page


class MockResponse:
    """
    Minimal mock response object that behaves like a requests response.
    """

    def __init__(self, text: str, should_raise: bool = False):
        self.text = text
        self.should_raise = should_raise

    def raise_for_status(self):
        """
        Simulate requests.Response.raise_for_status().
        """
        if self.should_raise:
            raise requests.HTTPError("Mock HTTP error")


def test_fetch_page_returns_html_on_success(monkeypatch):
    """
    Check that fetch_page returns HTML when the request succeeds.
    """

    def mock_get(url, timeout):
        return MockResponse("<html>success</html>")

    monkeypatch.setattr(requests, "get", mock_get)

    result = fetch_page("https://quotes.toscrape.com/")

    assert result == "<html>success</html>"


def test_fetch_page_returns_none_on_timeout(monkeypatch):
    """
    Check that fetch_page handles timeout errors gracefully.
    """

    def mock_get(url, timeout):
        raise requests.Timeout("Mock timeout")

    monkeypatch.setattr(requests, "get", mock_get)

    result = fetch_page("https://quotes.toscrape.com/")

    assert result is None


def test_fetch_page_returns_none_on_http_error(monkeypatch):
    """
    Check that fetch_page handles HTTP errors gracefully.
    """

    def mock_get(url, timeout):
        return MockResponse("<html>error</html>", should_raise=True)

    monkeypatch.setattr(requests, "get", mock_get)

    result = fetch_page("https://quotes.toscrape.com/bad-page/")

    assert result is None