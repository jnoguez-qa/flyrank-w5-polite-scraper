from urllib.parse import urljoin
from bs4 import BeautifulSoup

def extract_book_links(html_content: str, base_url: str) -> list[str]:
    """Extract all product page links from a catalogue page and convert them to absolute URLs."""
    soup = BeautifulSoup(html_content, "html.parser")
    book_links = []
    
    # Locate all article tags with class 'product_pod'
    articles = soup.find_all("article", class_="product_pod")
    for article in articles:
        a_tag = article.find("h3").find("a")
        if a_tag and a_tag.get("href"):
            relative_url = a_tag["href"]
            # Convert relative URL (../book_name/index.html) to absolute URL using urljoin
            absolute_url = urljoin(base_url, relative_url)
            book_links.append(absolute_url)
            
    return book_links

def extract_next_page_link(html_content: str, base_url: str) -> str | None:
    """Extract the URL of the next catalogue page if it exists."""
    soup = BeautifulSoup(html_content, "html.parser")
    next_li = soup.find("li", class_="next")
    
    if next_li and next_li.find("a"):
        relative_next = next_li.find("a")["href"]
        return urljoin(base_url, relative_next)
        
    return None