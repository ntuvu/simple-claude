#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def parse_urls_value(value: object) -> list[str]:
    if isinstance(value, list):
        urls = value
    elif isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError:
                raise SystemExit("urls must be a JSON array of strings.")
            if not isinstance(parsed, list):
                raise SystemExit("urls must be a JSON array of strings.")
            urls = parsed
        else:
            urls = [stripped]
    else:
        raise SystemExit("urls must be a JSON array of strings.")

    normalized: list[str] = []
    for item in urls:
        if not isinstance(item, str) or not item.strip():
            raise SystemExit("Each url must be a non-empty string.")
        normalized.append(item.strip())
    return normalized


def parse_stdin_payload() -> tuple[list[str] | None, int | None]:
    if sys.stdin.isatty():
        return None, None

    payload = sys.stdin.read().strip()
    if not payload:
        return None, None

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return None, None

    urls_raw = data.get("urls")
    urls = parse_urls_value(urls_raw) if urls_raw is not None else None

    max_chars_raw = data.get("maxCharacters", data.get("max_characters"))
    if max_chars_raw is None:
        max_chars = None
    else:
        try:
            max_chars = int(max_chars_raw)
        except (TypeError, ValueError):
            raise SystemExit("maxCharacters must be a positive number.")

    return urls, max_chars


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    env_candidates = [
        script_dir / ".env",
        script_dir.parent / ".env",
        script_dir.parent.parent / ".env",
    ]
    for env_file in env_candidates:
        load_env_file(env_file)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--urls",
        help="URLs to read. Pass a JSON array string or a single URL.",
    )
    parser.add_argument(
        "--max-characters",
        "--maxCharacters",
        dest="max_characters",
        type=int,
    )
    args = parser.parse_args()

    stdin_urls, stdin_max_characters = parse_stdin_payload()

    urls = parse_urls_value(args.urls) if args.urls is not None else stdin_urls
    max_characters = (
        args.max_characters
        if args.max_characters is not None
        else stdin_max_characters
    )

    if not urls:
        raise SystemExit(
            'Missing urls. Provide --urls "[\"https://...\"]" or JSON stdin {"urls":["https://..."]}.'
        )

    if max_characters is not None and max_characters < 1:
        raise SystemExit("maxCharacters must be a positive number.")

    exa_api_key = os.getenv("EXA_API_KEY")
    if not exa_api_key:
        searched = ", ".join(str(p) for p in env_candidates)
        raise SystemExit(
            f"Missing EXA_API_KEY. Set it in one of: {searched} or environment."
        )

    mcp_url = f"https://mcp.exa.ai/mcp?exaApiKey={exa_api_key}"

    cmd = [
        "mcp2cli",
        "--mcp",
        mcp_url,
        "web-fetch-exa",
        "--urls",
        json.dumps(urls, ensure_ascii=False),
    ]
    if max_characters is not None:
        cmd.extend(["--max-characters", str(max_characters)])

    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
