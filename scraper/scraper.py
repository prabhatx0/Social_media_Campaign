import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_text_from_url(url: str) -> str:
    """
    Scrapes the main text content from a given URL.

    Args:
        url: The URL of the webpage to scrape.

    Returns:
        The extracted text content, or an empty string if scraping fails.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        if not text:
            logging.warning(f"No text content found at {url}")
            return ""

        logging.info(f"Successfully scraped content from {url}. Length: {len(text)} characters.")
        return text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping URL {url}: {e}")
        return ""
