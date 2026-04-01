# Voice & Style Guide â News Dashboard Project

## Dashboard Tone

The AI briefing and any generated summaries should follow these principles:

### Professional Executive Briefing Style

* Write as a senior analyst briefing a CEO â direct, substantive, no filler
* Lead with "so what" â why does this story matter, not just what happened
* Connect dots across publications â highlight when multiple sources cover the same theme from different angles
* Flag actionable items â anything that may require attention, a decision, or further reading

### Language

* English by default for the dashboard and briefing
* Concise paragraphs â 2-4 sentences each
* No bullet points in the AI briefing â use flowing prose organized by theme
* Bold key terms sparingly for scannability
* Avoid hedging language ("it seems", "perhaps") â be direct about what the data shows

### What to Prioritize in Summaries

1. Market-moving events (rates, commodities, major earnings)
2. Regulatory and policy changes (EU, US, global trade)
3. Industry-relevant stories (automotive, mobility, leasing, fleet)
4. AI and technology developments with business implications
5. Strategy and leadership insights (especially from HBR, Economist leaders)

### What to Deprioritize

* Celebrity news, entertainment, sports
* Hyper-local US politics unless globally significant
* Repetitive coverage of the same story across publications (consolidate instead)

## Code Style

* Python code follows PEP 8
* Functions have docstrings
* Configuration is centralized in config.py
* Print statements are used for progress logging (this is a CLI tool, not a library)
* Error handling should be graceful â one broken feed should not crash the entire pipeline
