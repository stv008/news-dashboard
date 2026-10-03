# Personal News Dashboard

A Python-powered daily news dashboard that aggregates headlines from your subscriptions:
The Economist, WSJ, NYT, Bloomberg, FT, and HBR.

## Quick Start

```bash
# Install dependencies
pip install feedparser anthropic

# Run the dashboard
python run.py

# Open dashboard.html in your browser
```

## Features

- **RSS Feed Aggregation**: Pulls latest articles from all 6 publications
- **Search**: Client-side instant search across all articles
- **AI Briefing** (optional): Claude-powered executive morning summary
- **SQLite Storage**: Articles are stored locally for history and search
- **Dark Theme**: Clean, modern dashboard UI

## AI Briefing (Optional)

To enable the AI-powered daily summary:

```bash
# Install the Anthropic SDK
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Run as normal
python run.py
```

Get your API key at: https://console.anthropic.com

## Usage Options

```bash
python run.py              # Fetch + build dashboard
python run.py --no-fetch   # Rebuild from existing data
python run.py --fetch-only # Only fetch, don't build dashboard
```

## Automate (Optional)

Add a cron job to generate your dashboard every morning:

```bash
# Edit crontab
crontab -e

# Add this line (runs at 7:00 AM daily)
0 7 * * * cd /path/to/news-dashboard && python3 run.py
```

On Windows, use Task Scheduler to run `python run.py` on a schedule.

## Files

- `run.py` - Main entry point
- `config.py` - RSS feed URLs and settings
- `fetcher.py` - RSS feed fetcher and SQLite storage
- `dashboard_builder.py` - HTML dashboard generator
- `summarizer.py` - Optional Claude AI briefing
- `generate_sample.py` - Generate sample data for preview
