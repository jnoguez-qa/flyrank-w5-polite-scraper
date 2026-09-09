import pytest
from src.models import Book
from src.parser import parse_book_page, extract_book_links

# HTML ficticio para probar parseo y validación de Pydantic
MOCK_BOOK_HTML = """
<html>
    <body>
        <div class="product_main">
            <h1>Test Book Title</h1>
            <p class="star-rating four"></p>
        </div>
        <div id="product_description"></div>
        <p>A test description for the book.</p>
        <table class="table-striped">
            <tr><th>UPC</th><td>abc123upc</td></tr>
            <tr><th>Product Type</th><td>Books</td></tr>
            <tr><th>Price (excl. tax)</th><td>£10.00</td></tr>
            <tr><th>Price (incl. tax)</th><td>£12.00</td></tr>
            <tr><th>Tax</th><td>£2.00</td></tr>
            <tr><th>Availability</th><td>In stock (15 available)</td></tr>
            <tr><th>Number of reviews</th><td>0</td></tr>
        </table>
    </body>
</html>
"""

def test_parse_book_page_extracts_correct_data():
    url = "https://books.toscrape.com/catalogue/test-book_1/index.html"
    raw_data = parse_book_page(MOCK_BOOK_HTML, url)
    
    assert raw_data["title"] == "Test Book Title"
    assert raw_data["rating"] == 4
    assert raw_data["price"] == 12.0
    assert raw_data["stock_count"] == 15
    assert raw_data["upc"] == "abc123upc"

    

def test_pydantic_book_model_validation():
    url = "https://books.toscrape.com/catalogue/test-book_1/index.html"
    raw_data = parse_book_page(MOCK_BOOK_HTML, url)
    
    book = Book(**raw_data)
    assert book.title == "Test Book Title"
    assert book.rating == 4
    assert book.price == 12.0
    assert book.stock_count == 15

def test_extract_book_links_returns_absolute_urls():
    catalogue_html = """
    <article class="product_pod">
        <h3><a href="book_1/index.html">Book 1</a></h3>
    </article>
    """
    base_url = "https://books.toscrape.com/catalogue/page-1.html"
    links = extract_book_links(catalogue_html, base_url)
    
    assert len(links) == 1
    assert links[0] == "https://books.toscrape.com/catalogue/book_1/index.html"