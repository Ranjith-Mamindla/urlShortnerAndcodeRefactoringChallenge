from datetime import datetime, timezone

# In-memory store for shortened URLs
# key: short_code, value: dict with original URL, creation time, clicks count
url_store = {}

# Example to add a new URL entry:
def add_url(short_code, original_url):
    url_store[short_code] = {
        "url": original_url,
        "created_at": datetime.now(timezone.utc),  # timezone-aware UTC datetime
        "clicks": 0
    }
