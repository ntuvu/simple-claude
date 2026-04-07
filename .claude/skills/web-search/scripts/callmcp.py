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


def parse_stdin_payload() -> tuple[str | None, int | None]:
    if sys.stdin.isatty():
        return None, None

    payload = sys.stdin.read().strip()
    if not payload:
        return None, None

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return None, None

    query = data.get("query")
    num_results = data.get("numResults", data.get("num_results"))

    if num_results is None:
        parsed_num_results = None
    else:
        try:
            parsed_num_results = int(num_results)
        except (TypeError, ValueError):
            raise SystemExit("numResults must be a number.")

    return query, parsed_num_results


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
    parser.add_argument("--query", help="Natural language search query")
    parser.add_argument("--num-results", "--numResults", dest="num_results", type=int)
    args = parser.parse_args()

    stdin_query, stdin_num_results = parse_stdin_payload()

    query = args.query if args.query is not None else stdin_query
    num_results = args.num_results if args.num_results is not None else stdin_num_results

    if not query or not str(query).strip():
        raise SystemExit('Missing query. Provide --query or JSON stdin {"query":"..."}.')

    if num_results is not None and not (1 <= num_results <= 20):
        raise SystemExit("numResults must be between 1 and 20.")

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
        "web-search-exa",
        "--query",
        query,
    ]
    if num_results is not None:
        cmd.extend(["--num-results", str(num_results)])

    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
