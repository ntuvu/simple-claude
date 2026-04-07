---
name: web-search
description: >- 
  Search the web for any topic and get clean, ready-to-use content. Best for: Finding current information, news, facts, or answering questions about any topic. Returns: Clean text content from top search results, ready for LLM use. Query tips: describe the ideal page, not keywords. "blog post comparing React and Vue performance" not "React vs Vue". If highlights are insufficient, follow up with web_fetch_exa on the best URLs.
---

# Web Search (Exa via CLI)

## Tool Restriction (Critical)

Use CLI script `./scripts/callmcp.py` to call `web-search-exa`.
Do NOT call MCP tool directly.

## Token Isolation (Critical)

Never run Exa in main context. Always use `search-agent` for this skill.

- Agent runs CLI search via `scripts/callmcp.py`
- Agent extracts minimum viable snippet(s) + constraints
- Agent deduplicates near-identical results (mirrors/forks/repeated answers)
- Agent returns copyable snippets + brief explanation
- Main context stays clean regardless of search volume

## CLI to use

```bash
python3 scripts/callmcp.py --query "<query>" [--num-results <1-20>]
```

Or JSON stdin:

```bash
printf '{"query":"<query>","numResults":10}' | python3 scripts/callmcp.py
```

## Input schema

- `query`: string (required)
  - Natural language search query. Should be a semantically rich description of the ideal page, not just keywords.
- `numResults`: number (optional)
  - Number of search results to return (must be a number, default: 5)
  - Range: `1..20`

## What this tool provides

`web-search-exa`:
- searches the web for any topic
- returns titles, URLs, and highlighted snippets from top pages
- works best for broad discovery and fast research

If highlights are insufficient, follow up with `web_fetch_exa` on the best URL(s).

## When to Use

Use for:
- general web research
- finding relevant sources quickly
- collecting up-to-date references before deeper reading

## Query Guidelines

- Use the user’s full intent as query (not only 1-2 keywords)
- Include exact entities (product, company, API, version)
- Add time context when needed (e.g. `2026`, `latest`)

## Output Format

Return:
1) Top relevant findings (short)
2) Why each result is relevant
3) Source URLs

