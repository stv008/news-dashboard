"""
RSS Feed Fetcher
Pulls articles from all configured publications.
"""

import feedparser
import time
import sqlite3
import hashlib
import html
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from config import (
    FEEDS, LOOKBACK_HOURS, DB_PATH, USER_AGENT,
    FETCH_TIMEOUT_SECONDS, FETCH_DELAY_SECONDS, MAX_SUMMARY_LENGTH,
    MAX_ARTICLE_AGE_DAYS, MAX_FETCH_RETRIES,
)


def init_db():
    """Create the SQLite database and articles table if they don't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id TEXT PRIMARY KEY,
                publication TEXT NOT NULL,
                section TEXT,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                summary TEXT,
                author TEXT,
                published TEXT,
                fetched_at TEXT NOT NULL,
                ai_summary TEXT
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_published ON articles(published DESC)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_publication ON articles(publication)
        """)
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(
                title, summary, publication, content='articles', content_rowid='rowid'
            )
        """)
        conn.commit()


def make_id(link, title):
    """Generate a unique ID for an article based on link and title."""
    raw = f"{link}|{title}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def clean_html(text):
    """Strip HTML tags and decode entities from a string."""
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_date(entry):
    """Extract and normalize the publication date from a feed entry."""
    for field in ['published_parsed', 'updated_parsed']:
        parsed = entry.get(field)
        if parsed:
            try:
                dt = datetime(*parsed[:6], tzinfo=timezone.utc)
                return dt.isoformat()
            except Exception:
                pass
    return datetime.now(timezone.utc).isoformat()


def fetch_with_retry(url):
    """Fetch a URL with exponential backoff retries. Raises on final failure."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_err = None
    for attempt in range(MAX_FETCH_RETRIES):
        try:
            response = urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_SECONDS)
            return response.read()
        except Exception as e:
            last_err = e
            if attempt < MAX_FETCH_RETRIES - 1:
                time.sleep(FETCH_DELAY_SECONDS * (2 ** attempt))
    raise last_err


def fetch_feed(pub_name, feed_info):
    """Fetch and parse a single RSS feed. Returns list of article dicts."""
    url = feed_info["url"]
    section = feed_info.get("section", "General")
    articles = []
    try:
        try:
            raw_bytes = fetch_with_retry(url)
        except Exception as e:
            print(f"  Warning: Could not fetch {pub_name}/{section}: {e}")
            return []
        feed = feedparser.parse(raw_bytes)
        if feed.bozo and not feed.entries:
            try:
                feed = feedparser.parse(raw_bytes.decode("utf-8", errors="replace"))
            except Exception:
                pass
            if not feed.entries:
                print(f"  Warning: Could not parse {pub_name}/{section}: {feed.bozo_exception}")
                return []
        cutoff = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
        for entry in feed.entries:
            title = clean_html(entry.get('title', ''))
            if not title:
                continue
            link = entry.get('link', '')
            summary = clean_html(entry.get('summary', entry.get('description', '')))
            author = entry.get('author', '')
            published = parse_date(entry)
            try:
                pub_dt = datetime.fromisoformat(published)
                if pub_dt < cutoff:
                    continue
            except Exception:
                pass
            article = {
                'id': make_id(link, title),
                'publication': pub_name,
                'section': section,
                'title': title,
                'link': link,
                'summary': summary[:MAX_SUMMARY_LENGTH] if summary else '',
                'author': author,
                'published': published,
                'fetched_at': datetime.now(timezone.utc).isoformat(),
            }
            articles.append(article)
    except Exception as e:
        print(f"  Error fetching {pub_name}/{section}: {e}")
    return articles


def save_articles(articles):
    """Save articles to SQLite, skipping duplicates."""
    new_count = 0
    with sqlite3.connect(DB_PATH) as conn:
        for a in articles:
            try:
                cursor = conn.execute("""
                    INSERT OR IGNORE INTO articles
                    (id, publication, section, title, link, summary, author, published, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (a['id'], a['publication'], a['section'], a['title'], a['link'],
                      a['summary'], a['author'], a['published'], a['fetched_at']))
                if cursor.rowcount > 0:
                    conn.execute("""
                        INSERT OR IGNORE INTO articles_fts(rowid, title, summary, publication)
                        SELECT rowid, title, summary, publication FROM articles WHERE id = ?
                    """, (a['id'],))
                    new_count += 1
            except sqlite3.IntegrityError:
                pass
            except Exception as e:
                print(f"  Warning: Failed to save article '{a.get('title', '?')[:50]}': {e}")
        conn.commit()
    return new_count


def prune_old_articles():
    """Remove articles older than MAX_ARTICLE_AGE_DAYS to keep the DB lean."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_ARTICLE_AGE_DAYS)
    cutoff_iso = cutoff.isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT rowid FROM articles WHERE published < ?", (cutoff_iso,)
        ).fetchall()
        if not rows:
            return
        rowids = [r[0] for r in rows]
        # Remove from FTS index incrementally before deleting from content table
        conn.executemany("DELETE FROM articles_fts WHERE rowid = ?", [(r,) for r in rowids])
        conn.execute("DELETE FROM articles WHERE published < ?", (cutoff_iso,))
        conn.commit()
        print(f"  Pruned {len(rowids)} articles older than {MAX_ARTICLE_AGE_DAYS} days")


def fetch_all():
    """Fetch articles from all configured publications."""
    init_db()
    prune_old_articles()
    total_new = 0
    for pub_name, feeds in FEEDS.items():
        print(f"Fetching {pub_name}...")
        pub_articles = []
        for feed_info in feeds:
            articles = fetch_feed(pub_name, feed_info)
            pub_articles.extend(articles)
            time.sleep(FETCH_DELAY_SECONDS)
        new = save_articles(pub_articles)
        total_new += new
        print(f"  Got {len(pub_articles)} articles, {new} new")
    print(f"\nTotal new articles saved: {total_new}")
    return total_new


if __name__ == "__main__":
    fetch_all()
