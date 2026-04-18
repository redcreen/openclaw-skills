#!/usr/bin/env python3
"""Validate generated health-reminder reply payloads."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class ReminderValidationError(Exception):
    """Raised when a reminder reply violates the contract."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a generated health-reminders JSON file."
    )
    parser.add_argument("--reply-file", help="Path to a generated reminder JSON file.")
    parser.add_argument("--reply-json", help="Inline generated reminder JSON.")
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.reply_file and args.reply_json:
        raise ReminderValidationError("Use either --reply-file or --reply-json, not both.")
    if not args.reply_file and not args.reply_json:
        raise ReminderValidationError("One of --reply-file or --reply-json is required.")
    raw = Path(args.reply_file).read_text(encoding="utf-8") if args.reply_file else args.reply_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReminderValidationError(f"Invalid reminder JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReminderValidationError("Reminder payload must be a JSON object.")
    return payload


def require_non_empty_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ReminderValidationError(f"{key} must be a non-empty string.")
    return value.strip()


def require_string_list(payload: dict[str, Any], key: str, *, allow_empty: bool = False) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ReminderValidationError(f"{key} must be a list.")
    if not value and not allow_empty:
        raise ReminderValidationError(f"{key} must not be empty.")
    normalized = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(normalized) != len(value):
        raise ReminderValidationError(f"{key} must contain only non-empty strings.")
    return normalized


def validate_due_payload(payload: dict[str, Any]) -> dict[str, Any]:
    require_non_empty_string(payload, "checked_at")
    require_non_empty_string(payload, "reminder_status")
    due_count = payload.get("due_count")
    if not isinstance(due_count, int) or due_count < 0:
        raise ReminderValidationError("due_count must be an integer >= 0.")
    due_rules = payload.get("due_rules")
    if not isinstance(due_rules, list):
        raise ReminderValidationError("due_rules must be a list.")
    if len(due_rules) != due_count:
        raise ReminderValidationError("due_count must match the number of due_rules.")
    what_is_due = require_string_list(payload, "what_is_due")
    why_it_is_due = require_string_list(payload, "why_it_is_due")
    what_to_do_next = require_string_list(payload, "what_to_do_next")
    if due_count > 0:
        if len(what_is_due) != due_count or len(why_it_is_due) != due_count or len(what_to_do_next) != due_count:
            raise ReminderValidationError("Due replies must explain each due reminder with reason and next action.")
    markdown = require_non_empty_string(payload, "markdown")
    required_markers = ["Reminder Status:", "## What Is Due", "## Why It Is Due", "## What To Do Next"]
    missing = [marker for marker in required_markers if marker not in markdown]
    if missing:
        raise ReminderValidationError("markdown is missing required marker(s): " + ", ".join(missing))
    return {"status": "ok", "reply_type": "due", "due_count": due_count}


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("status") != "ok":
        raise ReminderValidationError("status must be `ok`.")
    if "due_count" in payload:
        return validate_due_payload(payload)
    raise ReminderValidationError("Unsupported reminder payload; expected a due-check result.")


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args)
        result = validate_payload(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ReminderValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
