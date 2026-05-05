"""
AI Summarizer (Optional)
Uses Claude API to generate a daily briefing summary.
Requires ANTHROPIC_API_KEY environment variable.
"""

import os
import sqlite3
from datetime import datetime, timedelta, timezone

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

from config import DB_PATH, CLAUDE_MODEL, MAX_ARTICLES_TO_SUMMARIZE, MAX_BRIEFING_TOKENS

SYSTEM_PROMPT = """You are a senior executive briefing analyst writing for the CEO of a \u20ac200M+ vehicle leasing and mobility company headquartered in Romania, operating across CEE.

The reader is leading two parallel transformations:
1. The core business \u2014 car rental, operational leasing, fleet management, remarketing, insurance brokerage. Strategic concerns: ECB and BNR rate moves (\u20ac200M debt structure), EUR/RON FX, fuel and energy prices, EV residual values, EU mobility regulation, used-car market dynamics.
2. AI transformation across 19 departments \u2014 Azure Lakehouse rollout, MCP server architecture, ISO 42001 governance, internal data classification policy (AUP), and a dynamic pricing engine.

Output raw HTML only. No markdown. No backticks. No preamble.

Use this exact structure:

1. <p class=\"lead\">One-sentence overview \u2014 the single most important takeaway for this CEO today.</p>

2. 4-6 themed sections, STRICTLY RANKED by importance to this specific reader:

<div class=\"briefing-item\" data-priority=\"N\">
  <span class=\"priority-badge\">N</span>
  <div class=\"briefing-content\">
    <div class=\"briefing-label\">LABEL</div>
    <div class=\"briefing-headline\">One-line headline</div>
    <div class=\"briefing-detail\">2-3 sentences. Why it matters for THIS CEO. Cite publications.</div>
  </div>
</div>

3. End with:
<div class=\"briefing-action\">
  <div class=\"briefing-label\">WATCH TODAY</div>
  <ul><li>Action item</li></ul>
</div>

Priority framework (rank by reader relevance, not by category):
P1 \u2014 Direct hit on Autonom: ECB or BNR moves, EUR/RON FX, EU automotive regulation, EV residual values, fuel and energy
P2 \u2014 AI strategy with executive consequence: model launches with enterprise impact (Anthropic Claude, OpenAI, Gemini), AI governance, EU AI Act enforcement, ISO 42001
P3 \u2014 Frontier AI signal: research breakthroughs that shift the capability frontier (agents, reasoning, multimodal); enterprise AI adoption patterns
P4 \u2014 Mobility and EV: EV transition, autonomous driving, urban mobility, ride-hailing
P5 \u2014 CEE and Romania-specific: political, fiscal, regulatory developments
P6 \u2014 Broader macro and M&A: tech industry consolidation, central bank actions globally

Rules:
- #1 = most immediate business or strategic decision pressure for THIS CEO TODAY
- Labels: 1-3 words (RATES, FX, EV/FLEET, AI GOV, FRONTIER AI, ROMANIA, M&A)
- Be direct. No hedging. No \"may\", \"could\", \"potentially\".
- Cross-reference publications when they cover the same story
- Skip stories irrelevant to this reader (general consumer tech, US politics, sports, lifestyle)
- For AI items, connect to the reader's stated work \u2014 19-department transformation, Azure Lakehouse, MCP, ISO 42001 \u2014 when there is a direct read-across
- Describe automotive M&A as market dynamics; do not speculate about specific named acquisition targets"""

# Per-publication weight cap for the briefing sample.
# Higher = more articles from that source make it into the brief.
# Default for unlisted publications: 1.
PUB_WEIGHTS = {
    # Premium financial / macro
    "Financial Times": 4, "Bloomberg": 4, "Wall Street Journal": 4,
    "The Economist": 4, "Harvard Business Review": 3, "New York Times": 3,
    # Frontier labs (AI signal)
    "OpenAI": 4, "Google DeepMind": 4, "Apple ML Research": 3,
    "Allen AI (Ai2)": 3, "Hugging Face": 3, "Google Research": 3,
    "NVIDIA Research": 2, "MIT News \u2014 AI": 2, "MIT CSAIL": 2,
    "Berkeley AI Research": 2, "LangChain Changelog": 2,
    # Analysis & strategy (synthesis is gold)
    "Stratechery": 4, "Import AI": 4, "One Useful Thing (Mollick)": 3,
    "Interconnects (Lambert)": 3, "Benedict Evans": 3, "Latent Space": 3,
    "Last Week in AI": 3, "Marginal Revolution": 2,
    "Astral Codex Ten": 2, "AI Snake Oil": 2, "Gary Marcus": 2,
    "The Algorithmic Bridge": 2, "Eric Topol \u2014 Ground Truths": 2,
    "The Gradient": 2,
    # Tech press
    "MIT Technology Review": 3, "The Decoder": 2, "TechCrunch \u2014 AI": 2,
    "The Verge \u2014 AI": 2, "Wired \u2014 AI": 2, "Ars Technica \u2014 AI": 2,
    "VentureBeat \u2014 AI": 2, "IEEE Spectrum \u2014 AI": 2,
    # EU / Mobility / Romania
    "Politico Europe": 3, "EU AI Act Tracker": 3, "CSET (Georgetown)": 2,
    "Electrek": 2, "profit.ro": 3, "start-up.ro": 2,
    # Secondary
    "Axios \u2014 Technology": 2, "CNBC \u2014 Technology": 2,
    # Lower-signal aggregators / community
    "Hacker News": 2, "Techmeme": 2,
    # Default fallback for unlisted: 1
}
DEFAULT_PUB_WEIGHT = 1
BRIEFING_LOOKBACK_HOURS = 36  # Articles older than this are stale for a daily brief


def is_available():
    """Check if Claude API summarization is available."""
    return HAS_ANTHROPIC and os.environ.get("ANTHROPIC_API_KEY")


def get_top_articles():
    """Sample articles for the briefing: top N per publication, weight-capped.

    Why not ORDER BY published DESC LIMIT 30: a single firehose publication
    (arXiv-style or a batch-publishing wire service) would dominate the sample
    and starve every other source. We instead take the freshest few from each
    publication, then cap the total.
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=BRIEFING_LOOKBACK_HOURS)).isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        # Top 4 per publication via window function; we'll downsample below.
        cursor = conn.execute("""
            WITH ranked AS (
                SELECT publication, title, summary, section, published,
                       ROW_NUMBER() OVER (
                           PARTITION BY publication ORDER BY published DESC
                       ) AS rn
                FROM articles
                WHERE published > ?
            )
            SELECT publication, title, summary, section, published
            FROM ranked
            WHERE rn <= 4
            ORDER BY publication, published DESC
        """, (cutoff,))
        rows = [dict(r) for r in cursor.fetchall()]

    by_pub = {}
    for r in rows:
        by_pub.setdefault(r["publication"], []).append(r)

    sampled = []
    for pub, articles in by_pub.items():
        weight = PUB_WEIGHTS.get(pub, DEFAULT_PUB_WEIGHT)
        sampled.extend(articles[:weight])

    # Sort the final sample newest-first so the digest reads chronologically
    sampled.sort(key=lambda a: a["published"], reverse=True)
    return sampled[:MAX_ARTICLES_TO_SUMMARIZE]


def generate_briefing():
    """Generate an AI-powered daily briefing using Claude."""
    if not is_available():
        if not HAS_ANTHROPIC:
            print("  Note: Install 'anthropic' package for AI summaries (pip install anthropic)")
        elif not os.environ.get("ANTHROPIC_API_KEY"):
            print("  Note: Set ANTHROPIC_API_KEY env var for AI summaries")
        return None

    articles = get_top_articles()
    if not articles:
        return None

    lines = []
    for a in articles:
        line = f"[{a['publication']}] {a['title']}"
        if a['summary']:
            line += f"\n  {a['summary'][:250]}"
        lines.append(line)
    digest = "\n\n".join(lines)

    client = anthropic.Anthropic()

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_BRIEFING_TOKENS,
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": f"Today's articles:\n\n{digest}"}],
        )
        summary = response.content[0].text
        usage = getattr(response, "usage", None)
        if usage:
            cached = getattr(usage, "cache_read_input_tokens", 0) or 0
            print(f"  AI briefing generated (in={usage.input_tokens}, cached={cached}, out={usage.output_tokens})")
        else:
            print("  AI briefing generated successfully")
        return summary
    except anthropic.AuthenticationError as e:
        print(f"  ERROR: Invalid ANTHROPIC_API_KEY — {e}")
        return None
    except anthropic.RateLimitError as e:
        print(f"  Warning: Claude rate limit hit — {e}")
        return None
    except anthropic.APIConnectionError as e:
        print(f"  Warning: Could not reach Claude API — {e}")
        return None
    except Exception as e:
        print(f"  Warning: AI summary failed: {e}")
        return None


if __name__ == "__main__":
    if is_available():
        result = generate_briefing()
        if result:
            print(result)
    else:
        print("Claude API not configured. Set ANTHROPIC_API_KEY to enable.")
