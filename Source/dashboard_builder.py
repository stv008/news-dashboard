"""
Dashboard Builder
Generates a beautiful HTML dashboard from stored articles.
"""

import os
import sqlite3
import re
import html as html_mod
from datetime import datetime, timezone
from config import DB_PATH, OUTPUT_HTML, MAX_ARTICLES_PER_PUB, LOOKBACK_HOURS, PUB_COLORS


def esc(text):
    """Escape a string for safe HTML attribute and content insertion."""
    if not text:
        return ""
    return html_mod.escape(str(text), quote=True)


def sanitize_ai_html(raw_html):
    """Strip dangerous tags and event handlers from AI-generated HTML."""
    if not raw_html:
        return raw_html
    # Remove dangerous block-level elements entirely (with their content)
    raw_html = re.sub(
        r'<(script|iframe|object|embed|form|style)[^>]*>.*?</\1>',
        '', raw_html, flags=re.DOTALL | re.IGNORECASE
    )
    # Strip inline event handlers (onclick=, onload=, etc.)
    raw_html = re.sub(r'\s+on\w+\s*=\s*(?:"[^"]*"|\'[^\']*\')', '', raw_html, flags=re.IGNORECASE)
    # Strip javascript: URIs in href/src
    raw_html = re.sub(r'(href|src)\s*=\s*["\']javascript:[^"\']*["\']', '', raw_html, flags=re.IGNORECASE)
    return raw_html


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Dashboard - {{ date }}</title>
    <style>
        :root {
            --bg: #0f1117;
            --surface: #1a1d27;
            --surface2: #242836;
            --border: #2e3345;
            --text: #e4e6ef;
            --text-muted: #8b8fa3;
            --accent: #6c7aff;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }
        .header {
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            padding: 24px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            font-size: 22px;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        .header .date {
            color: var(--text-muted);
            font-size: 14px;
        }
        .header .right-section {
            display: flex;
            align-items: center;
            gap: 24px;
        }
        .header .stats {
            display: flex;
            gap: 20px;
            font-size: 13px;
            color: var(--text-muted);
        }
        .stats span { font-weight: 600; color: var(--accent); }
        .refresh-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 18px;
            background: var(--accent);
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.2s;
        }
        .refresh-btn:hover { opacity: 0.85; }
        .refresh-btn:active { transform: scale(0.97); }
        .refresh-btn.loading { opacity: 0.6; pointer-events: none; }
        .refresh-btn .icon { font-size: 15px; transition: transform 0.6s; }
        .refresh-btn.loading .icon { animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* Search */
        .search-bar {
            padding: 20px 40px;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
        }
        .search-bar input {
            width: 100%;
            max-width: 600px;
            padding: 12px 18px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--surface2);
            color: var(--text);
            font-size: 15px;
            outline: none;
            transition: border-color 0.2s;
        }
        .search-bar input:focus { border-color: var(--accent); }
        .search-bar input::placeholder { color: var(--text-muted); }
        .search-row {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .time-toggle {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 18px;
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-muted);
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
            flex-shrink: 0;
        }
        .time-toggle:hover { border-color: var(--accent); }
        .time-toggle .toggle-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--text-muted);
            transition: background 0.2s;
        }
        .time-toggle.active {
            border-color: var(--accent);
            color: var(--text);
        }
        .time-toggle.active .toggle-dot {
            background: #48bb78;
            box-shadow: 0 0 6px rgba(72, 187, 120, 0.4);
        }

        /* AI Summary section */
        .ai-summary {
            margin: 24px 40px;
            padding: 28px 32px;
            background: linear-gradient(135deg, #1e2235 0%, #1a1d27 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
        }
        .ai-summary h2 {
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 16px;
            color: var(--accent);
        }
        .ai-summary .summary-text {
            font-size: 14px;
            line-height: 1.7;
            color: var(--text);
        }
        .ai-summary .lead {
            font-size: 16px;
            font-weight: 500;
            line-height: 1.6;
            color: var(--text);
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        .briefing-item {
            margin-bottom: 18px;
            display: flex;
            align-items: flex-start;
            gap: 14px;
        }
        .priority-badge {
            flex-shrink: 0;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: var(--accent);
            color: #fff;
            font-size: 13px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-top: 2px;
        }
        .briefing-item[data-priority="1"] .priority-badge { background: #e53e3e; }
        .briefing-item[data-priority="2"] .priority-badge { background: #dd6b20; }
        .briefing-item[data-priority="3"] .priority-badge { background: var(--accent); }
        .briefing-content {
            flex: 1;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        .briefing-item:last-of-type .briefing-content { border-bottom: none; }
        .briefing-label {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.2px;
            color: var(--accent);
            margin-bottom: 2px;
        }
        .briefing-item[data-priority="1"] .briefing-label { color: #e53e3e; }
        .briefing-item[data-priority="2"] .briefing-label { color: #dd6b20; }
        .briefing-headline {
            font-size: 15px;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 4px;
        }
        .briefing-detail {
            font-size: 13px;
            line-height: 1.6;
            color: var(--text-muted);
        }
        .briefing-action {
            margin-top: 20px;
            padding: 16px 20px;
            background: rgba(108, 122, 255, 0.08);
            border-radius: 8px;
            border: 1px solid rgba(108, 122, 255, 0.15);
        }
        .briefing-action .briefing-label {
            margin-bottom: 10px;
        }
        .briefing-action ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .briefing-action li {
            font-size: 13px;
            line-height: 1.6;
            color: var(--text);
            padding: 4px 0 4px 20px;
            position: relative;
        }
        .briefing-action li::before {
            content: "▸";
            position: absolute;
            left: 0;
            color: var(--accent);
        }

        /* Main grid */
        .main { padding: 24px 40px; }
        .pub-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 24px;
        }
        .pub-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }
        .pub-header {
            padding: 14px 18px;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .pub-header .count {
            font-size: 11px;
            font-weight: 400;
            opacity: 0.8;
            background: rgba(255,255,255,0.15);
            padding: 2px 8px;
            border-radius: 10px;
        }
        .article-list { padding: 8px 0; }
        .article {
            padding: 12px 18px;
            border-bottom: 1px solid var(--border);
            transition: background 0.15s;
            cursor: pointer;
        }
        .article:last-child { border-bottom: none; }
        .article:hover { background: var(--surface2); }
        .article a {
            text-decoration: none;
            color: var(--text);
            font-size: 14px;
            font-weight: 500;
            display: block;
            line-height: 1.4;
        }
        .article a:hover { color: var(--accent); }
        .article .meta {
            display: flex;
            gap: 12px;
            margin-top: 4px;
            font-size: 11px;
            color: var(--text-muted);
        }
        .article .summary-preview {
            margin-top: 6px;
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.5;
            display: none;
        }
        .article.expanded .summary-preview { display: block; }
        .section-tag {
            font-size: 10px;
            padding: 1px 6px;
            border-radius: 4px;
            background: var(--surface2);
            color: var(--text-muted);
        }

        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 60px 40px;
            font-size: 15px;
            color: var(--text-muted);
        }
        .empty-state strong {
            color: var(--accent);
            cursor: pointer;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 30px;
            font-size: 12px;
            color: var(--text-muted);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header, .main, .search-bar, .ai-summary { padding-left: 16px; padding-right: 16px; }
            .pub-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Daily News Dashboard</h1>
            <div class="date">{{ date }} | Last updated: {{ updated_at }}</div>
        </div>
        <div class="right-section">
            <div class="stats">
                <div><span>{{ total_articles }}</span> articles</div>
                <div><span>{{ pub_count }}</span> publications</div>
            </div>
            <button class="refresh-btn" id="refreshBtn" onclick="refreshDashboard()">
                <span class="icon">&#x21bb;</span> Refresh
            </button>
        </div>
    </div>

    <div class="search-bar">
        <div class="search-row">
            <input type="text" id="search" placeholder="Search articles by title, summary, or publication..." autocomplete="off">
            <button class="time-toggle active" id="timeToggle" onclick="toggleTimeFilter()">
                <span class="toggle-dot"></span>
                <span class="toggle-label">Last {{ lookback_hours }}h</span>
            </button>
        </div>
    </div>

    {{ ai_summary_section }}

    <div class="main">
        <div class="pub-grid" id="pubGrid">
            {{ publication_cards }}
        </div>
        <div id="emptyState" class="empty-state" style="display:none;">
            No articles match the current filter. Click <strong onclick="toggleTimeFilter()">All articles</strong> to see older stories.
        </div>
    </div>

    <div class="footer">
        Generated {{ updated_at }} | Personal News Dashboard
    </div>

    <script>
    // State
    let timeFilterActive = true;

    function getCutoff() {
        return Date.now() - ({{ lookback_hours }} * 60 * 60 * 1000);
    }

    // Master filter: applies both search and time filter together
    function applyFilters() {
        const query = document.getElementById('search').value.toLowerCase().trim();
        const cutoff = getCutoff();
        let visibleCount = 0;

        document.querySelectorAll('.article').forEach(el => {
            let show = true;

            if (timeFilterActive) {
                const published = el.dataset.published || '';
                if (published) {
                    const pubTime = new Date(published).getTime();
                    if (!isNaN(pubTime) && pubTime < cutoff) show = false;
                }
            }

            if (show && query) {
                const title = (el.dataset.title || '').toLowerCase();
                const summary = (el.dataset.summary || '').toLowerCase();
                const pub = (el.dataset.pub || '').toLowerCase();
                if (!title.includes(query) && !summary.includes(query) && !pub.includes(query)) {
                    show = false;
                }
            }

            el.style.display = show ? '' : 'none';
            if (show) visibleCount++;
        });

        // Hide publication cards with zero visible articles, update counts
        document.querySelectorAll('.pub-card').forEach(card => {
            const visible = card.querySelectorAll('.article:not([style*="display: none"])');
            card.style.display = visible.length > 0 ? '' : 'none';
            const countEl = card.querySelector('.count');
            if (countEl) countEl.textContent = visible.length + ' articles';
        });

        // Update total count in header
        const statsSpans = document.querySelectorAll('.stats span');
        if (statsSpans.length > 0) statsSpans[0].textContent = visibleCount;

        // Empty state (#26)
        const emptyEl = document.getElementById('emptyState');
        if (emptyEl) emptyEl.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    function toggleTimeFilter() {
        const btn = document.getElementById('timeToggle');
        timeFilterActive = !timeFilterActive;
        btn.classList.toggle('active', timeFilterActive);
        btn.querySelector('.toggle-label').textContent = timeFilterActive ? 'Last {{ lookback_hours }}h' : 'All articles';
        applyFilters();
    }

    document.getElementById('search').addEventListener('input', applyFilters);
    applyFilters();

    // Keyboard shortcut: "/" focuses search, Escape clears it
    document.addEventListener('keydown', function(e) {
        if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
            e.preventDefault();
            document.getElementById('search').focus();
        } else if (e.key === 'Escape' && document.activeElement.id === 'search') {
            document.getElementById('search').value = '';
            applyFilters();
            document.activeElement.blur();
        }
    });

    // Toggle article summary on click
    document.querySelectorAll('.article').forEach(el => {
        el.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') return;
            this.classList.toggle('expanded');
        });
    });

    // Refresh button -- local: POST to /refresh; Pages: link to Actions UI
    function refreshDashboard() {
        const isLocal = ['localhost', '127.0.0.1', ''].includes(window.location.hostname);
        if (!isLocal) {
            window.open('https://github.com/stv008/news-dashboard/actions/workflows/refresh.yml', '_blank');
            return;
        }
        const btn = document.getElementById('refreshBtn');
        btn.classList.add('loading');
        btn.innerHTML = '<span class="icon">&#x21bb;</span> Refreshing...';

        // Record the generation time before we start
        let startGenTime = 0;
        fetch('/status').then(r => r.json()).then(d => { startGenTime = d.last_generated || 0; });

        fetch('/refresh', { method: 'POST' })
            .then(r => r.json())
            .then(() => {
                // Poll /status until last_generated changes (real completion detection)
                let attempts = 0;
                const poll = setInterval(() => {
                    attempts++;
                    if (attempts > 60) { // 3 min max
                        clearInterval(poll);
                        btn.classList.remove('loading');
                        btn.innerHTML = '<span class="icon">&#x21bb;</span> Refresh';
                        alert('Refresh is taking longer than expected. Check the terminal.');
                        return;
                    }
                    fetch('/status')
                        .then(r => r.json())
                        .then(data => {
                            if (data.last_generated > startGenTime) {
                                clearInterval(poll);
                                location.reload();
                            }
                        })
                        .catch(() => {});
                }, 3000);
            })
            .catch(() => {
                btn.classList.remove('loading');
                btn.innerHTML = '<span class="icon">&#x21bb;</span> Refresh';
                alert('Could not connect. Make sure you are running server.py (python server.py)');
            });
    }
    </script>
</body>
</html>"""


def get_articles():
    """Fetch recent articles from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT * FROM articles
            ORDER BY published DESC
        """)
        return [dict(row) for row in cursor.fetchall()]


def format_time(iso_str):
    """Format an ISO timestamp to a readable time string."""
    try:
        dt = datetime.fromisoformat(iso_str)
        now = datetime.now(timezone.utc)
        diff = now - dt
        hours = diff.total_seconds() / 3600
        if hours < 1:
            return f"{int(diff.total_seconds() / 60)}m ago"
        elif hours < 24:
            return f"{int(hours)}h ago"
        else:
            return dt.strftime("%b %d, %H:%M")
    except Exception:
        return ""


def build_publication_card(pub_name, articles):
    """Build HTML for a single publication card."""
    colors = PUB_COLORS.get(pub_name, {"bg": "#555", "text": "#fff"})

    articles_html = ""
    for a in articles[:MAX_ARTICLES_PER_PUB]:
        time_str = format_time(a['published'])
        section = esc(a.get('section', ''))
        section_tag = f'<span class="section-tag">{section}</span>' if section else ''
        summary_text = esc(a.get('summary', '')[:200])
        title = esc(a.get('title', ''))
        link = esc(a.get('link', ''))
        author = esc(a.get('author', ''))
        published = esc(a.get('published', ''))

        articles_html += f"""
        <div class="article" data-title="{title}" data-summary="{summary_text}" data-pub="{esc(pub_name)}" data-published="{published}">
            <a href="{link}" target="_blank" rel="noopener">{title}</a>
            <div class="meta">
                {section_tag}
                <span>{time_str}</span>
                {'<span>' + author + '</span>' if author else ''}
            </div>
            <div class="summary-preview">{summary_text}</div>
        </div>"""

    return f"""
    <div class="pub-card">
        <div class="pub-header" style="background:{colors['bg']};color:{colors['text']}">
            {pub_name}
            <span class="count">{len(articles)} articles</span>
        </div>
        <div class="article-list">
            {articles_html}
        </div>
    </div>"""


def build_dashboard(ai_summary=None):
    """Generate the full HTML dashboard."""
    articles = get_articles()

    # Group by publication
    pubs = {}
    for a in articles:
        pub = a['publication']
        if pub not in pubs:
            pubs[pub] = []
        pubs[pub].append(a)

    # Build publication cards (ordered by PUB_COLORS keys for consistency)
    pub_order = list(PUB_COLORS.keys())
    cards_html = ""
    for pub in pub_order:
        if pub in pubs:
            cards_html += build_publication_card(pub, pubs[pub])

    # AI summary section
    ai_html = ""
    if ai_summary:
        ai_html = f"""
    <div class="ai-summary">
        <h2>AI Daily Briefing</h2>
        <div class="summary-text">{sanitize_ai_html(ai_summary)}</div>
    </div>"""

    now = datetime.now(timezone.utc)
    html_output = TEMPLATE
    html_output = html_output.replace("{{ date }}", now.strftime("%A, %B %d, %Y"))
    html_output = html_output.replace("{{ updated_at }}", now.strftime("%H:%M UTC"))
    html_output = html_output.replace("{{ total_articles }}", str(len(articles)))
    html_output = html_output.replace("{{ pub_count }}", str(len(pubs)))
    html_output = html_output.replace("{{ publication_cards }}", cards_html)
    html_output = html_output.replace("{{ ai_summary_section }}", ai_html)
    html_output = html_output.replace("{{ lookback_hours }}", str(LOOKBACK_HOURS))

    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"Dashboard saved to {OUTPUT_HTML}")
    print(f"  {len(articles)} articles from {len(pubs)} publications")
    return OUTPUT_HTML


if __name__ == "__main__":
    build_dashboard()
