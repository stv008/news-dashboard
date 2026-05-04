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
# Each publication may have multiple feeds (sections)
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

    # === AI — Tech Press (Tier 3) ===
    "The Verge — AI": [
        {"url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "section": "AI"},
    ],
    "TechCrunch — AI": [
        {"url": "https://techcrunch.com/category/artificial-intelligence/feed/", "section": "AI"},
    ],
    "Wired — AI": [
        {"url": "https://www.wired.com/feed/tag/ai/latest/rss", "section": "AI"},
    ],
    "Ars Technica — AI": [
        {"url": "https://arstechnica.com/ai/feed/", "section": "AI"},
    ],
    "MIT Technology Review": [
        {"url": "https://www.technologyreview.com/feed/", "section": "Latest"},
    ],
    "IEEE Spectrum — AI": [
        {"url": "https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss", "section": "AI"},
    ],
    "VentureBeat — AI": [
        {"url": "https://venturebeat.com/category/ai/feed/", "section": "AI"},
    ],
    "The Decoder": [
        {"url": "https://the-decoder.com/feed/", "section": "AI"},
    ],
    # BROKEN 2026-05-04: Forbes has no public AI-section RSS (404 on /ai/feed/).
    # "Forbes — AI": [
    #     {"url": "https://www.forbes.com/ai/feed/", "section": "AI"},
    # ],
    # BROKEN 2026-05-04: Reuters RSS endpoints return 401/000 (auth required).
    # "Reuters — Technology": [
    #     {"url": "https://www.reuters.com/arc/outboundfeeds/v3/category/technology/?outputType=xml", "section": "Technology"},
    # ],
    "CNBC — Technology": [
        {"url": "https://www.cnbc.com/id/19854910/device/rss/rss.html", "section": "Technology"},
    ],
    # BROKEN 2026-05-04: Engadget has no AI-section RSS; general feed available but not AI-focused.
    # "Engadget — AI": [
    #     {"url": "https://www.engadget.com/rss-ai.xml", "section": "AI"},
    # ],
    "The Register": [
        {"url": "https://www.theregister.com/headlines.atom", "section": "Tech"},
    ],
    "Axios — Technology": [
        {"url": "https://www.axios.com/feeds/feed.rss", "section": "All"},
    ],
    # BROKEN 2026-05-04: AP technology-only feed not available; only general AP feedburner works.
    # "AP — Technology": [
    #     {"url": "https://feeds.apnews.com/apf-technology", "section": "Technology"},
    # ],
    "Rest of World": [
        {"url": "https://restofworld.org/feed/", "section": "Latest"},
    ],

    # === AI — Aggregators (Tier 4) ===
    "Hacker News": [
        {"url": "https://hnrss.org/frontpage", "section": "Front Page"},
        {"url": "https://hnrss.org/newest?q=AI", "section": "AI Filter"},
    ],
    "Techmeme": [
        {"url": "https://www.techmeme.com/feed.xml", "section": "Tech Meta"},
    ],
    "r/MachineLearning": [
        {"url": "https://www.reddit.com/r/MachineLearning/.rss", "section": "Top"},
    ],
    "r/LocalLLaMA": [
        {"url": "https://www.reddit.com/r/LocalLLaMA/.rss", "section": "Top"},
    ],
    "r/singularity": [
        {"url": "https://www.reddit.com/r/singularity/.rss", "section": "Top"},
    ],
    "Last Week in AI": [
        {"url": "https://lastweekin.ai/feed", "section": "Weekly"},
    ],
}

# === Publication display order and colors ===
PUB_COLORS = {
    "Financial Times": {"bg": "#FCD0A1", "text": "#33302E"},
    "Bloomberg": {"bg": "#472AAF", "text": "#fff"},
    "Wall Street Journal": {"bg": "#0080C3", "text": "#fff"},
    "New York Times": {"bg": "#1A1A1A", "text": "#fff"},
    "The Economist": {"bg": "#E3120B", "text": "#fff"},
    "Harvard Business Review": {"bg": "#C8102E", "text": "#fff"},
    # AI — Tech Press
    "The Verge — AI": {"bg": "#5200FF", "text": "#fff"},
    "TechCrunch — AI": {"bg": "#0A9C3A", "text": "#fff"},
    "Wired — AI": {"bg": "#1A1A1A", "text": "#fff"},
    "Ars Technica — AI": {"bg": "#FF4F00", "text": "#fff"},
    "MIT Technology Review": {"bg": "#E5092F", "text": "#fff"},
    "IEEE Spectrum — AI": {"bg": "#00629B", "text": "#fff"},
    "VentureBeat — AI": {"bg": "#D81C2F", "text": "#fff"},
    "The Decoder": {"bg": "#0F172A", "text": "#fff"},
    "CNBC — Technology": {"bg": "#005594", "text": "#fff"},
    "The Register": {"bg": "#A8232C", "text": "#fff"},
    "Axios — Technology": {"bg": "#1858A7", "text": "#fff"},
    "Rest of World": {"bg": "#0E1A2B", "text": "#fff"},
    # AI — Aggregators
    "Hacker News": {"bg": "#FF6600", "text": "#fff"},
    "Techmeme": {"bg": "#0066CC", "text": "#fff"},
    "r/MachineLearning": {"bg": "#FF4500", "text": "#fff"},
    "r/LocalLLaMA": {"bg": "#FF4500", "text": "#fff"},
    "r/singularity": {"bg": "#FF4500", "text": "#fff"},
    "Last Week in AI": {"bg": "#2563EB", "text": "#fff"},
}

# === Fetcher settings ===
LOOKBACK_HOURS = 48             # How many hours back to look for articles

# Per-publication overrides. Some publications (HBR, weekly newsletters) don't
# publish often enough for the global 48h window — extend their lookback.
LOOKBACK_OVERRIDES = {
    "Harvard Business Review": 168,  # 1 week
    "Last Week in AI": 240,          # 10 days (weekly newsletter)
    "MIT Technology Review": 168,    # 1 week
}

MAX_ARTICLES_PER_PUB = 15       # Maximum articles per publication on dashboard
FETCH_TIMEOUT_SECONDS = 15      # HTTP request timeout per feed
FETCH_DELAY_SECONDS = 0.5       # Politeness delay between feed requests
MAX_FETCH_RETRIES = 3           # Retry transient failures up to N times
MAX_SUMMARY_LENGTH = 500        # Max chars stored per article summary
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# === Database maintenance ===
MAX_ARTICLE_AGE_DAYS = 90       # Prune articles older than this

# === Claude API settings (optional) ===
CLAUDE_MODEL = "claude-sonnet-4-6"
MAX_ARTICLES_TO_SUMMARIZE = 30  # Top N articles to send for AI summary
MAX_BRIEFING_TOKENS = 1500      # Max output tokens for AI briefing

# === Server settings ===
SERVER_PORT = 8080
