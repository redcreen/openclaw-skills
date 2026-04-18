#!/usr/bin/env python3
"""Validate generated health-review reply payloads."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class ReviewValidationError(Exception):
    """Raised when a generated review payload violates the reply contract."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a generated health-review JSON file."
    )
    parser.add_argument("--review-file", help="Path to a generated review JSON file.")
    parser.add_argument("--review-json", help="Inline generated review JSON.")
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.review_file and args.review_json:
        raise ReviewValidationError("Use either --review-file or --review-json, not both.")
    if not args.review_file and not args.review_json:
        raise ReviewValidationError("One of --review-file or --review-json is required.")
    raw = Path(args.review_file).read_text(encoding="utf-8") if args.review_file else args.review_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReviewValidationError(f"Invalid review JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReviewValidationError("Review payload must be a JSON object.")
    return payload


def require_non_empty_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ReviewValidationError(f"{key} must be a non-empty string.")
    return value.strip()


def require_non_empty_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list) or not value:
        raise ReviewValidationError(f"{key} must be a non-empty list.")
    normalized = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(normalized) != len(value):
        raise ReviewValidationError(f"{key} must contain only non-empty strings.")
    return normalized


def validate_window(payload: dict[str, Any]) -> None:
    window = payload.get("review_window")
    if not isinstance(window, dict):
        raise ReviewValidationError("review_window must be an object.")
    for key in ("start_date", "end_date"):
        if not isinstance(window.get(key), str) or not window.get(key).strip():
            raise ReviewValidationError(f"review_window.{key} must be a non-empty string.")
    days = window.get("days")
    if not isinstance(days, int) or days < 1:
        raise ReviewValidationError("review_window.days must be an integer >= 1.")


def validate_markdown(payload: dict[str, Any], saved_expected: bool) -> None:
    markdown = require_non_empty_string(payload, "markdown")
    required_markers = ["Review Window:", "## Main Takeaway", "## What Changed", "## Next Focus"]
    missing = [marker for marker in required_markers if marker not in markdown]
    if missing:
        raise ReviewValidationError("markdown is missing required marker(s): " + ", ".join(missing))
    non_empty_lines = [line for line in markdown.splitlines() if line.strip()]
    if len(non_empty_lines) < 7:
        raise ReviewValidationError("markdown is too short for a review reply.")
    if saved_expected and "Saved To:" not in markdown:
        raise ReviewValidationError("markdown must include Saved To when a review file was written.")


def validate_saved_paths(payload: dict[str, Any]) -> bool:
    has_md = "saved_markdown_path" in payload
    has_json = "saved_json_path" in payload
    if has_md != has_json:
        raise ReviewValidationError("saved_markdown_path and saved_json_path must appear together.")
    if not has_md:
        return False
    require_non_empty_string(payload, "saved_markdown_path")
    require_non_empty_string(payload, "saved_json_path")
    return True


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("status") != "ok":
        raise ReviewValidationError("status must be `ok`.")
    mode = payload.get("mode")
    if mode not in {"daily", "weekly", "monthly", "custom"}:
        raise ReviewValidationError("mode must be one of: daily, weekly, monthly, custom.")
    validate_window(payload)
    require_non_empty_string(payload, "main_takeaway")
    what_changed = require_non_empty_list(payload, "what_changed")
    next_focus = require_non_empty_list(payload, "next_focus")
    if payload.get("main_takeaway") != what_changed[0]:
        raise ReviewValidationError("main_takeaway must match the first What Changed item.")
    saved_expected = validate_saved_paths(payload)
    validate_markdown(payload, saved_expected)
    return {
        "status": "ok",
        "mode": mode,
        "saved": saved_expected,
        "record_count": payload.get("record_count"),
    }


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args)
        result = validate_payload(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ReviewValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
