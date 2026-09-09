import time
from src.fetcher import fetch_page, check_target_health
from src.parser import extract_book_links, extract_next_page_link, parse_book_page
from src.models import Book
from src.exporter import export_to_json, export_to_csv, export_run_report

def main():
    start_time = time.time()

    print("--- Running Health Check ---")
    if not check_target_health():
        print("Error: Target website is unreachable or returned an unhealthy status code. Aborting.")
        return
    print("Target website is online and healthy.\n")

    current_url = "https://books.toscrape.com/catalogue/page-1.html"
    max_pages = 3
    discovered_links = []
    validated_books = []

    print("--- Stage 3: Discovering & Parsing Books ---")

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

    for index, book_url in enumerate(discovered_links, 1):
        html, is_cache, _ = fetch_page(book_url)
        status = "CACHE HIT" if is_cache else "FETCH"

        raw_data = parse_book_page(html, book_url)
        book_obj = Book(**raw_data)
        validated_books.append(book_obj)

        print(f"[{index}/60] [{status}] Validated: '{book_obj.title}' (£{book_obj.price}) | Rating: {book_obj.rating}/5")

    print(f"\nSuccessfully validated {len(validated_books)} books using Pydantic.")

    # Stage 4 & 6: Export Data & Execution Report
    print("\n--- Stage 4 & 6: Exporting Data and Run Report ---")
    json_file = export_to_json(validated_books)
    csv_file = export_to_csv(validated_books)
    
    elapsed_time = time.time() - start_time
    report_file = export_run_report(len(validated_books), max_pages, elapsed_time)

    print(f"[SUCCESS] Exported {len(validated_books)} books to JSON: {json_file}")
    print(f"[SUCCESS] Exported {len(validated_books)} books to CSV:  {csv_file}")
    print(f"[SUCCESS] Run Report generated: {report_file}")

if __name__ == "__main__":
    main()