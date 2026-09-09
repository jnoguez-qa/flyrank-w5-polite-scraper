import hashlib
import time
from pathlib import Path
import requests
from src.config import USER_AGENT, HTTP_TIMEOUT, REQUEST_DELAY, CACHE_DIR

def get_cache_filename(url: str) -> Path:
    """Generate a readable filename for the cached file based on the URL."""
    if "page-1.html" in url or url.endswith("books.toscrape.com/") or url.endswith("index.html"):
        filename = "catalogue-page-1.html"
    elif "page-2.html" in url:
        filename = "catalogue-page-2.html"
    elif "page-3.html" in url:
        filename = "catalogue-page-3.html"
    else:
        url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:10]
        filename = f"page-{url_hash}.html"
    return CACHE_DIR / filename

def fetch_page(url: str) -> tuple[str, bool, int]:
    """
    Fetch HTML content from a URL or read from local cache.
    Returns: (html_content, is_cache_hit, content_size_bytes)
    """
    cache_path = get_cache_filename(url)

    # 1. Read from cache if it exists
    if cache_path.exists():
        html_content = cache_path.read_text(encoding="utf-8")
        return html_content, True, len(html_content.encode("utf-8"))

    # 2. Polite Delay before network request
    time.sleep(REQUEST_DELAY)

    # 3. Fetch from network
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)

    # 4. Verify status code
    if response.status_code != 200:
        raise RuntimeError(f"Fetch failed for {url} with status code {response.status_code}")

    html_content = response.text

    # 5. Save to cache
    cache_path.write_text(html_content, encoding="utf-8")
    
    return html_content, False, len(html_content.encode("utf-8"))

def check_target_health(url: str = "https://books.toscrape.com/") -> bool:
    """Perform a lightweight health check to verify target website availability."""
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.head(url, headers=headers, timeout=HTTP_TIMEOUT)
        if response.status_code == 200:
            return True
        # Fallback to GET if HEAD is not allowed by server
        response = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
        return response.status_code == 200
    except requests.RequestException:
        return False