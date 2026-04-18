#!/usr/bin/env python3
"""Validate generated bundle export or restore reply payloads."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class BundleValidationError(Exception):
    """Raised when a bundle reply violates the contract."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a generated bundle reply JSON file."
    )
    parser.add_argument("--reply-file", help="Path to a generated bundle reply JSON file.")
    parser.add_argument("--reply-json", help="Inline generated bundle reply JSON.")
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.reply_file and args.reply_json:
        raise BundleValidationError("Use either --reply-file or --reply-json, not both.")
    if not args.reply_file and not args.reply_json:
        raise BundleValidationError("One of --reply-file or --reply-json is required.")
    raw = Path(args.reply_file).read_text(encoding="utf-8") if args.reply_file else args.reply_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BundleValidationError(f"Invalid bundle JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise BundleValidationError("Bundle payload must be a JSON object.")
    return payload


def require_non_empty_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise BundleValidationError(f"{key} must be a non-empty string.")
    return value.strip()


def require_string_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list) or not value:
        raise BundleValidationError(f"{key} must be a non-empty list.")
    normalized = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(normalized) != len(value):
        raise BundleValidationError(f"{key} must contain only non-empty strings.")
    return normalized


def validate_markdown(payload: dict[str, Any]) -> None:
    markdown = require_non_empty_string(payload, "markdown")
    required_markers = ["Bundle Status:", "Source Or Target:", "Saved To:", "## What Was Included"]
    missing = [marker for marker in required_markers if marker not in markdown]
    if missing:
        raise BundleValidationError("markdown is missing required marker(s): " + ", ".join(missing))


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("status") != "ok":
        raise BundleValidationError("status must be `ok`.")
    operation = payload.get("operation")
    if operation not in {"export", "restore"}:
        raise BundleValidationError("operation must be `export` or `restore`.")
    require_non_empty_string(payload, "bundle_status")
    require_non_empty_string(payload, "source_or_target")
    saved_to = require_non_empty_string(payload, "saved_to")
    included = require_string_list(payload, "what_was_included")
    validate_markdown(payload)
    if operation == "export":
        bundle_path = require_non_empty_string(payload, "bundle_path")
        if saved_to != bundle_path:
            raise BundleValidationError("saved_to must match bundle_path for export replies.")
    else:
        restored_count = payload.get("restored_count")
        if not isinstance(restored_count, int) or restored_count < 0:
            raise BundleValidationError("restored_count must be an integer >= 0.")
        if restored_count != len(included):
            raise BundleValidationError("restored_count must match what_was_included length.")
    return {"status": "ok", "operation": operation, "item_count": len(included)}


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args)
        result = validate_payload(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except BundleValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
