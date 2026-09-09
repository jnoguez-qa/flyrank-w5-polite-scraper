from src.fetcher import fetch_page
from src.parser import extract_book_links, extract_next_page_link, parse_book_page
from src.models import Book

def main():
    current_url = "https://books.toscrape.com/catalogue/page-1.html"
    max_pages = 3
    discovered_links = []
    validated_books = []

    print("--- Stage 3: Discovering & Parsing Books ---")

    # 1. Discover Links across 3 pages
    for page_num in range(1, max_pages + 1):
        if not current_url:
            break

        html, is_cache, _ = fetch_page(current_url)
        status = "CACHE HIT" if is_cache else "FETCH"
        print(f"[{status}] Catalogue Page {page_num}: {current_url}")

        links = extract_book_links(html, current_url)
        discovered_links.extend(links)
        current_url = extract_next_page_link(html, current_url)

    print(f"\nDiscovered {len(discovered_links)} books. Extracting and validating...\n")

    # 2. Extract and Validate each book using Pydantic
    for index, book_url in enumerate(discovered_links, 1):
        html, is_cache, size = fetch_page(book_url)
        status = "CACHE HIT" if is_cache else "FETCH"

        raw_data = parse_book_page(html, book_url)
        
        # Pydantic validation
        book_obj = Book(**raw_data)
        validated_books.append(book_obj)

        print(f"[{index}/60] [{status}] Validated: '{book_obj.title}' (£{book_obj.price}) | Rating: {book_obj.rating}/5")

    print(f"\nSuccessfully validated {len(validated_books)} books using Pydantic.")

if __name__ == "__main__":
    main()