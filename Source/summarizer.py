"""
AI Summarizer (Optional)
Uses Claude API to generate a daily briefing summary.
Requires ANTHROPIC_API_KEY environment variable.
"""

import os
import sqlite3

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

from config import DB_PATH, CLAUDE_MODEL, MAX_ARTICLES_TO_SUMMARIZE, MAX_BRIEFING_TOKENS

SYSTEM_PROMPT = """You are a senior executive briefing analyst. Your reader is the CEO of a \u20ac200M+ vehicle leasing and mobility company headquartered in Romania, operating across CEE.

Output raw HTML only. No markdown. No backticks. No preamble.

Use this exact structure:

1. <p class="lead">One-sentence overview \u2014 the single most important takeaway.</p>

2. 3-5 themed sections, STRICTLY RANKED by importance to this specific reader:

<div class="briefing-item" data-priority="N">
  <span class="priority-badge">N</span>
  <div class="briefing-content">
    <div class="briefing-label">LABEL</div>
    <div class="briefing-headline">One-line headline</div>
    <div class="briefing-detail">2-3 sentences. Why it matters. Cite publications.</div>
  </div>
</div>

3. End with:
<div class="briefing-action">
  <div class="briefing-label">WATCH TODAY</div>
  <ul><li>Action item</li></ul>
</div>

Priority framework (rank by relevance to reader, not by category number):
P1 \u2014 Interest rates, central bank policy (ECB, BNR), bond markets, credit conditions
P2 \u2014 FX and currency risk (EUR/RON, USD/EUR, sovereign spreads)
P3 \u2014 Automotive, fleet, leasing, mobility, EV transition, fuel/energy prices
P4 \u2014 AI adoption in enterprise, tech with direct business impact
P5 \u2014 EU/CEE regulation, trade policy, Romania-specific political or fiscal risk
P6 \u2014 M&A, corporate strategy, leadership

Rules:
- #1 = most immediate business impact for a fleet/leasing CEO
- Labels: 1-3 words (RATES, FX, FLEET, ENERGY, AI, EU REGULATION, M&A)
- Be direct. No hedging.
- Cross-reference publications when they cover the same story
- Skip stories irrelevant to this reader"""


def is_available():
    """Check if Claude API summarization is available."""
    return HAS_ANTHROPIC and os.environ.get("ANTHROPIC_API_KEY")


def get_top_articles():
    """Get recent articles for summarization."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT publication, title, summary, section
            FROM articles
            ORDER BY published DESC
            LIMIT ?
        """, (MAX_ARTICLES_TO_SUMMARIZE,))
        return [dict(row) for row in cursor.fetchall()]


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
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Today's articles:\n\n{digest}"}],
        )
        summary = response.content[0].text
        print("  AI briefing generated successfully")
        return summary
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
