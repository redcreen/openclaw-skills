#!/usr/bin/env python3
"""Lightweight validation for rendered private-doctor replies."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class ReplyValidationError(Exception):
    """Raised when a rendered reply violates the contract."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a rendered private-doctor reply JSON file."
    )
    parser.add_argument("--reply-file", help="Path to a rendered reply JSON file.")
    parser.add_argument("--reply-json", help="Inline rendered reply JSON.")
    return parser.parse_args()


def load_reply(args: argparse.Namespace) -> dict[str, Any]:
    if args.reply_file and args.reply_json:
        raise ReplyValidationError("Use either --reply-file or --reply-json, not both.")
    if not args.reply_file and not args.reply_json:
        raise ReplyValidationError("One of --reply-file or --reply-json is required.")
    raw = Path(args.reply_file).read_text(encoding="utf-8") if args.reply_file else args.reply_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReplyValidationError(f"Invalid reply JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReplyValidationError("Reply must be a JSON object.")
    return payload


def require_sections(reply: dict[str, Any], required: list[str]) -> None:
    sections = reply.get("sections")
    if not isinstance(sections, dict):
        raise ReplyValidationError("sections must be an object.")
    missing = [key for key in required if not isinstance(sections.get(key), str) or not sections.get(key).strip()]
    if missing:
        raise ReplyValidationError("Missing required section(s): " + ", ".join(missing))


def validate_archive_honesty(reply: dict[str, Any]) -> None:
    source = reply.get("archive_status_source")
    code = reply.get("record_status_code")
    if source == "not-verified" and code != "not_verified":
        raise ReplyValidationError(
            "record_status_code must stay `not_verified` when archive_status_source is `not-verified`."
        )
    if source == "observed-write-result":
        require_sections(reply, ["recorded", "saved_to"])


def validate_markdown_shape(reply: dict[str, Any]) -> None:
    markdown = reply.get("markdown")
    if not isinstance(markdown, str):
        raise ReplyValidationError("markdown must be a string.")
    non_empty_lines = [line for line in markdown.splitlines() if line.strip()]
    if len(non_empty_lines) < 3:
        raise ReplyValidationError("markdown is too short; expected a multi-line doctor reply.")


def validate_reply(reply: dict[str, Any]) -> dict[str, Any]:
    mode = reply.get("mode")
    if mode not in {"routine", "onboarding", "trend"}:
        raise ReplyValidationError("mode must be one of: routine, onboarding, trend.")
    language = reply.get("language")
    if language not in {"zh", "en"}:
        raise ReplyValidationError("language must be `zh` or `en`.")
    markdown = reply.get("markdown")
    if not isinstance(markdown, str) or not markdown.strip():
        raise ReplyValidationError("markdown must be a non-empty string.")

    if mode == "onboarding":
        require_sections(reply, ["record_status", "profile_status", "doctor_view", "next_questions"])
    else:
        require_sections(reply, ["record_status", "doctor_view", "advice"])

    validate_archive_honesty(reply)
    validate_markdown_shape(reply)
    return {
        "status": "ok",
        "mode": mode,
        "language": language,
        "archive_status_source": reply.get("archive_status_source"),
        "record_status_code": reply.get("record_status_code"),
    }


def main() -> int:
    args = parse_args()
    try:
        reply = load_reply(args)
        result = validate_reply(reply)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ReplyValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
