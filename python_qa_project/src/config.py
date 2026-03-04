# src/config.py

# This Python dictionary holds configuration details for different websites.
# It makes our script flexible. We can easily add new sites here.
SITE_CONFIGS = {
    "hackernews": {
        "name": "Hacker News",
        "start_url": "https://news.ycombinator.com/newest",
        "article_selector": "tr.athing",
        "title_selector": ".titleline > a",
        "link_selector": ".titleline > a",
        "timestamp": {
            "strategy": "sibling-attribute",
            "sibling_selector": ".age",
            "attribute": "title",
            "transform": lambda raw: raw.split(" ")[0] if raw else None,
        },
        "pagination_selector": "a.morelink",
    },
    # You could add another site config here, like for Reddit.
    # "reddit": { /* ... */ }
}

# These are constants for our script.
TARGET_ARTICLE_COUNT = 100
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/533.36"
SLEEP_SECONDS = 0.5  # Playwright Python's asyncio.sleep takes seconds
OUTPUT_DIR_NAME = "reports"  # This is the name of the folder for our reports.
