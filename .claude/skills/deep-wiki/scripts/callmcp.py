#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys


MCP_STDIO_CMD = "npx -y deepwiki-mcp"
ALLOWED_OPERATIONS = {
    "get-deepwiki-index",
    "get-deepwiki-page",
}


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

    return data


def resolve_operation(cli_operation: str | None, payload: dict[str, object]) -> str:
    operation = (
        cli_operation
        if cli_operation is not None
        else payload.get("operation")
        or payload.get("tool")
        or payload.get("method")
    )

    if not isinstance(operation, str) or not operation.strip():
        raise SystemExit(
            "Missing operation. Provide positional operation or JSON stdin with one of: "
            "get-deepwiki-index, get-deepwiki-page."
        )

    normalized = operation.strip()
    if normalized not in ALLOWED_OPERATIONS:
        raise SystemExit(
            "Invalid operation. Must be one of: get-deepwiki-index, get-deepwiki-page."
        )

    return normalized


def parse_repo_name(value: object) -> tuple[str | None, str | None]:
    if not isinstance(value, str) or not value.strip():
        return None, None

    repo_name = value.strip()
    if "/" not in repo_name:
        raise SystemExit('repoName must be in "owner/repo" format.')

    owner, repo = repo_name.split("/", 1)
    owner = owner.strip()
    repo = repo.strip()
    if not owner or not repo:
        raise SystemExit('repoName must be in "owner/repo" format.')

    return owner, repo


def resolve_owner_repo(
    cli_owner: str | None,
    cli_repo: str | None,
    cli_repo_name: str | None,
    payload: dict[str, object],
) -> tuple[str | None, str | None]:
    owner_from_repo_name, repo_from_repo_name = parse_repo_name(
        cli_repo_name if cli_repo_name is not None else payload.get("repoName") or payload.get("repo_name")
    )

    owner_value = cli_owner if cli_owner is not None else payload.get("owner")
    repo_value = cli_repo if cli_repo is not None else payload.get("repo")

    owner = owner_value.strip() if isinstance(owner_value, str) and owner_value.strip() else owner_from_repo_name
    repo = repo_value.strip() if isinstance(repo_value, str) and repo_value.strip() else repo_from_repo_name

    return owner, repo


def resolve_path(cli_path: str | None, payload: dict[str, object]) -> str | None:
    path_value = cli_path if cli_path is not None else payload.get("path")
    if path_value is None:
        return None

    if not isinstance(path_value, str) or not path_value.strip():
        raise SystemExit("path must be a non-empty string.")

    return path_value.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "operation",
        nargs="?",
        choices=sorted(ALLOWED_OPERATIONS),
        help="MCP operation: get-deepwiki-index, get-deepwiki-page",
    )
    parser.add_argument("--owner", help="Repository owner")
    parser.add_argument("--repo", help="Repository name")
    parser.add_argument(
        "--repo-name",
        dest="repo_name",
        help='Repository in "owner/repo" format (helper for get-deepwiki-index)',
    )
    parser.add_argument(
        "--path",
        help="Path to DeepWiki page (for get-deepwiki-page)",
    )
    args = parser.parse_args()

    payload = parse_stdin_payload()

    operation = resolve_operation(args.operation, payload)
    owner, repo = resolve_owner_repo(args.owner, args.repo, args.repo_name, payload)
    path = resolve_path(args.path, payload)

    cmd = [
        "mcp2cli",
        "--mcp-stdio",
        MCP_STDIO_CMD,
        operation,
    ]

    if operation == "get-deepwiki-index":
        if not owner or not repo:
            raise SystemExit(
                'Missing owner/repo. Provide --owner and --repo, or --repo-name "owner/repo", or JSON stdin with owner+repo.'
            )
        if path is not None:
            raise SystemExit("path is only supported with get-deepwiki-page.")
        cmd.extend(["--owner", owner, "--repo", repo])

    if operation == "get-deepwiki-page":
        if path is None:
            raise SystemExit(
                'Missing path. Provide --path or JSON stdin {"path":"..."} for get-deepwiki-page.'
            )
        if owner or repo:
            raise SystemExit("owner/repo are only supported with get-deepwiki-index.")
        cmd.extend(["--path", path])

    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
