# Working Rules

## File Safety

* Never delete files without explicit permission
* Always preserve originals â create copies before editing
* When reorganizing, generate an ORGANIZATION-LOG.md documenting every move (before â after)

## Process

* Before starting any task: read all relevant files in Context/ first
* Ask clarifying questions before executing â do not guess at ambiguous requirements
* Show a brief plan and wait for approval before making changes
* For multi-step tasks, check in after major milestones

## Output Standards

* Save all generated files to /Output/ unless instructed otherwise
* Name deliverables: YYYY-MM-DD\_\[topic]\_v1.\[ext]
* Source code changes go in /Source/
* Dashboard HTML output goes in /Output/

**Default outputs:**

* Code â .py files in /Source/
* Dashboard â .html in /Output/
* Documentation â .md

## Code Standards

* All Python code must run on Python 3.10+ on Windows
* Dependencies must be documented in requirements.txt
* Configuration (feed URLs, settings) must be separated from logic (config.py)
* API keys must never be hardcoded â use environment variables only
* Code should include docstrings and inline comments for maintainability

## Context Awareness

* Read about-me.md at the start of every session
* This is a personal tool â no multi-user concerns, no authentication complexity
* RSS feeds are the primary data source; scraping is a future enhancement
* The Claude API integration is optional and should degrade gracefully when no key is set

## Sensitive Information

* Do not include API keys, passwords, or tokens in any committed file
* The articles database is local and personal â no privacy concerns with stored content
* When working with subscription credentials (future scraper work), flag security implications

## What Not To Do

* Do not invent article data or fake news content for testing without clearly labeling it as sample data
* Do not make external API calls without explicit approval
* Do not modify files in /Context/ without asking first
* Do not push code to any remote repository without permission

## Session Continuity

* At the end of a significant session, update /session-log.md with a summary of what was done, decisions made, and next steps
* This file serves as memory between sessions â read it at session start if it exists
