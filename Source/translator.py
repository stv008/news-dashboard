"""
Article Translator (Optional)
Translates titles + summaries of non-English publications to English using
Claude Haiku, at build time. Originals are preserved in the
title_original / summary_original columns so the change is reversible and a
"translated from X" hint can be shown on the card.

Requires ANTHROPIC_API_KEY environment variable. If unavailable, the pipeline
silently leaves foreign-language text untouched.
"""

import os
import json
import sqlite3

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

from config import (
    DB_PATH, PUB_LANGUAGES, TRANSLATE_MODEL,
    TRANSLATE_BATCH_SIZE, TRANSLATE_MAX_TOKENS, MAX_SUMMARY_LENGTH,
)

SYSTEM_PROMPT = (
    "You are a professional translator for a financial/tech news dashboard. "
    "Translate each article's title and summary into natural, concise English. "
    "Preserve proper nouns, company names, product names, and tickers exactly. "
    "Do not editorialize, add, or omit information. Keep the journalistic tone. "
    "Return ONLY a JSON array, no prose, no markdown fences. Each element must be "
    '{"id": "<id>", "title": "<english title>", "summary": "<english summary>"} '
    "matching the input ids exactly. If a summary is empty, return an empty string."
)


def is_available():
    """Check if Claude API translation is available."""
    return HAS_ANTHROPIC and os.environ.get("ANTHROPIC_API_KEY")


def _ensure_columns(conn):
    """Add title_original / summary_original columns if they don't exist yet."""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(articles)").fetchall()}
    if "title_original" not in cols:
        conn.execute("ALTER TABLE articles ADD COLUMN title_original TEXT")
    if "summary_original" not in cols:
        conn.execute("ALTER TABLE articles ADD COLUMN summary_original TEXT")
    conn.commit()


def _get_untranslated(conn):
    """Fetch foreign-language articles not yet translated (title_original IS NULL)."""
    pubs = list(PUB_LANGUAGES.keys())
    if not pubs:
        return []
    placeholders = ",".join("?" * len(pubs))
    cursor = conn.execute(
        f"""
        SELECT id, publication, title, summary
        FROM articles
        WHERE publication IN ({placeholders})
          AND title_original IS NULL
        """,
        pubs,
    )
    return [dict(r) for r in cursor.fetchall()]


def _translate_batch(client, batch):
    """Translate one batch of article dicts. Returns {id: {title, summary}}."""
    items = [
        {
            "id": a["id"],
            "language": PUB_LANGUAGES.get(a["publication"], "the source language"),
            "title": a["title"] or "",
            "summary": (a["summary"] or "")[:MAX_SUMMARY_LENGTH],
        }
        for a in batch
    ]
    user_msg = (
        "Translate the following articles to English. Each item lists its source "
        "language.\n\n" + json.dumps(items, ensure_ascii=False)
    )
    response = client.messages.create(
        model=TRANSLATE_MODEL,
        max_tokens=TRANSLATE_MAX_TOKENS,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = response.content[0].text.strip()
    # Be tolerant of stray fences or prose around the JSON array.
    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("no JSON array in translation response")
    parsed = json.loads(raw[start:end + 1])
    return {
        item["id"]: {"title": item.get("title", ""), "summary": item.get("summary", "")}
        for item in parsed
        if isinstance(item, dict) and "id" in item
    }


def _apply_translation(conn, article_id, en_title, en_summary):
    """Write English into title/summary, preserving the original; sync FTS."""
    row = conn.execute(
        "SELECT rowid, title, summary, publication FROM articles WHERE id = ?",
        (article_id,),
    ).fetchone()
    if not row:
        return
    rowid, orig_title, orig_summary, pub = row
    en_title = (en_title or orig_title).strip()
    en_summary = (en_summary or "").strip()
    conn.execute(
        """
        UPDATE articles
        SET title_original = ?, summary_original = ?, title = ?, summary = ?
        WHERE id = ?
        """,
        (orig_title, orig_summary, en_title, en_summary, article_id),
    )
    # Keep the FTS index in sync (same delete-then-reinsert pattern as prune).
    conn.execute("DELETE FROM articles_fts WHERE rowid = ?", (rowid,))
    conn.execute(
        """
        INSERT OR IGNORE INTO articles_fts(rowid, title, summary, publication)
        SELECT rowid, title, summary, publication FROM articles WHERE id = ?
        """,
        (article_id,),
    )


def translate_new_articles():
    """Translate untranslated foreign-language articles to English in place."""
    if not is_available():
        if not HAS_ANTHROPIC:
            print("  Note: Install 'anthropic' for translation (pip install anthropic)")
        elif not os.environ.get("ANTHROPIC_API_KEY"):
            print("  Note: Set ANTHROPIC_API_KEY to enable translation")
        return 0

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        _ensure_columns(conn)
        pending = _get_untranslated(conn)
        if not pending:
            print("  No new foreign-language articles to translate")
            return 0

        client = anthropic.Anthropic()
        translated = 0
        for i in range(0, len(pending), TRANSLATE_BATCH_SIZE):
            batch = pending[i:i + TRANSLATE_BATCH_SIZE]
            try:
                results = _translate_batch(client, batch)
            except anthropic.AuthenticationError as e:
                print(f"  ERROR: Invalid ANTHROPIC_API_KEY — {e}")
                break
            except Exception as e:
                print(f"  Warning: translation batch failed ({len(batch)} articles): {e}")
                continue
            for a in batch:
                t = results.get(a["id"])
                if not t:
                    continue
                _apply_translation(conn, a["id"], t.get("title"), t.get("summary"))
                translated += 1
            conn.commit()

        by_lang = {}
        for a in pending:
            lang = PUB_LANGUAGES.get(a["publication"], "?")
            by_lang[lang] = by_lang.get(lang, 0) + 1
        breakdown = ", ".join(f"{k}: {v}" for k, v in sorted(by_lang.items()))
        print(f"  Translated {translated}/{len(pending)} articles to English ({breakdown})")
        return translated


if __name__ == "__main__":
    if is_available():
        translate_new_articles()
    else:
        print("Claude API not configured. Set ANTHROPIC_API_KEY to enable translation.")
