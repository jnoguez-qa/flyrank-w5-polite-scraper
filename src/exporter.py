import csv
import json
from pathlib import Path
from src.models import Book

DATA_DIR = Path("data")

def export_to_json(books: list[Book], filename: str = "books.json") -> Path:
    """Export list of Pydantic Book models to a formatted JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / filename
    
    # Convert Pydantic models to a list of dicts
    books_data = [book.model_dump() for book in books]
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(books_data, f, ensure_ascii=False, indent=2)
        
    return file_path

def export_to_csv(books: list[Book], filename: str = "books.csv") -> Path:
    """Export list of Pydantic Book models to a CSV file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / filename
    
    if not books:
        return file_path
        
    # Get header field names directly from the Pydantic model
    fieldnames = list(Book.model_fields.keys())
    
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(book.model_dump())
            
    return file_path

def export_run_report(total_books: int, pages_scraped: int, execution_time_sec: float, filename: str = "run_report.json") -> Path:
    """Export run metrics and execution proof to a JSON report."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / filename
    
    report_data = {
        "status": "SUCCESS",
        "target": "https://books.toscrape.com/",
        "total_records_extracted": total_books,
        "pages_scraped": pages_scraped,
        "execution_time_seconds": round(execution_time_sec, 2),
        "politeness_settings": {
            "user_agent": "PoliteScraper/1.0 (+portfolio-project)",
            "request_delay_seconds": 0.5,
            "cache_enabled": True
        }
    }
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
        
    return file_path