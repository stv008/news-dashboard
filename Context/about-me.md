# About This Project

## Purpose

Personal daily news dashboard that aggregates headlines and articles from Marius's six paid subscriptions into a single interface with search and AI-powered briefings.

## Owner

* Marius Stefan, CEO & Founder, Autonom
* Solo user â this is a personal productivity tool, not a team-facing product

## Subscriptions Covered

* The Economist
* Wall Street Journal (WSJ)
* New York Times (NYT)
* Bloomberg
* Financial Times (FT)
* Harvard Business Review (HBR)

## What It Does

1. **RSS Ingestion** â Pulls latest headlines and summaries from all 6 publications via RSS feeds
2. **SQLite Storage** â Stores articles locally for history, deduplication, and search
3. **Search** â Client-side instant search across all articles by title, summary, or publication
4. **AI Briefing** (optional) â Claude API generates an executive morning summary highlighting the 3-5 most important stories and cross-cutting themes
5. **HTML Dashboard** â Dark-themed, responsive dashboard opened in a local browser

## Technical Setup

* Python 3.10+
* Dependencies: `feedparser`, `anthropic` (optional)
* Database: SQLite (local, no server needed)
* Output: Static HTML file opened in browser
* Runs on: Lenovo ThinkPad X1 Carbon, Windows
* Optional: Claude API key from console.anthropic.com (billed separately from Pro/Team subscriptions)

## Reading Priorities

Marius is a hands-on CEO in the mobility/leasing sector. Topics of particular interest:

* Macroeconomics, interest rates, central bank policy
* Automotive and mobility industry
* AI adoption in enterprise
* European business and regulation
* M&A and corporate strategy
* Leadership and management thinking (HBR)

## Future Roadmap

* Authenticated scraping for full article text (beyond RSS summaries)
* Topic clustering and personalized relevance ranking
* Scheduled daily generation (cron / Windows Task Scheduler)
* Email delivery of morning briefing
