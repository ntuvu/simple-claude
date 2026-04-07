---
name: web-fetch
description: >-
  Read a webpage's full content as clean markdown. Use after web_search_exa when highlights are insufficient or to read any URL. Best for: Extracting full content from known URLs. Batch multiple URLs in one call. Returns: Clean text content and metadata from the page(s).
---

# Web Fetch (Exa via CLI)

## Tool Restriction (Critical)

Use CLI script `./scripts/callmcp.py` to call `web-fetch-exa`.
Do NOT call MCP tool directly.

## Token Isolation (Critical)

Never run Exa in main context. Always use `search-agent` for this skill.

- Agent runs CLI fetch via `scripts/callmcp.py`
- Agent extracts minimum viable snippet(s) from each URL + constraints
- Agent deduplicates overlapping/near-identical page content
- Agent returns copyable snippets + brief explanation
- Main context stays clean regardless of fetch volume

## CLI to use

```bash
python3 scripts/callmcp.py --urls '["https://docs.dagster.io"]' [--max-characters <positive-number>]
```

Multiple URLs:

```bash
python3 scripts/callmcp.py --urls '["https://docs.dagster.io","https://www.exa.ai/exa-api"]'
```

Or JSON stdin:

```bash
printf '{"urls":["https://docs.dagster.io"],"maxCharacters":3000}' | python3 scripts/callmcp.py
```

## Input schema

- `urls`: string[] (required)
  - URLs to read. Batch multiple URLs in one call.
- `maxCharacters`: number (optional)
  - Maximum characters to extract per page (must be a positive number, default: 3000)

## What this tool provides

`web-fetch-exa`:
- fetches full page content from known URL(s)
- returns clean markdown text for fast reading
- supports batching multiple URLs in one call

## When to Use

Use for:
- reading full content after `web_search_exa` snippets are too short
- extracting details from known source URLs
- comparing content across multiple pages

## Input Guidelines

- Pass exact URL(s)
- Batch related URLs in one call when possible
- Prefer 1-5 high-signal URLs first, then expand only if needed

## Output Format

Return:
1) Short summary per URL
2) Key extracted points/snippets relevant to user question
3) Source URL list

