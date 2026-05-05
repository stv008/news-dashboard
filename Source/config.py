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

    # === AI — Frontier Labs & Primary Research (Tier 1) ===
    "OpenAI": [
        {"url": "https://openai.com/news/rss.xml", "section": "News"},
    ],
    "Google DeepMind": [
        {"url": "https://deepmind.google/blog/rss.xml", "section": "Blog"},
    ],
    "Google Research": [
        {"url": "https://blog.research.google/feeds/posts/default", "section": "Research"},
    ],
    "Hugging Face": [
        {"url": "https://huggingface.co/blog/feed.xml", "section": "Blog"},
    ],
    "NVIDIA Developer": [
        {"url": "https://developer.nvidia.com/blog/feed/", "section": "Developer"},
    ],
    "NVIDIA Research": [
        {"url": "https://research.nvidia.com/rss.xml", "section": "Research"},
    ],
    "Apple ML Research": [
        {"url": "https://machinelearning.apple.com/rss.xml", "section": "Research"},
    ],
    "Allen AI (Ai2)": [
        {"url": "https://allenai.org/rss.xml", "section": "News"},
    ],
    "MIT CSAIL": [
        {"url": "https://www.csail.mit.edu/rss.xml", "section": "News"},
    ],
    "MIT News — AI": [
        {"url": "https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml", "section": "AI"},
    ],
    "Berkeley AI Research": [
        {"url": "https://bair.berkeley.edu/blog/feed.xml", "section": "Blog"},
    ],
    # REMOVED 2026-05-05: arXiv cs.AI/LG/CL — firehose (1000+ papers/day) drowned signal.
    # Re-add via topic-keyword filter or curated subset (e.g., Hugging Face Daily Papers).
    "Replicate": [
        {"url": "https://replicate.com/blog/rss", "section": "Blog"},
    ],
    "LangChain Changelog": [
        {"url": "https://changelog.langchain.com/feed.xml", "section": "Changelog"},
    ],
    # BROKEN 2026-05-05: Anthropic, Meta AI, Microsoft Research, Microsoft AI Blog,
    #                    Cohere, Stanford HAI, DeepLearning.AI/The Batch, ElevenLabs,
    #                    Pinecone, Papers with Code, HuggingFace Daily Papers
    #                    — no public RSS endpoint accessible (404/403/HTML responses tested).

    # === AI — Analysis & Strategy (Tier 2) ===
    "Stratechery": [
        {"url": "https://stratechery.com/feed/", "section": "Analysis"},
    ],
    "Import AI": [
        {"url": "https://importai.substack.com/feed", "section": "Weekly"},
    ],
    "One Useful Thing (Mollick)": [
        {"url": "https://www.oneusefulthing.org/feed", "section": "Analysis"},
    ],
    "Latent Space": [
        {"url": "https://www.latent.space/feed", "section": "Engineering"},
    ],
    "Marginal Revolution": [
        {"url": "https://marginalrevolution.com/feed", "section": "Economics+AI"},
    ],
    "Astral Codex Ten": [
        {"url": "https://www.astralcodexten.com/feed", "section": "Long-form"},
    ],
    "LessWrong": [
        {"url": "https://www.lesswrong.com/feed.xml", "section": "Community"},
    ],
    "AI Snake Oil": [
        {"url": "https://www.aisnakeoil.com/feed", "section": "Critical"},
    ],
    "The Gradient": [
        {"url": "https://thegradientpub.substack.com/feed", "section": "Research"},
    ],
    "Gary Marcus": [
        {"url": "https://garymarcus.substack.com/feed", "section": "Skeptical"},
    ],
    "Interconnects (Lambert)": [
        {"url": "https://www.interconnects.ai/feed", "section": "Post-training"},
    ],
    "The Algorithmic Bridge": [
        {"url": "https://www.thealgorithmicbridge.com/feed", "section": "Commentary"},
    ],
    "Eric Topol — Ground Truths": [
        {"url": "https://erictopol.substack.com/feed", "section": "Healthcare AI"},
    ],
    "Benedict Evans": [
        {"url": "https://www.ben-evans.com/benedictevans?format=rss", "section": "Strategy"},
    ],

    # === AI — EU / Mobility / Romania (Tier 5) ===
    "Politico Europe": [
        {"url": "https://www.politico.eu/feed/", "section": "Tech/Policy"},
    ],
    "EU AI Act Tracker": [
        {"url": "https://artificialintelligenceact.eu/feed/", "section": "Policy"},
    ],
    "CSET (Georgetown)": [
        {"url": "https://cset.georgetown.edu/feed/", "section": "AI Policy"},
    ],
    "Electrek": [
        {"url": "https://electrek.co/feed/", "section": "EV/Mobility"},
    ],
    "start-up.ro": [
        {"url": "https://start-up.ro/feed/", "section": "Romania Tech"},
    ],
    "profit.ro": [
        {"url": "https://www.profit.ro/rss", "section": "Romania Business"},
    ],
    # BROKEN 2026-05-05: Euractiv, OECD AI, Brookings AI, Automotive News, The Drive
    #                    — RSS endpoints return 403/404 or non-RSS content.
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
    # AI — Frontier Labs
    "OpenAI": {"bg": "#000000", "text": "#fff"},
    "Google DeepMind": {"bg": "#4285F4", "text": "#fff"},
    "Google Research": {"bg": "#34A853", "text": "#fff"},
    "Hugging Face": {"bg": "#FFD21E", "text": "#1A1A1A"},
    "NVIDIA Developer": {"bg": "#76B900", "text": "#fff"},
    "NVIDIA Research": {"bg": "#1A4314", "text": "#fff"},
    "Apple ML Research": {"bg": "#1A1A1A", "text": "#fff"},
    "Allen AI (Ai2)": {"bg": "#003E7E", "text": "#fff"},
    "MIT CSAIL": {"bg": "#A31F34", "text": "#fff"},
    "MIT News — AI": {"bg": "#8A1A2A", "text": "#fff"},
    "Berkeley AI Research": {"bg": "#003262", "text": "#FDB515"},
    "Replicate": {"bg": "#000000", "text": "#fff"},
    "LangChain Changelog": {"bg": "#1C3C3C", "text": "#fff"},
    # AI — Analysis & Strategy
    "Stratechery": {"bg": "#D4661F", "text": "#fff"},
    "Import AI": {"bg": "#0F4C81", "text": "#fff"},
    "One Useful Thing (Mollick)": {"bg": "#5E35B1", "text": "#fff"},
    "Latent Space": {"bg": "#0F766E", "text": "#fff"},
    "Marginal Revolution": {"bg": "#8B7355", "text": "#fff"},
    "Astral Codex Ten": {"bg": "#7B2D26", "text": "#fff"},
    "LessWrong": {"bg": "#2C3E50", "text": "#fff"},
    "AI Snake Oil": {"bg": "#4A4A4A", "text": "#fff"},
    "The Gradient": {"bg": "#1A535C", "text": "#fff"},
    "Gary Marcus": {"bg": "#6A1B1B", "text": "#fff"},
    "Interconnects (Lambert)": {"bg": "#1E3A8A", "text": "#fff"},
    "The Algorithmic Bridge": {"bg": "#6D28D9", "text": "#fff"},
    "Eric Topol — Ground Truths": {"bg": "#0E7C4A", "text": "#fff"},
    "Benedict Evans": {"bg": "#3F3F46", "text": "#fff"},
    # AI — EU / Mobility / Romania
    "Politico Europe": {"bg": "#FF1A4B", "text": "#fff"},
    "EU AI Act Tracker": {"bg": "#003399", "text": "#FFCC00"},
    "CSET (Georgetown)": {"bg": "#041E42", "text": "#fff"},
    "Electrek": {"bg": "#00B956", "text": "#fff"},
    "start-up.ro": {"bg": "#E94B3C", "text": "#fff"},
    "profit.ro": {"bg": "#0E6E2A", "text": "#fff"},
}

# === Tier classification (used for dashboard filter pills) ===
# Maps publication name → tier slug. Publications not listed default to "other".
PUB_TIERS = {
    # Macro & Business (the original 6)
    "Financial Times": "macro", "Bloomberg": "macro", "Wall Street Journal": "macro",
    "New York Times": "macro", "The Economist": "macro", "Harvard Business Review": "macro",
    # Tech Press (AI-focused or AI-section feeds)
    "The Verge — AI": "techpress", "TechCrunch — AI": "techpress",
    "Wired — AI": "techpress", "Ars Technica — AI": "techpress",
    "MIT Technology Review": "techpress", "IEEE Spectrum — AI": "techpress",
    "VentureBeat — AI": "techpress", "The Decoder": "techpress",
    "CNBC — Technology": "techpress", "The Register": "techpress",
    "Axios — Technology": "techpress", "Rest of World": "techpress",
    # Aggregators (community / meta-curation)
    "Hacker News": "aggregators", "Techmeme": "aggregators",
    "r/MachineLearning": "aggregators", "r/LocalLLaMA": "aggregators",
    "r/singularity": "aggregators", "Last Week in AI": "aggregators",
    # Frontier Labs (primary research / official lab blogs)
    "OpenAI": "frontier", "Google DeepMind": "frontier", "Google Research": "frontier",
    "Hugging Face": "frontier", "NVIDIA Developer": "frontier", "NVIDIA Research": "frontier",
    "Apple ML Research": "frontier", "Allen AI (Ai2)": "frontier",
    "MIT CSAIL": "frontier", "MIT News — AI": "frontier",
    "Berkeley AI Research": "frontier", "Replicate": "frontier",
    "LangChain Changelog": "frontier",
    # Analysis & Strategy (synthesis voices)
    "Stratechery": "analysis", "Import AI": "analysis",
    "One Useful Thing (Mollick)": "analysis", "Latent Space": "analysis",
    "Marginal Revolution": "analysis", "Astral Codex Ten": "analysis",
    "LessWrong": "analysis", "AI Snake Oil": "analysis",
    "The Gradient": "analysis", "Gary Marcus": "analysis",
    "Interconnects (Lambert)": "analysis", "The Algorithmic Bridge": "analysis",
    "Eric Topol — Ground Truths": "analysis", "Benedict Evans": "analysis",
    # EU & Romania (policy + mobility + local)
    "Politico Europe": "eu_ro", "EU AI Act Tracker": "eu_ro",
    "CSET (Georgetown)": "eu_ro", "Electrek": "eu_ro",
    "start-up.ro": "eu_ro", "profit.ro": "eu_ro",
}

# Display order and human labels for the tier filter pills.
TIER_ORDER = ["macro", "frontier", "analysis", "techpress", "eu_ro", "aggregators"]
TIER_LABELS = {
    "macro": "Macro & Business",
    "frontier": "Frontier Labs",
    "analysis": "Analysis",
    "techpress": "Tech Press",
    "eu_ro": "EU & Romania",
    "aggregators": "Aggregators",
    "other": "Other",
}

# === Fetcher settings ===
LOOKBACK_HOURS = 48             # How many hours back to look for articles

# Per-publication overrides. Some publications (HBR, weekly newsletters) don't
# publish often enough for the global 48h window — extend their lookback.
LOOKBACK_OVERRIDES = {
    "Harvard Business Review": 168,         # 1 week
    "Last Week in AI": 240,                 # 10 days (weekly newsletter)
    "MIT Technology Review": 168,           # 1 week
    # Weekly/sporadic substacks & analyses
    "Stratechery": 168,                     # 2x/week
    "Import AI": 240,                       # weekly
    "One Useful Thing (Mollick)": 240,      # weekly
    "Latent Space": 240,                    # weekly
    "Astral Codex Ten": 240,                # sporadic
    "AI Snake Oil": 336,                    # ~2 weeks
    "The Gradient": 336,                    # irregular
    "Gary Marcus": 240,                     # ~weekly
    "Interconnects (Lambert)": 240,         # weekly
    "The Algorithmic Bridge": 240,          # weekly
    "Eric Topol — Ground Truths": 240,      # weekly
    "Benedict Evans": 240,                  # weekly
    # Sporadic policy / research
    "EU AI Act Tracker": 336,               # legislative cadence
    "CSET (Georgetown)": 336,               # weekly/monthly
    "Allen AI (Ai2)": 240,                  # research cadence
    "Apple ML Research": 720,               # ~monthly
    "NVIDIA Research": 336,                 # research cadence
    "Berkeley AI Research": 336,            # research cadence
    "MIT CSAIL": 240,                       # weekly
    "MIT News — AI": 168,                   # weekly
    "LangChain Changelog": 240,             # weekly product cadence
    "Replicate": 336,                       # ~weekly to bi-weekly
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
MAX_ARTICLES_TO_SUMMARIZE = 100 # Cap total articles sent for AI summary
MAX_BRIEFING_TOKENS = 2400      # Max output tokens for AI briefing
                                # (briefings densely cite + 4-6 sections need headroom)

# === Server settings ===
SERVER_PORT = 8080
