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