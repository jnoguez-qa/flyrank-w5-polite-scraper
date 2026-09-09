from src.fetcher import fetch_page

def main():
    target_url = "https://books.toscrape.com/catalogue/page-1.html"
    
    try:
        html, is_cache, size = fetch_page(target_url)
        status_label = "CACHE HIT" if is_cache else "FETCH"
        print(f"[{status_label}] Size: {size} bytes | URL: {target_url}")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()