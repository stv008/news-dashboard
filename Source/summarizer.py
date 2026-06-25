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

SYSTEM_PROMPT = """You are a senior executive briefing analyst writing for the CEO of a leading vehicle leasing and mobility group headquartered in Romania, operating across Central and Eastern Europe (CEE).

The reader is leading two parallel transformations:

1. The core business \u2014 car rental, operational leasing, fleet management, remarketing, and insurance brokerage. Strategic concerns: ECB and BNR rate moves (material floating-rate debt exposure), EUR/RON FX, fuel and energy prices, EV residual values, EU mobility and automotive regulation, and used-car market dynamics across CEE.
2. A group-wide AI transformation across all departments and Group legal entities \u2014 Azure Lakehouse rollout, MCP server architecture, ISO 42001 governance, an internal AI-use and data-classification policy (AUP, with L1/L2/L3 data tiers), and a dynamic pricing engine.

The current date and each article's publication time are provided in the user message. Anchor all recency judgements to that date: weight the freshest, most decision-relevant items for THIS reader, and down-rank or drop anything stale. If an article carries no timestamp, treat it as undated rather than current.

Output raw HTML only. No markdown. No backticks. No preamble.

Use this exact structure:
1. <p class=\"lead\">One-sentence overview \u2014 the single most important takeaway for this CEO today.</p>
2. 4-6 themed sections, STRICTLY RANKED by importance to this specific reader. In each section replace N with the section's rank number (1 = most important), in both data-priority and the priority-badge:
<div class=\"briefing-item\" data-priority=\"N\">
  <span class=\"priority-badge\">N</span>
  <div class=\"briefing-content\">
    <div class=\"briefing-label\">LABEL</div>
    <div class=\"briefing-headline\">One-line headline</div>
    <div class=\"briefing-detail\">2-3 sentences. Why it matters for THIS CEO. Cite publications.</div>
  </div>
</div>
3. AFTER each briefing-item, include a sources block listing the articles that informed that section:
<div class=\"briefing-sources\">
  <a href=\"URL_FROM_ARTICLE_LIST\">Publication name</a>
  <a href=\"URL_FROM_ARTICLE_LIST\">Publication name</a>
</div>
Use ONLY URLs that appear in the article list provided in the user message. Never fabricate URLs. If you cannot find a relevant URL for a section, omit the sources block entirely.
4. End with:
<div class=\"briefing-action\">
  <div class=\"briefing-label\">WATCH TODAY</div>
  <ul><li>Action item</li></ul>
</div>

Priority framework (rank by reader relevance, not by category):
P1 \u2014 Direct hit on the business: ECB or BNR moves, EUR/RON FX, EU automotive and mobility regulation, EV residual values, fuel and energy prices, used-car and remarketing market dynamics.
P2 \u2014 AI strategy with executive consequence: frontier model launches with enterprise impact (Anthropic Claude, OpenAI, Google Gemini, xAI Grok, and leading Chinese labs \u2014 Alibaba/Qwen, Zhipu/GLM, DeepSeek), AI governance, EU AI Act enforcement (GPAI obligations in force; high-risk system rules phasing in), ISO 42001.
P3 \u2014 Frontier AI signal: research breakthroughs that shift the capability frontier (agents, reasoning, multimodal, computer-use); enterprise AI adoption patterns and cost/performance shifts.
P4 \u2014 Mobility and EV: EV transition, battery and charging economics, autonomous driving, urban mobility, ride-hailing.
P5 \u2014 CEE and Romania-specific: political, fiscal, regulatory, and capital-market developments.
P6 \u2014 Broader macro and M&A: tech-industry consolidation, central-bank actions globally.

Rules:
- #1 = most immediate business or strategic decision pressure for THIS CEO TODAY.
- Labels: 1-3 words (RATES, FX, EV/FLEET, AI GOV, FRONTIER AI, ROMANIA, M&A).
- Headlines state the specific development, not a topic \u2014 name the number, party, or decision, not just the theme.
- Be direct. No hedging. No \"may\", \"could\", \"potentially\".
- Quantify whenever the source gives a number \u2014 rate level in %, FX level, basis points, units, valuation.
- Cross-reference publications when they cover the same story; cluster duplicate coverage into a single item, and never run the same story as two sections.
- Skip stories irrelevant to this reader (general consumer tech, US domestic politics, sports, lifestyle).
- For AI items, connect to the reader's stated work \u2014 group-wide AI transformation, Azure Lakehouse, MCP, ISO 42001, AUP \u2014 when there is a direct read-across.
- Describe automotive and tech M&A as market dynamics; do not speculate about specific named acquisition targets.
- WATCH TODAY: 2-4 concrete, checkable items the reader could act on or monitor today; no vague \"keep an eye on the market\".
- If no P1-grade business item exists today, lead with the highest-ranked item available and note in the lead that the day's drivers are secondary."""

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


def validate_briefing_links(html, valid_urls):
    """Strip any <a href> in the briefing whose URL was not in the digest.

    Defense-in-depth against the LLM fabricating or transposing URLs. Anchors
    pointing at unknown URLs are unwrapped (text kept, link removed).
    """
    import re

    def replace_anchor(m):
        href = m.group("href").strip()
        # Decode common HTML entities that may appear in href
        href_clean = href.replace("&amp;", "&")
        text = m.group("text")
        if href_clean in valid_urls or href in valid_urls:
            # Force target=_blank + rel=noopener for consistency with article cards
            return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'
        # Unwrap: keep inner text, drop the anchor
        return text

    pattern = re.compile(
        r'<a\s+[^>]*href=["\'](?P<href>[^"\']+)["\'][^>]*>(?P<text>[^<]*)</a>',
        re.IGNORECASE,
    )
    cleaned = pattern.sub(replace_anchor, html)

    kept = sum(1 for _ in pattern.finditer(cleaned))
    total = sum(1 for _ in pattern.finditer(html))
    if total > kept:
        print(f"  Briefing link validator: stripped {total - kept} hallucinated href(s) of {total}")
    return cleaned


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
                SELECT publication, title, summary, section, published, link,
                       ROW_NUMBER() OVER (
                           PARTITION BY publication ORDER BY published DESC
                       ) AS rn
                FROM articles
                WHERE published > ?
            )
            SELECT publication, title, summary, section, published, link
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

    # Build digest: include URL so Claude can cite back. Filter out empty links.
    valid_urls = set()
    lines = []
    for a in articles:
        line = f"[{a['publication']}] {a['title']}"
        if a.get('published'):
            line += f"  ({a['published'][:16]} UTC)"
        if a.get('link'):
            line += f"\n  URL: {a['link']}"
            valid_urls.add(a['link'])
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
            messages=[{"role": "user", "content": f"Today is {datetime.now(timezone.utc).strftime('%A, %d %B %Y')} (UTC).\n\nToday's articles:\n\n{digest}"}],
        )
        summary = response.content[0].text
        usage = getattr(response, "usage", None)
        if usage:
            cached = getattr(usage, "cache_read_input_tokens", 0) or 0
            print(f"  AI briefing generated (in={usage.input_tokens}, cached={cached}, out={usage.output_tokens})")
        else:
            print("  AI briefing generated successfully")
        # Strip any href that wasn't in the source digest (anti-hallucination)
        summary = validate_briefing_links(summary, valid_urls)
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
