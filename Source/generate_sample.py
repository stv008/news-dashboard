"""Generate sample data to preview the dashboard."""
import sqlite3
import os
import sys
from datetime import datetime, timezone, timedelta

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from config import DB_PATH
from fetcher import init_db, make_id

SAMPLE_ARTICLES = [
    # The Economist
    {"publication": "The Economist", "section": "Leaders", "title": "The world economy's surprising resilience", "summary": "Despite trade tensions and geopolitical uncertainty, global growth continues to outperform expectations. Central banks face a delicate balancing act between inflation control and supporting expansion.", "link": "https://economist.com/1", "author": ""},
    {"publication": "The Economist", "section": "Finance & Economics", "title": "Why the dollar's dominance is being tested", "summary": "A growing number of countries are exploring alternatives to dollar-denominated trade. The implications for global finance are profound.", "link": "https://economist.com/2", "author": ""},
    {"publication": "The Economist", "section": "Business", "title": "AI is reshaping the consulting industry", "summary": "McKinsey, BCG, and Bain are racing to integrate artificial intelligence into their advisory services. The results are transforming how strategic decisions get made.", "link": "https://economist.com/3", "author": ""},
    {"publication": "The Economist", "section": "Europe", "title": "Europe's defence spending surge faces industrial bottlenecks", "summary": "NATO members are finally increasing military budgets, but the continent's defence industry cannot keep up with demand. Supply chains are the new front line.", "link": "https://economist.com/4", "author": ""},

    # Wall Street Journal
    {"publication": "Wall Street Journal", "section": "Markets", "title": "S&P 500 Hits Record as Tech Rally Broadens", "summary": "The benchmark index reached a new all-time high as gains spread beyond the largest technology companies to include industrials and financials.", "link": "https://wsj.com/1", "author": "James Mackintosh"},
    {"publication": "Wall Street Journal", "section": "Business", "title": "Tesla's New Strategy: Cheaper Cars, Bigger Market", "summary": "Elon Musk's pivot to affordable EVs signals a fundamental shift in Tesla's approach to the mass market, but margins are under pressure.", "link": "https://wsj.com/2", "author": "Rebecca Elliott"},
    {"publication": "Wall Street Journal", "section": "Tech", "title": "OpenAI Closes $15 Billion Funding Round at $300B Valuation", "summary": "The AI company's latest fundraise makes it one of the most valuable private companies in history, as enterprise adoption accelerates.", "link": "https://wsj.com/3", "author": "Berber Jin"},
    {"publication": "Wall Street Journal", "section": "World", "title": "China's Manufacturing Sector Shows Renewed Strength", "summary": "Factory activity expanded for the third consecutive month, suggesting Beijing's stimulus measures are gaining traction.", "link": "https://wsj.com/4", "author": "Stella Yifan Xie"},
    {"publication": "Wall Street Journal", "section": "Opinion", "title": "The Fed's Next Move Will Define 2026", "summary": "With inflation sticky and growth solid, the Federal Reserve faces its most consequential policy decision since the pandemic era.", "link": "https://wsj.com/5", "author": "Greg Ip"},

    # New York Times
    {"publication": "New York Times", "section": "Home", "title": "Supreme Court to Hear Major AI Copyright Case", "summary": "The justices will consider whether training AI models on copyrighted material constitutes fair use, in a case that could reshape the technology industry.", "link": "https://nytimes.com/1", "author": "Adam Liptak"},
    {"publication": "New York Times", "section": "Business", "title": "Remote Work Is Here to Stay, New Data Shows", "summary": "Three years after companies began calling workers back, hybrid arrangements have stabilized and productivity metrics support the shift.", "link": "https://nytimes.com/2", "author": "Emma Goldberg"},
    {"publication": "New York Times", "section": "Technology", "title": "Inside Google's Race to Build the Next Generation of Search", "summary": "As AI-powered search tools gain market share, Google is fundamentally rethinking how its core product works.", "link": "https://nytimes.com/3", "author": "Nico Grant"},
    {"publication": "New York Times", "section": "World", "title": "EU Trade Commissioner Pushes for Unified Tariff Response", "summary": "European officials are crafting a coordinated response to new US trade barriers, seeking to avoid a full-scale trade war.", "link": "https://nytimes.com/4", "author": "Matina Stevis-Gridneff"},
    {"publication": "New York Times", "section": "Politics", "title": "Bipartisan Push for AI Regulation Gains Momentum in Senate", "summary": "A coalition of senators from both parties has introduced comprehensive AI oversight legislation, marking the most serious effort yet.", "link": "https://nytimes.com/5", "author": "Cecilia Kang"},

    # Bloomberg
    {"publication": "Bloomberg", "section": "Markets", "title": "Bond Traders Bet on Rate Cut by September", "summary": "Treasury yields fell sharply as economic data pointed to cooling demand, fueling expectations the Fed will ease monetary policy sooner than projected.", "link": "https://bloomberg.com/1", "author": "Liz Capo McCormick"},
    {"publication": "Bloomberg", "section": "Technology", "title": "Microsoft's AI Revenue Tops $10 Billion Quarterly Run Rate", "summary": "Azure AI services and Copilot subscriptions drove the milestone, cementing Microsoft's position as the leading enterprise AI platform.", "link": "https://bloomberg.com/2", "author": "Dina Bass"},
    {"publication": "Bloomberg", "section": "Markets", "title": "Oil Drops Below $70 on OPEC+ Production Increase Plans", "summary": "Crude prices fell after the alliance signaled it would begin unwinding production cuts earlier than expected, pressuring energy stocks.", "link": "https://bloomberg.com/3", "author": "Grant Smith"},
    {"publication": "Bloomberg", "section": "Wealth", "title": "Private Credit Funds Attract Record $50B in Q1", "summary": "Institutional investors continue pouring money into private lending as banks retreat from risk, pushing total private credit AUM past $2 trillion.", "link": "https://bloomberg.com/4", "author": "Silas Brown"},

    # Financial Times
    {"publication": "Financial Times", "section": "Companies", "title": "Arm's chips power 99% of new AI smartphones", "summary": "The SoftBank-owned chip designer's architecture has become the de facto standard for on-device AI processing, creating a powerful moat.", "link": "https://ft.com/1", "author": "Tim Bradshaw"},
    {"publication": "Financial Times", "section": "Markets", "title": "European stocks rally on defence spending optimism", "summary": "Continental equities outperformed US peers as investors bet that increased military budgets will drive industrial growth across the region.", "link": "https://ft.com/2", "author": "Katie Martin"},
    {"publication": "Financial Times", "section": "World", "title": "India overtakes Japan as world's fourth-largest economy", "summary": "Nominal GDP figures confirm India's ascent, driven by a technology services boom and growing domestic consumption.", "link": "https://ft.com/3", "author": "Benjamin Parkin"},
    {"publication": "Financial Times", "section": "Companies", "title": "LVMH signals luxury slowdown as aspirational buyers pull back", "summary": "The world's largest luxury group warned that demand from middle-class consumers is weakening, even as ultra-wealthy spending remains robust.", "link": "https://ft.com/4", "author": "Adrienne Klasa"},

    # Harvard Business Review
    {"publication": "Harvard Business Review", "section": "Latest", "title": "Why Your AI Strategy Needs a Human-Centered Redesign", "summary": "Companies rushing to deploy AI often overlook the organizational changes needed to capture value. A new framework puts people at the center of AI transformation.", "link": "https://hbr.org/1", "author": "Tsedal Neeley"},
    {"publication": "Harvard Business Review", "section": "Latest", "title": "The End of the 5-Year Strategic Plan", "summary": "In an era of constant disruption, rigid long-term planning is giving way to adaptive strategy frameworks that embrace uncertainty.", "link": "https://hbr.org/2", "author": "Martin Reeves"},
    {"publication": "Harvard Business Review", "section": "Latest", "title": "How Top CEOs Build Trust in a Polarized World", "summary": "Research on 200 global leaders reveals that the most effective CEOs navigate controversy by being transparent about values while staying operationally focused.", "link": "https://hbr.org/3", "author": "Frances Frei"},
]


def generate_sample_data():
    """Insert sample articles into the database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)

    now = datetime.now(timezone.utc)
    for i, a in enumerate(SAMPLE_ARTICLES):
        # Spread articles over the last 24 hours
        published = (now - timedelta(hours=i * 0.8)).isoformat()
        article_id = make_id(a['link'], a['title'])

        conn.execute("""
            INSERT OR IGNORE INTO articles
            (id, publication, section, title, link, summary, author, published, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (article_id, a['publication'], a['section'], a['title'], a['link'],
              a['summary'], a['author'], published, now.isoformat()))

        # FTS index
        conn.execute("""
            INSERT OR IGNORE INTO articles_fts(rowid, title, summary, publication)
            SELECT rowid, title, summary, publication FROM articles WHERE id = ?
        """, (article_id,))

    conn.commit()
    conn.close()
    print(f"Inserted {len(SAMPLE_ARTICLES)} sample articles")


if __name__ == "__main__":
    generate_sample_data()

    from dashboard_builder import build_dashboard

    # Sample AI briefing
    sample_briefing = """<p><strong>Markets & Macro:</strong> A risk-on mood dominated global markets, with the S&P 500 hitting record highs while bond traders increasingly price in a September rate cut. Oil's drop below $70 on OPEC+ production signals adds a deflationary tailwind, though the Fed's next move remains the key variable for H2 2026.</p>

<p><strong>AI Dominance Continues:</strong> The AI investment cycle shows no signs of slowing. OpenAI's $300B valuation, Microsoft's $10B AI run rate, and a looming Supreme Court copyright case all underscore that artificial intelligence remains the defining business story of the decade. The regulatory landscape is shifting too, with bipartisan Senate legislation gaining real traction.</p>

<p><strong>Geopolitical Realignment:</strong> Three stories point to a reshuffling of global economic power: India overtaking Japan as the world's fourth-largest economy, Europe's defence spending surge running into industrial capacity limits, and China's manufacturing rebound suggesting stimulus is working. The EU's coordinated tariff response adds another dimension to the evolving trade architecture.</p>

<p><strong>Worth Watching:</strong> LVMH's warning about weakening aspirational luxury demand could be an early signal of broader consumer softening in developed markets. Private credit's continued surge past $2 trillion in AUM represents a structural shift in how risk is intermediated â one that regulators are watching closely.</p>"""

    build_dashboard(ai_summary=sample_briefing)
    print("Sample dashboard generated!")
