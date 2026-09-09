from src.fetcher import fetch_page
from src.parser import extract_book_links, extract_next_page_link

def main():
    current_url = "https://books.toscrape.com/catalogue/page-1.html"
    max_pages = 3
    discovered_links = []

    print("--- Stage 2: Discovering Book Links ---")

    for page_num in range(1, max_pages + 1):
        if not current_url:
            break

        html, is_cache, size = fetch_page(current_url)
        status = "CACHE HIT" if is_cache else "FETCH"
        print(f"[{status}] Page {page_num}: {current_url} ({size} bytes)")

        # Extract book links from current page
        links = extract_book_links(html, current_url)
        discovered_links.extend(links)

        # Get next page link dynamically
        current_url = extract_next_page_link(html, current_url)

    print(f"\nTotal book links discovered across {max_pages} pages: {len(discovered_links)}")
    if discovered_links:
        print(f"Sample Link 1: {discovered_links[0]}")
        print(f"Sample Link 60: {discovered_links[-1]}")

if __name__ == "__main__":
    main()