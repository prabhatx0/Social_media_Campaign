# tests/test_scraper.py
import pytest
from unittest.mock import patch, MagicMock
from scraper.scraper import scrape_text_from_url

@patch('scraper.scraper.requests.get')
def test_scrape_text_from_url_success(mock_get):
    """Test successful scraping of a simple HTML page."""
    html_content = """
    <html>
        <head><title>Test</title></head>
        <body>
            <script>console.log('ignore')</script>
            <style>.ignore { color: red; }</style>
            <header><h1>Title</h1></header>
            <main><p>This is the main content.</p><p>Another paragraph.</p></main>
            <footer>Footer content</footer>
        </body>
    </html>
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = html_content.encode('utf-8')
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = scrape_text_from_url("[http://example.com](http://example.com)")
    
    expected_text = "Test\nTitle\nThis is the main content.\nAnother paragraph.\nFooter content"
    assert result == expected_text
    mock_get.assert_called_once_with("[http://example.com](http://example.com)", headers=pytest.ANY, timeout=10)

@patch('scraper.scraper.requests.get')
def test_scrape_text_from_url_http_error(mock_get):
    """Test handling of HTTP errors during scraping."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    result = scrape_text_from_url("[http://example.com/notfound](http://example.com/notfound)")
    assert result == ""

@patch('scraper.scraper.requests.get')
def test_scrape_text_from_url_connection_error(mock_get):
    """Test handling of connection errors."""
    mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")

    result = scrape_text_from_url("[http://example.com/unreachable](http://example.com/unreachable)")
    assert result == ""
