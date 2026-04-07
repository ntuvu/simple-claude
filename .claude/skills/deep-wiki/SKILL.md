---
name: deep-wiki
description: >-
  Use when working with frameworks or libraries (e.g., React, Next.js, Prisma)
  and the repository is unfamiliar, so you need fast, source-linked context on
  architecture, modules, and key features before diving into implementation files.
context: fork
agent: search-agent
---

# DeepWiki (stdio MCP via CLI)

Read DeepWiki documentation pages for public GitHub repositories.

## Tool Restriction (Critical)

Use CLI script `./scripts/callmcp.py`.
In this repository, use `scripts/callmcp.py` for DeepWiki operations to enforce operation allowlist and stable CLI behavior.

## Supported operations only (Critical)

This skill allows ONLY:
- `get-deepwiki-index`
- `get-deepwiki-page`

Do NOT use `ask-question` or legacy DeepWiki tools.

## Required call order (Critical)

You MUST call `get-deepwiki-index` first to obtain page `path` values.
Then call `get-deepwiki-page` with one of those paths.

## Token Isolation (Critical)

Always run this skill with `search-agent` to keep main context small.

- Agent calls DeepWiki via `scripts/callmcp.py`
- Agent gets index first, then fetches only relevant page(s)
- Agent extracts concise, copyable findings
- Main context stays clean even for large page outputs

## CLI to use

Get index for a repository:

```bash
python3 scripts/callmcp.py get-deepwiki-index --repo-name "owner/repo"
```

Equivalent explicit args:

```bash
python3 scripts/callmcp.py get-deepwiki-index --owner "owner" --repo "repo"
```

Get a page by path (path must come from index):

```bash
python3 scripts/callmcp.py get-deepwiki-page --path "/owner/repo/1-topic"
```

Or JSON stdin:

```bash
printf '{"operation":"get-deepwiki-index","repoName":"owner/repo"}' | python3 scripts/callmcp.py
printf '{"operation":"get-deepwiki-page","path":"/owner/repo/1-topic"}' | python3 scripts/callmcp.py
```

## Input schema

- `operation`: string (required)
  - One of: `get-deepwiki-index`, `get-deepwiki-page`

For `get-deepwiki-index`:
- `repoName`: string (optional helper)
  - Format: `owner/repo`
- `owner`: string (optional if `repoName` provided)
- `repo`: string (optional if `repoName` provided)

For `get-deepwiki-page`:
- `path`: string (required)
  - DeepWiki page path returned by `get-deepwiki-index`

## Recommended flow

1) Call `get-deepwiki-index` to list available pages and their `path`.
2) Select only relevant page path(s) for the user question.
3) Call `get-deepwiki-page` for selected path(s).
4) Summarize only the sections relevant to the request.

## When to use

Use this skill when:
- you need architecture/feature overview of a public GitHub repository
- you want a fast map of modules before reading source code
- you need curated wiki-style context to support implementation/review

## Output format

Return:
1) Relevant DeepWiki page paths selected from index
2) Key technical points tied to the user request
3) Source repo and page path(s) used
