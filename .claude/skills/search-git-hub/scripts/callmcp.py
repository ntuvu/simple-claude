#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys


ALLOWED_KEYS = {
    "query",
    "matchCase",
    "matchWholeWords",
    "useRegexp",
    "repo",
    "path",
    "language",
    "match_case",
    "match_whole_words",
    "use_regexp",
}


def parse_bool(value: object, name: str) -> bool:
    if isinstance(value, bool):
        return value
    raise SystemExit(f"{name} must be a boolean.")


def parse_language_value(value: object) -> list[str]:
    if isinstance(value, list):
        items = value
    elif isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            raise SystemExit("language must be a JSON array of strings.")
        if not isinstance(parsed, list):
            raise SystemExit("language must be a JSON array of strings.")
        items = parsed
    else:
        raise SystemExit("language must be a JSON array of strings.")

    result: list[str] = []
    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise SystemExit("Each language value must be a non-empty string.")
        result.append(item.strip())
    return result


def parse_stdin_payload() -> dict[str, object]:
    if sys.stdin.isatty():
        return {}

    payload = sys.stdin.read().strip()
    if not payload:
        return {}

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        raise SystemExit("stdin payload must be a JSON object.")

    unknown = set(data.keys()) - ALLOWED_KEYS
    if unknown:
        raise SystemExit(f"Unknown fields in stdin payload: {', '.join(sorted(unknown))}")

    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        help=(
            "The literal code pattern to search for (e.g., 'useState(', "
            "'export function'). Use actual code that would appear in files, "
            "not keywords or questions."
        ),
    )
    parser.add_argument(
        "--match-case",
        action="store_true",
        help="Whether the search should be case sensitive",
    )
    parser.add_argument(
        "--match-whole-words",
        action="store_true",
        help="Whether to match whole words only",
    )
    parser.add_argument(
        "--use-regexp",
        action="store_true",
        help="Whether to interpret the query as a regular expression",
    )
    parser.add_argument(
        "--repo",
        help=(
            "Filter by repository. Examples: 'facebook/react', 'microsoft/vscode', "
            "'vercel/ai'."
        ),
    )
    parser.add_argument(
        "--path",
        help=(
            "Filter by file path. Examples: 'src/components/Button.tsx', 'README.md'."
        ),
    )
    parser.add_argument(
        "--language",
        help=(
            "Filter by programming language as JSON array, e.g. "
            "'[\"TypeScript\",\"TSX\"]'."
        ),
    )
    args = parser.parse_args()

    data = parse_stdin_payload()

    query = args.query if args.query is not None else data.get("query")
    match_case = args.match_case or parse_bool(data.get("matchCase", data.get("match_case", False)), "matchCase")
    match_whole_words = args.match_whole_words or parse_bool(
        data.get("matchWholeWords", data.get("match_whole_words", False)),
        "matchWholeWords",
    )
    use_regexp = args.use_regexp or parse_bool(data.get("useRegexp", data.get("use_regexp", False)), "useRegexp")
    repo = args.repo if args.repo is not None else data.get("repo")
    path = args.path if args.path is not None else data.get("path")

    if args.language is not None:
        language = parse_language_value(args.language)
    elif "language" in data:
        language = parse_language_value(data.get("language"))
    else:
        language = None

    if query is None or not str(query).strip():
        raise SystemExit('Missing query. Provide --query or JSON stdin {"query":"..."}.')

    if repo is not None and not isinstance(repo, str):
        raise SystemExit("repo must be a string.")
    if path is not None and not isinstance(path, str):
        raise SystemExit("path must be a string.")

    cmd = [
        "mcp2cli",
        "--mcp",
        "https://mcp.grep.app",
        "search-git-hub",
        "--query",
        str(query).strip(),
    ]

    if match_case:
        cmd.append("--match-case")
    if match_whole_words:
        cmd.append("--match-whole-words")
    if use_regexp:
        cmd.append("--use-regexp")
    if repo is not None and repo.strip():
        cmd.extend(["--repo", repo.strip()])
    if path is not None and path.strip():
        cmd.extend(["--path", path.strip()])
    if language is not None:
        cmd.extend(["--language", json.dumps(language, ensure_ascii=False)])

    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
