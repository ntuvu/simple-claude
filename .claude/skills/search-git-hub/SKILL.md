---
name: search-git-hub
description: >-
  Find real-world code examples from over a million public GitHub repositories to help answer programming questions. IMPORTANT: This tool searches for literal code patterns (like grep), not keywords. Search for actual code that would appear in files.
context: fork
agent: search-agent
---

# Search GitHub Code (via CLI)

Find real code usage patterns from public GitHub repositories.

## Tool Restriction (Critical)

Use CLI script `./scripts/callmcp.py` to call `search-git-hub`.
Do NOT call MCP tool directly.

## Token Isolation (Critical)

Never run high-volume search in main context. Always use `search-agent`.

- Agent runs CLI search via `scripts/callmcp.py`
- Agent extracts minimum viable snippet(s) + constraints
- Agent deduplicates near-identical results
- Agent returns copyable snippets + brief explanation
- Main context stays clean regardless of result volume

## Literal-pattern search only

Search **actual code patterns**, not generic keywords/questions.

- ✅ Good: `useState(`, `import React from`, `async function`, `(?s)try {.*await`
- ❌ Bad: `react tutorial`, `best practices`, `how to use`

## When to use

Use this skill when:
- implementing unfamiliar APIs/libraries and needing real usage patterns
- unsure about syntax, params, or configuration for a specific library
- looking for production-style implementation examples
- understanding how libraries/frameworks are combined in real projects

## CLI to use

```bash
python3 scripts/callmcp.py --query "useState("
```

Examples:

```bash
python3 scripts/callmcp.py --query "getServerSession" --language '["TypeScript","TSX"]'
python3 scripts/callmcp.py --query "ErrorBoundary" --language '["TSX"]'
python3 scripts/callmcp.py --query "(?s)useEffect\(\(\) => {.*removeEventListener" --use-regexp
python3 scripts/callmcp.py --query "CORS(" --match-case --language '["Python"]'
```

Or JSON stdin:

```bash
printf '{"query":"useState(","language":["TypeScript","TSX"],"useRegexp":false}' | python3 scripts/callmcp.py
```

## Input schema

- `query`: string (required)
  - The literal code pattern to search for.
- `matchCase`: boolean (optional, default: `false`)
  - Whether search is case-sensitive.
- `matchWholeWords`: boolean (optional, default: `false`)
  - Whether to match whole words only.
- `useRegexp`: boolean (optional, default: `false`)
  - Whether to interpret query as regex.
- `repo`: string (optional)
  - Repository filter, e.g. `facebook/react`, `vercel/`.
- `path`: string (optional)
  - File path filter, e.g. `src/components/Button.tsx`, `/route.ts`.
- `language`: string[] (optional)
  - Language filter, e.g. `["TypeScript","TSX"]`, `["Python"]`.

## Regex tips

- Set `useRegexp=true` for flexible matching.
- Prefix with `(?s)` to match across multiple lines.
- Example: `(?s)useState\(.*loading`

## Output format

Return:
1) Top relevant code findings (short)
2) Why each match is relevant
3) Source repo/path links (if available)
