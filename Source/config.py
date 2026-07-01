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

    # === Emerging Markets — Business & AI (Tier 6) ===
    # Added 2026-06-23. All RSS endpoints verified live. Reputable regional
    # business/tech sources across China, India, Brazil, Poland, Germany,
    # Middle East, Indonesia, Singapore, Taiwan, Japan, South Korea, Hong Kong.
    # China
    "SCMP — Tech": [
        {"url": "https://www.scmp.com/rss/318208/feed", "section": "Tech"},
    ],
    "TechNode": [
        {"url": "https://technode.com/feed/", "section": "China Tech"},
    ],
    "Pandaily": [
        {"url": "https://pandaily.com/feed/", "section": "China AI"},
    ],
    # Hong Kong
    "Hong Kong Free Press": [
        {"url": "https://hongkongfp.com/feed/", "section": "Hong Kong"},
    ],
    "Asia Times": [
        {"url": "https://asiatimes.com/feed/", "section": "Geopolitics"},
    ],
    # India
    "Livemint — Tech": [
        {"url": "https://www.livemint.com/rss/technology", "section": "Technology"},
    ],
    "Inc42": [
        {"url": "https://inc42.com/feed/", "section": "Startups"},
    ],
    "YourStory": [
        {"url": "https://yourstory.com/feed", "section": "Startups"},
    ],
    # Brazil
    "Brazil Journal": [
        {"url": "https://braziljournal.com/feed/", "section": "Business"},
    ],
    "Startups Brasil": [
        {"url": "https://www.startups.com.br/feed/", "section": "Startups"},
    ],
    # Poland
    "Notes from Poland": [
        {"url": "https://notesfrompoland.com/feed/", "section": "Poland"},
    ],
    "300Gospodarka": [
        {"url": "https://300gospodarka.pl/feed", "section": "Economy"},
    ],
    "Rzeczpospolita": [
        {"url": "https://www.rp.pl/rss/1019", "section": "Business"},
    ],
    # Germany
    "Der Spiegel — International": [
        {"url": "https://www.spiegel.de/international/index.rss", "section": "International"},
    ],
    "Heise online": [
        {"url": "https://www.heise.de/rss/heise-atom.xml", "section": "Tech"},
    ],
    "t3n": [
        {"url": "https://t3n.de/rss.xml", "section": "Digital"},
    ],
    "Handelsblatt": [
        {"url": "https://www.handelsblatt.com/contentexport/feed/schlagzeilen", "section": "Business"},
    ],
    # Middle East
    "Al Jazeera": [
        {"url": "https://www.aljazeera.com/xml/rss/all.xml", "section": "Middle East"},
    ],
    "Wamda": [
        {"url": "https://www.wamda.com/feed", "section": "MENA Startups"},
    ],
    # REMOVED 2026-06-23: Arab News — RSS valid but returns HTTP 403 from
    # GitHub Actions runner IPs (Cloudflare). Works from residential IPs only.
    # "Arab News": [
    #     {"url": "https://www.arabnews.com/rss.xml", "section": "Gulf Business"},
    # ],
    # Indonesia
    "Antara News": [
        {"url": "https://en.antaranews.com/rss/news.xml", "section": "Indonesia"},
    ],
    "Tech in Asia": [
        {"url": "https://www.techinasia.com/feed", "section": "SEA Tech"},
    ],
    # Singapore
    "Channel NewsAsia": [
        {"url": "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml", "section": "Singapore"},
    ],
    "Straits Times — Business": [
        {"url": "https://www.straitstimes.com/news/business/rss.xml", "section": "Business"},
    ],
    # Taiwan
    "DigiTimes": [
        {"url": "https://www.digitimes.com/rss/daily.xml", "section": "Semiconductors"},
    ],
    "Taipei Times": [
        {"url": "https://www.taipeitimes.com/xml/index.rss", "section": "Taiwan"},
    ],
    # Japan
    "The Japan Times": [
        {"url": "https://www.japantimes.co.jp/feed/", "section": "Japan"},
    ],
    # South Korea
    "Korea Times — Tech": [
        {"url": "https://www.koreatimes.co.kr/www/rss/tech.xml", "section": "Tech"},
    ],
    "TheElec": [
        {"url": "http://www.thelec.kr/rss/allArticle.xml", "section": "Semiconductors"},
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
    # Emerging Markets — China / HK
    "SCMP — Tech": {"bg": "#FFCA05", "text": "#1A1A1A"},
    "TechNode": {"bg": "#00A8A8", "text": "#fff"},
    "Pandaily": {"bg": "#2D2D2D", "text": "#fff"},
    "Hong Kong Free Press": {"bg": "#E4002B", "text": "#fff"},
    "Asia Times": {"bg": "#A8232C", "text": "#fff"},
    # Emerging Markets — India
    "Livemint — Tech": {"bg": "#0B7FBF", "text": "#fff"},
    "Inc42": {"bg": "#1BB394", "text": "#fff"},
    "YourStory": {"bg": "#ED1C24", "text": "#fff"},
    # Emerging Markets — Brazil
    "Brazil Journal": {"bg": "#009C3B", "text": "#fff"},
    "Startups Brasil": {"bg": "#FF5C00", "text": "#fff"},
    # Emerging Markets — Poland
    "Notes from Poland": {"bg": "#DC143C", "text": "#fff"},
    "300Gospodarka": {"bg": "#B01C2E", "text": "#fff"},
    "Rzeczpospolita": {"bg": "#7A1420", "text": "#fff"},
    # Emerging Markets — Germany
    "Der Spiegel — International": {"bg": "#E64415", "text": "#fff"},
    "Heise online": {"bg": "#BD1421", "text": "#fff"},
    "t3n": {"bg": "#149EE7", "text": "#fff"},
    "Handelsblatt": {"bg": "#FF8000", "text": "#fff"},
    # Emerging Markets — Middle East
    "Al Jazeera": {"bg": "#E8B500", "text": "#1A1A1A"},
    "Wamda": {"bg": "#00AEEF", "text": "#fff"},
    # Emerging Markets — Indonesia
    "Antara News": {"bg": "#C8102E", "text": "#fff"},
    "Tech in Asia": {"bg": "#EE2A24", "text": "#fff"},
    # Emerging Markets — Singapore
    "Channel NewsAsia": {"bg": "#D4202A", "text": "#fff"},
    "Straits Times — Business": {"bg": "#00407A", "text": "#fff"},
    # Emerging Markets — Taiwan
    "DigiTimes": {"bg": "#003B71", "text": "#fff"},
    "Taipei Times": {"bg": "#1C5E3A", "text": "#fff"},
    # Emerging Markets — Japan
    "The Japan Times": {"bg": "#00305C", "text": "#fff"},
    # Emerging Markets — South Korea
    "Korea Times — Tech": {"bg": "#003A70", "text": "#fff"},
    "TheElec": {"bg": "#0F4C81", "text": "#fff"},
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
    # Emerging Markets (China, India, Brazil, Poland, Germany, Middle East,
    # Indonesia, Singapore, Taiwan, Japan, South Korea, Hong Kong)
    "SCMP — Tech": "emkt", "TechNode": "emkt", "Pandaily": "emkt",
    "Hong Kong Free Press": "emkt", "Asia Times": "emkt",
    "Livemint — Tech": "emkt", "Inc42": "emkt", "YourStory": "emkt",
    "Brazil Journal": "emkt", "Startups Brasil": "emkt",
    "Notes from Poland": "emkt", "300Gospodarka": "emkt", "Rzeczpospolita": "emkt",
    "Der Spiegel — International": "emkt", "Heise online": "emkt",
    "t3n": "emkt", "Handelsblatt": "emkt",
    "Al Jazeera": "emkt", "Wamda": "emkt",
    "Antara News": "emkt", "Tech in Asia": "emkt",
    "Channel NewsAsia": "emkt", "Straits Times — Business": "emkt",
    "DigiTimes": "emkt", "Taipei Times": "emkt",
    "The Japan Times": "emkt",
    "Korea Times — Tech": "emkt", "TheElec": "emkt",
}

# Display order and human labels for the tier filter pills.
TIER_ORDER = ["macro", "frontier", "analysis", "techpress", "eu_ro", "emkt", "aggregators"]
TIER_LABELS = {
    "macro": "Macro & Business",
    "frontier": "Frontier Labs",
    "analysis": "Analysis",
    "techpress": "Tech Press",
    "eu_ro": "EU & Romania",
    "emkt": "Emerging Markets",
    "aggregators": "Aggregators",
    "other": "Other",
}

# === Fetcher settings ===
LOOKBACK_HOURS = 48             # How many hours back to look for articles

# Per-publication overrides. Some publications (HBR, weekly newsletters) don't
# publish often enough for the global 48h window — extend their lookback.
LOOKBACK_OVERRIDES = {
    "The Economist": 168,                   # 1 week (weekly edition, mid-week publish)
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
    # Emerging Markets — startup/regional outlets that publish less often
    "Wamda": 168,                           # MENA startup news, ~weekly cadence
    "Notes from Poland": 120,               # 5 days
    "Startups Brasil": 120,                 # 5 days
    "Pandaily": 120,                        # 5 days
    "Brazil Journal": 96,                   # 4 days
    "Der Spiegel — International": 336,      # English edition is curated, ~weekly cadence
    "Korea Times — Tech": 168,              # tech section, lower cadence
}

# Some feeds emit entry links as relative paths with no usable base to resolve
# them against (no xml:base, and the feed's own rel="self" link is broken —
# HBR's atom feed literally returns "site.hostname/..." unsubstituted). For
# those publications, hardcode the real site root so fetcher.py can urljoin
# the relative path into a working absolute URL.
LINK_BASE_OVERRIDES = {
    "Harvard Business Review": "https://hbr.org",
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

# === Translation settings (optional) ===
# Publications that publish in a language other than English. Their article
# titles + summaries are translated to English (via Claude Haiku) at build time;
# the original text is preserved in the title_original/summary_original columns.
# Publications NOT listed here are assumed to already be in English.
PUB_LANGUAGES = {
    "Heise online": "German",
    "t3n": "German",
    "Handelsblatt": "German",
    "300Gospodarka": "Polish",
    "Rzeczpospolita": "Polish",
    "Brazil Journal": "Portuguese",
    "Startups Brasil": "Portuguese",
    "TheElec": "Korean",
    # Note: Korea Times, SCMP, TechNode, Pandaily, Asia Times, Antara (EN edition),
    # Tech in Asia, CNA, Straits Times, DigiTimes, Taipei Times, Japan Times all
    # publish in English — no translation needed.
}
TRANSLATE_MODEL = "claude-haiku-4-5"   # cheap/fast model for bulk translation
TRANSLATE_BATCH_SIZE = 20              # articles per Claude call
TRANSLATE_MAX_TOKENS = 4096           # output cap per batch

# === Claude API settings (optional) ===
CLAUDE_MODEL = "claude-sonnet-4-6"
MAX_ARTICLES_TO_SUMMARIZE = 100 # Cap total articles sent for AI summary
MAX_BRIEFING_TOKENS = 3200      # Max output tokens for AI briefing
                                # 4-6 sections + per-section <a href> sources block
                                # need ~3K to render without truncation

# === Server settings ===
SERVER_PORT = 8080
