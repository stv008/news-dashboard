#!/usr/bin/env python3
"""
News Dashboard - Main Entry Point
Run this script to fetch latest articles and generate your dashboard.

Usage:
    python run.py              # Fetch articles + build dashboard
    python run.py --no-fetch   # Rebuild dashboard from existing data
    python run.py --fetch-only # Only fetch, don't build dashboard
"""

import sys
import os

# Ensure we're running from the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from fetcher import fetch_all
from dashboard_builder import build_dashboard
from summarizer import generate_briefing, is_available


def main():
    args = sys.argv[1:]

    skip_fetch = "--no-fetch" in args
    fetch_only = "--fetch-only" in args

    print("=" * 50)
    print("  Personal News Dashboard")
    print("=" * 50)
    print()

    # Step 1: Fetch articles
    if not skip_fetch:
        print("[1/3] Fetching articles from RSS feeds...")
        fetch_all()
        print()
    else:
        print("[1/3] Skipping fetch (using existing data)")
        print()

    if fetch_only:
        print("Done (fetch only mode)")
        return

    # Step 2: AI summary (optional)
    ai_summary = None
    if is_available():
        print("[2/3] Generating AI briefing...")
        ai_summary = generate_briefing()
        print()
    else:
        print("[2/3] AI briefing skipped (no API key)")
        print("  To enable: pip install anthropic && export ANTHROPIC_API_KEY=sk-ant-...")
        print()

    # Step 3: Build dashboard
    print("[3/3] Building dashboard...")
    output = build_dashboard(ai_summary)
    print()

    print("=" * 50)
    print(f"  Dashboard ready: {os.path.abspath(output)}")
    print(f"  Open in your browser to view")
    print("=" * 50)


if __name__ == "__main__":
    main()
