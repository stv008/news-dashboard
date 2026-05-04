"""
Configuration for News Dashboard
RSS feeds and settings for all publications.
"""

import os

# === Paths ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(SCRIPT_DIR, "articles.db")
OUTPUT_HTML = os.path.join(PROJECT_DIR, "Output", "dashboard.html")

# === RSS Feed sources ===
FEEDS = {
    "The Economist": [
        {"url": "https://www.economist.com/finance-and-economics/rss.xml", "section": "Finance & Economics"},
        {"url": "https://www.economist.com/business/rss.xml", "section": "Business"},
        {"url": "https://www.economist.com/leaders/rss.xml", "section": "Leaders"},
        {"url": "https://www.economist.com/briefing/rss.xml", "section": "Briefing"},
        {"url": "https://www.economist.com/international/rss.xml", "section": "International"},
        {"url": "https://www.economist.com/europe/rss.xml", "section": "Europe"},
    ],
    "Wall Street Journal": [
        {"url": "https://feeds.content.dowjones.io/public/rss/RSSOpinion", "section": "Opinion"},
        {"url": "https://feeds.content.dowjones.io/public/rss/socialeconomyfeed", "section": "Economy"},
        {"url": "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain", "section": "Markets"},
        {"url": "https://feeds.content.dowjones.io/public/rss/WSJcomUSBusiness", "section": "US Business"},
        {"url": "https://feeds.content.dowjones.io/public/rss/RSSWorldNews", "section": "World"},
        {"url": "https://feeds.content.dowjones.io/public/rss/RSSWSJD", "section": "Tech"},
    ],
    "New York Times": [
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "section": "Home"},
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", "section": "Business"},
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "section": "Technology"},
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "section": "World"},
        {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "section": "Politics"},
    ],
    "Bloomberg": [
        {"url": "https://feeds.bloomberg.com/markets/news.rss", "section": "Markets"},
        {"url": "https://feeds.bloomberg.com/politics/news.rss", "section": "Politics"},
        {"url": "https://feeds.bloomberg.com/technology/news.rss", "section": "Technology"},
        {"url": "https://feeds.bloomberg.com/wealth/news.rss", "section": "Wealth"},
    ],
    "Financial Times": [
        {"url": "https://www.ft.com/rss/home", "section": "Home"},
        {"url": "https://www.ft.com/companies?format=rss", "section": "Companies"},
        {"url": "https://www.ft.com/markets?format=rss", "section": "Markets"},
        {"url": "https://www.ft.com/world?format=rss", "section": "World"},
    ],
    "Harvard Business Review": [
        {"url": "https://feeds.feedburner.com/harvardbusiness", "section": "Latest"},
    ],
}

PUB_COLORS = {
    "Financial Times": {"bg": "#FCD0A1", "text": "#33302E"},
    "Bloomberg": {"bg": "#472AAF", "text": "#fff"},
    "Wall Street Journal": {"bg": "#0080C3", "text": "#fff"},
    "New York Times": {"bg": "#1A1A1A", "text": "#fff"},
    "The Economist": {"bg": "#E3120B", "text": "#fff"},
    "Harvard Business Review": {"bg": "#C8102E", "text": "#fff"},
}

LOOKBACK_HOURS = 48

# Per-publication overrides. HBR doesn't publish on weekends, so the
# global 48h window drops it every Monday morning.
LOOKBACK_OVERRIDES = {
    "Harvard Business Review": 168,  # 1 week
}

MAX_ARTICLES_PER_PUB = 15
FETCH_TIMEOUT_SECONDS = 15
FETCH_DELAY_SECONDS = 0.5
MAX_FETCH_RETRIES = 3
MAX_SUMMARY_LENGTH = 500
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)
MAX_ARTICLE_AGE_DAYS = 90
CLAUDE_MODEL = "claude-sonnet-4-6"
MAX_ARTICLES_TO_SUMMARIZE = 30
MAX_BRIEFING_TOKENS = 1500
SERVER_PORT = 8080
