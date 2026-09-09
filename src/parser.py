import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Helper to convert word ratings to integers
RATING_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5
}

def extract_book_links(html_content: str, base_url: str) -> list[str]:
    """Extract all product page links from a catalogue page and convert them to absolute URLs."""
    soup = BeautifulSoup(html_content, "html.parser")
    book_links = []
    
    articles = soup.find_all("article", class_="product_pod")
    for article in articles:
        a_tag = article.find("h3").find("a") if article.find("h3") else None
        if a_tag and a_tag.get("href"):
            relative_url = a_tag["href"]
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

def parse_rating(soup: BeautifulSoup) -> int:
    """Extract rating from class names safely (e.g. 'star-rating Three' -> 3)."""
    rating_tag = soup.find("p", class_=re.compile(r"star-rating", re.I))
    if rating_tag:
        # Cambiamos "classes" por "class" en la línea 41
        classes = rating_tag.get("class", [])
        for class_name in classes:
            lower_class = class_name.lower().strip()
            if lower_class in RATING_MAP:
                return RATING_MAP[lower_class]
    return 1  # Fallback si no se encuentra la clase

def parse_book_page(html_content: str, url: str) -> dict:
    """Extract raw and cleaned product details from a book detail page safely."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Main Title
    product_main = soup.find("div", class_="product_main")
    title = ""
    if product_main:
        h1_tag = product_main.find("h1")
        if h1_tag:
            title = h1_tag.get_text(strip=True)
    
    # 2. Rating
    rating = parse_rating(soup)
    
    # 3. Product Description
    desc_tag = soup.find("div", id="product_description")
    description = ""
    if desc_tag:
        p_tag = desc_tag.find_next_sibling("p")
        if p_tag:
            description = p_tag.get_text(strip=True)
            
    # 4. Product Information Table (UPC, Prices, Stock, Reviews)
    table_data = {}
    table = soup.find("table", class_="table-striped")
    if table:
        for row in table.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td:
                table_data[th.get_text(strip=True)] = td.get_text(strip=True)
            
    # Clean Prices
    def clean_price(val_str: str) -> float:
        cleaned = re.sub(r"[^\d.]", "", val_str)
        return float(cleaned) if cleaned else 0.0

    price = clean_price(table_data.get("Price (incl. tax)", "0"))
    price_excl_tax = clean_price(table_data.get("Price (excl. tax)", "0"))
    price_incl_tax = clean_price(table_data.get("Price (incl. tax)", "0"))
    tax = clean_price(table_data.get("Tax", "0"))
    
    # Availability & Stock Count
    availability_str = table_data.get("Availability", "")
    stock_match = re.search(r"In stock \((\d+) available\)", availability_str)
    stock_count = int(stock_match.group(1)) if stock_match else 0
    
    # Number of reviews
    reviews_str = table_data.get("Number of reviews", "0")
    number_of_reviews = int(reviews_str) if reviews_str.isdigit() else 0

    return {
        "url": url,
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability_str,
        "stock_count": stock_count,
        "upc": table_data.get("UPC", ""),
        "product_type": table_data.get("Product Type", ""),
        "price_excl_tax": price_excl_tax,
        "price_incl_tax": price_incl_tax,
        "tax": tax,
        "number_of_reviews": number_of_reviews,
        "description": description
    }