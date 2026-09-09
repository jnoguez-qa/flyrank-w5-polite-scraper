# 📚 The Polite Scraper — Books to Scrape

A robust, polite, and modular web scraper built with Python to extract structured data from [books.toscrape.com](https://books.toscrape.com/). Designed following professional software development practices, featuring local file caching, strict data validation with **Pydantic**, network health checks, automated unit testing with **pytest**, and multi-format data export (JSON & CSV).

---

## 🛠️ Key Features

* **Polite Scraping:** Implements a configurable delay (`0.5s`) between actual network requests to respect the target server's load.
* **Local File Caching:** Disk-based caching system (`.data_cache/`) powered by SHA-256 URL hashes to prevent redundant network requests and accelerate development iterations.
* **Integrated Health Check:** Lightweight pre-flight check (`HEAD`/`GET`) to verify target website availability before running the extraction pipeline.
* **Dynamic Catalogue Navigation:** Automatic pagination traversal across multiple catalogue pages and individual book detail links.
* **Strict Validation with Pydantic:** Schema enforcement and data normalization (prices as floats, star ratings converted to `1–5` integers, stock counts, UPC, tax breakdown, etc.).
* **Unit Testing Suite:** Comprehensive tests using **pytest** to ensure parsing, cleaning, and model validation remain solid.
* **Multi-Format Export:** Automatic persistence of validated book models to structured `JSON` and `CSV` files in the `data/` directory.

---

## 📂 Project Structure

```text
scraper/
├── data/                    # Output directory for exported files (books.json, books.csv)
├── .data_cache/             # Local cache directory for raw HTML responses
├── src/                     # Core source code
│   ├── __init__.py
│   ├── config.py            # Configuration variables and project constants
│   ├── exporter.py          # Data export module for JSON and CSV formats
│   ├── fetcher.py           # HTTP request management, caching, and health check logic
│   ├── main.py              # Main orchestrator executing the scraping pipeline
│   ├── models.py            # Pydantic data schemas (Book model)
│   └── parser.py            # BeautifulSoup HTML extraction and normalization logic
├── tests/                   # Automated unit testing suite
│   └── test_parser_and_models.py
├── pytest.ini               # Pytest path and runner configuration
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🏗️ System Architecture

```text
[ Health Check ] ──(OK)──> [ Discover Catalogue Pages ]
                                     │
                                     ▼
                            [ Extract Book URLs ]
                                     │
                                     ▼
                        [ Fetch Book HTML (Cache/HTTP) ]
                                     │
                                     ▼
                        [ BeautifulSoup Clean & Parse ]
                                     │
                                     ▼
                        [ Pydantic Data Validation ]
                                     │
                                     ▼
                        [ Export to JSON & CSV ]
```

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/tu-usuario/flyrank-w5-polite-scraper.git](https://github.com/tu-usuario/flyrank-w5-polite-scraper.git)
cd flyrank-w5-polite-scraper/scraper
```

### 2. Create and activate a virtual environment

* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🧪 Running Unit Tests

Run the automated test suite using **pytest** to verify HTML parsing and Pydantic model validation:

```bash
python -m pytest
```

---

## 💻 Running the Scraper

Execute the complete end-to-end pipeline (Health Check, dynamic scraping, Pydantic validation, and data export):

```bash
python -m src.main
```

### Expected Output:
```text
--- Running Health Check ---
Target website is online and healthy.

--- Stage 3: Discovering & Parsing Books ---
[CACHE HIT] Catalogue Page 1: [https://books.toscrape.com/catalogue/page-1.html](https://books.toscrape.com/catalogue/page-1.html)
[CACHE HIT] Catalogue Page 2: [https://books.toscrape.com/catalogue/page-2.html](https://books.toscrape.com/catalogue/page-2.html)
[CACHE HIT] Catalogue Page 3: [https://books.toscrape.com/catalogue/page-3.html](https://books.toscrape.com/catalogue/page-3.html)

Discovered 60 books. Extracting and validating...

[1/60] [FETCH] Validated: 'A Light in the Attic' (£51.77) | Rating: 3/5
...
[60/60] [FETCH] Validated: 'The Natural History of Us' (£45.22) | Rating: 3/5

Successfully validated 60 books using Pydantic.

--- Stage 4: Exporting Data ---
[SUCCESS] Exported 60 books to JSON: data\books.json
[SUCCESS] Exported 60 books to CSV:  data\books.csv
```

---

## 📊 Data Model Schema (`Book`)

| Field | Type | Description |
| :--- | :--- | :--- |
| `url` | `str` | Absolute URL of the book detail page |
| `title` | `str` | Full title of the book |
| `price` | `float` | Price in GBP (£) |
| `rating` | `int` | Star rating integer (`1` to `5`) |
| `availability` | `str` | Raw availability status string |
| `stock_count` | `int` | Number of items available in stock |
| `upc` | `str` | Universal Product Code (UPC) |
| `product_type` | `str` | Product classification category |
| `price_excl_tax` | `float` | Price excluding taxes |
| `price_incl_tax` | `float` | Price including taxes |
| `tax` | `float` | Calculated tax amount |
| `number_of_reviews` | `int` | Total number of customer reviews |
| `description` | `str \| None` | Product description text |

---

## 📄 License

This repository was created for educational software engineering purposes following ethical web scraping principles.