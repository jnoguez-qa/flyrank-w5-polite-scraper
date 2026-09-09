from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "cache"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure required directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Politeness Settings
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/jnoguez-qa/flyrank-w5-polite-scraper)"
HTTP_TIMEOUT = 10  # seconds
REQUEST_DELAY = 0.5  # seconds