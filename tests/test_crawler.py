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

from src import crawler


def test_crawl_site_traverses_pages_until_no_next(monkeypatch):
    """
    Check that crawl_site follows pagination until no next page exists.

    This test mocks fetch_page and wait_if_needed so it does not hit
    the live site and does not wait 6 seconds between pages.
    """

    page_1_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">“Page one quote.”</span>
                <small class="author">Author One</small>
                <a class="tag">pageone</a>
            </div>
            <li class="next"><a href="/page/2/">Next</a></li>
        </body>
    </html>
    """

    page_2_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">“Page two quote.”</span>
                <small class="author">Author Two</small>
                <a class="tag">pagetwo</a>
            </div>
        </body>
    </html>
    """

    def mock_fetch_page(url):
        if url == "https://quotes.toscrape.com/":
            return page_1_html
        if url == "https://quotes.toscrape.com/page/2/":
            return page_2_html
        return None

    def mock_wait_if_needed(last_request_time, delay=6):
        return None

    monkeypatch.setattr(crawler, "fetch_page", mock_fetch_page)
    monkeypatch.setattr(crawler, "wait_if_needed", mock_wait_if_needed)

    pages = crawler.crawl_site("https://quotes.toscrape.com/")

    assert len(pages) == 2
    assert pages[0]["page_number"] == 1
    assert pages[1]["page_number"] == 2
    assert pages[0]["url"] == "https://quotes.toscrape.com/"
    assert pages[1]["url"] == "https://quotes.toscrape.com/page/2/"

from src.crawler import wait_if_needed


def test_wait_if_needed_does_not_sleep_on_first_request(monkeypatch):
    """
    Check that the first request does not trigger a delay.
    """
    sleep_calls = []

    def mock_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr("time.sleep", mock_sleep)

    wait_if_needed(last_request_time=None, delay=6)

    assert sleep_calls == []


def test_wait_if_needed_sleeps_remaining_time(monkeypatch):
    """
    Check that wait_if_needed sleeps only for the remaining delay time.
    """
    sleep_calls = []

    def mock_time():
        return 10.0

    def mock_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr("time.time", mock_time)
    monkeypatch.setattr("time.sleep", mock_sleep)

    wait_if_needed(last_request_time=6.0, delay=6)

    assert sleep_calls == [2.0]