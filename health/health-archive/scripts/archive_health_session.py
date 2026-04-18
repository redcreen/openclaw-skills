#!/usr/bin/env python3
"""Archive multiple health payloads as one local-first session."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import archive_health_record as archive_lib


class SessionArchiveError(Exception):
    """Raised when a session payload cannot be archived."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive multiple health payloads in one session."
    )
    parser.add_argument("--payload-file", help="Path to a JSON payload file.")
    parser.add_argument("--payload-json", help="Inline JSON payload.")
    parser.add_argument("--data-root", help="Override the external health data root.")
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.payload_file and args.payload_json:
        raise SessionArchiveError("Use either --payload-file or --payload-json, not both.")
    if not args.payload_file and not args.payload_json:
        raise SessionArchiveError("One of --payload-file or --payload-json is required.")
    raw = open(args.payload_file, "r", encoding="utf-8").read() if args.payload_file else args.payload_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SessionArchiveError(f"Invalid JSON payload: {exc}") from exc
    if not isinstance(payload, dict):
        raise SessionArchiveError("Payload must be a JSON object.")
    return payload


def archive_session(payload: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        raise SessionArchiveError("entries must be a non-empty list.")

    delegated_args = argparse.Namespace(
        payload_file=None,
        payload_json=None,
        data_root=args.data_root,
    )
    archived: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for index, item in enumerate(entries, start=1):
        if not isinstance(item, dict):
            errors.append({"index": index, "status": "not archived", "error": "entry must be an object"})
            continue
        working = dict(item)
        if "data_root" not in working and payload.get("data_root"):
            working["data_root"] = payload["data_root"]
        try:
            archived.append(archive_lib.archive(working, delegated_args))
        except archive_lib.ArchiveError as exc:
            errors.append({"index": index, "status": "not archived", "error": str(exc)})

    if archived and not errors:
        status = "archived"
    elif archived and errors:
        status = "partially archived"
    else:
        status = "not archived"

    return {
        "status": status,
        "session_label": payload.get("session_label"),
        "archived_count": len(archived),
        "error_count": len(errors),
        "entries": archived,
        "errors": errors,
    }


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args)
        result = archive_session(payload, args)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["status"] != "not archived" else 1
    except SessionArchiveError as exc:
        print(json.dumps({"status": "not archived", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
