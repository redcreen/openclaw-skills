#!/usr/bin/env python3
"""Validate generated doctor-brief reply payloads."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class BriefValidationError(Exception):
    """Raised when a generated doctor brief violates the reply contract."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a generated doctor-brief JSON file."
    )
    parser.add_argument("--brief-file", help="Path to a generated brief JSON file.")
    parser.add_argument("--brief-json", help="Inline generated brief JSON.")
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.brief_file and args.brief_json:
        raise BriefValidationError("Use either --brief-file or --brief-json, not both.")
    if not args.brief_file and not args.brief_json:
        raise BriefValidationError("One of --brief-file or --brief-json is required.")
    raw = Path(args.brief_file).read_text(encoding="utf-8") if args.brief_file else args.brief_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BriefValidationError(f"Invalid brief JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise BriefValidationError("Brief payload must be a JSON object.")
    return payload


def require_non_empty_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise BriefValidationError(f"{key} must be a non-empty string.")
    return value.strip()


def require_non_empty_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list) or not value:
        raise BriefValidationError(f"{key} must be a non-empty list.")
    normalized = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(normalized) != len(value):
        raise BriefValidationError(f"{key} must contain only non-empty strings.")
    return normalized


def validate_window(payload: dict[str, Any]) -> None:
    window = payload.get("brief_window")
    if not isinstance(window, dict):
        raise BriefValidationError("brief_window must be an object.")
    for key in ("start_date", "end_date"):
        if not isinstance(window.get(key), str) or not window.get(key).strip():
            raise BriefValidationError(f"brief_window.{key} must be a non-empty string.")
    days = window.get("days")
    if not isinstance(days, int) or days < 1:
        raise BriefValidationError("brief_window.days must be an integer >= 1.")


def validate_saved_paths(payload: dict[str, Any]) -> bool:
    has_md = "saved_markdown_path" in payload
    has_json = "saved_json_path" in payload
    if has_md != has_json:
        raise BriefValidationError("saved_markdown_path and saved_json_path must appear together.")
    if not has_md:
        return False
    require_non_empty_string(payload, "saved_markdown_path")
    require_non_empty_string(payload, "saved_json_path")
    return True


def validate_markdown(payload: dict[str, Any], saved_expected: bool) -> None:
    markdown = require_non_empty_string(payload, "markdown")
    required_markers = [
        "Brief Window:",
        "## Main Concerns",
        "## Clinician Snapshot",
        "## Follow-Up Points",
    ]
    missing = [marker for marker in required_markers if marker not in markdown]
    if missing:
        raise BriefValidationError("markdown is missing required marker(s): " + ", ".join(missing))
    if saved_expected and "Saved To:" not in markdown:
        raise BriefValidationError("markdown must include Saved To when a brief file was written.")
    non_empty_lines = [line for line in markdown.splitlines() if line.strip()]
    if len(non_empty_lines) < 8:
        raise BriefValidationError("markdown is too short for a clinician brief.")


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("status") != "ok":
        raise BriefValidationError("status must be `ok`.")
    validate_window(payload)
    main_concerns = require_non_empty_list(payload, "main_concerns")
    clinician_snapshot = require_non_empty_list(payload, "clinician_snapshot")
    if not set(clinician_snapshot).intersection(payload.get("profile_snapshot", []) + payload.get("trend_summary", [])):
        raise BriefValidationError("clinician_snapshot must be grounded in profile_snapshot or trend_summary.")
    saved_expected = validate_saved_paths(payload)
    validate_markdown(payload, saved_expected)
    return {
        "status": "ok",
        "main_concern_count": len(main_concerns),
        "snapshot_count": len(clinician_snapshot),
        "saved": saved_expected,
    }


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args)
        result = validate_payload(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except BriefValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
