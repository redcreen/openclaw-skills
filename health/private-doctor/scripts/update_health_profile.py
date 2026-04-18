#!/usr/bin/env python3
"""Append confirmed long-lived facts to the local health profile."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any


DEFAULT_DATA_ROOT = Path("~/document/personal health").expanduser()
PROFILE_HEADER = """# Health Profile

## Facts
"""


class ProfileUpdateError(Exception):
    """Raised when profile updates cannot be applied."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append confirmed long-lived facts to the health profile."
    )
    parser.add_argument("--payload-file", help="Path to a JSON payload file.")
    parser.add_argument("--payload-json", help="Inline JSON payload.")
    parser.add_argument("--data-root", help="Override the external health data root.")
    return parser.parse_args()


def choose_data_root(arg_root: str | None, payload_root: Any) -> Path:
    if arg_root:
        return Path(arg_root).expanduser()
    if isinstance(payload_root, str) and payload_root.strip():
        return Path(payload_root).expanduser()
    env_root = os.environ.get("HEALTH_DATA_ROOT") or os.environ.get("HEALTH_ARCHIVE_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return DEFAULT_DATA_ROOT


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.payload_file and not args.payload_json:
        raise ProfileUpdateError("One of --payload-file or --payload-json is required.")
    if args.payload_file and args.payload_json:
        raise ProfileUpdateError("Use either --payload-file or --payload-json, not both.")
    raw = Path(args.payload_file).read_text(encoding="utf-8") if args.payload_file else args.payload_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProfileUpdateError(f"Invalid JSON payload: {exc}") from exc
    if not isinstance(payload, dict):
        raise ProfileUpdateError("Payload must be a JSON object.")
    return payload


def ensure_profile(profile_path: Path) -> None:
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    if not profile_path.exists():
        profile_path.write_text(PROFILE_HEADER, encoding="utf-8")


def parse_literal(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def latest_profile_map(profile_path: Path) -> dict[str, Any]:
    latest: dict[str, Any] = {}
    if not profile_path.exists():
        return latest
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- ") or " | " not in line:
            continue
        body = line.split(" | ", 1)[1]
        if "label=" not in body:
            continue
        parts = {}
        for chunk in body.split(","):
            if "=" not in chunk:
                continue
            key, value = chunk.split("=", 1)
            parts[key.strip()] = parse_literal(value.strip())
        label = parts.get("label")
        if isinstance(label, str):
            latest[label] = parts.get("value")
    return latest


def normalize_facts(raw_facts: Any) -> list[dict[str, Any]]:
    if raw_facts in (None, "", []):
        raise ProfileUpdateError("facts is required and must not be empty.")
    if isinstance(raw_facts, str):
        raw_facts = [{"text": raw_facts}]
    if not isinstance(raw_facts, list):
        raise ProfileUpdateError("facts must be a string or a list.")

    normalized = []
    for item in raw_facts:
        if isinstance(item, str):
            text = item.strip()
            if text:
                normalized.append({"text": text})
            continue
        if not isinstance(item, dict):
            raise ProfileUpdateError("Each fact must be a string or an object.")
        cleaned = {}
        for key, value in item.items():
            if not isinstance(key, str) or not key.strip():
                raise ProfileUpdateError("Fact keys must be non-empty strings.")
            cleaned[key.strip()] = value
        if cleaned:
            normalized.append(cleaned)
    if not normalized:
        raise ProfileUpdateError("facts did not contain any usable entries.")
    return normalized


def render_fact_line(fact: dict[str, Any], recorded_at: str) -> str:
    if "text" in fact and len(fact) == 1:
        return f"- {recorded_at} | {fact['text']}"
    ordered = ", ".join(
        f"{key}={json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value}"
        for key, value in sorted(fact.items())
    )
    return f"- {recorded_at} | {ordered}"


def should_skip_fact(fact: dict[str, Any], latest: dict[str, Any]) -> bool:
    label = fact.get("label")
    if not isinstance(label, str) or "value" not in fact:
        return False
    return label in latest and latest[label] == fact["value"]


def update_profile(payload: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    data_root = choose_data_root(args.data_root, payload.get("data_root"))
    profile_path = data_root / "profile.md"
    ensure_profile(profile_path)

    latest = latest_profile_map(profile_path)
    facts = normalize_facts(payload.get("facts"))
    recorded_at = payload.get("recorded_at") or dt.datetime.now().astimezone().isoformat()
    if not isinstance(recorded_at, str):
        raise ProfileUpdateError("recorded_at must be a string when provided.")

    written = []
    skipped = []
    lines = []
    for fact in facts:
        if should_skip_fact(fact, latest):
            skipped.append(fact)
            continue
        lines.append(render_fact_line(fact, recorded_at))
        written.append(fact)

    if lines:
        with profile_path.open("a", encoding="utf-8") as handle:
            current = profile_path.read_text(encoding="utf-8")
            if current and not current.endswith("\n"):
                handle.write("\n")
            if not current.endswith("\n\n"):
                handle.write("\n")
            for line in lines:
                handle.write(line + "\n")

    return {
        "status": "profile updated",
        "deduplicated": len(written) == 0 and len(skipped) > 0,
        "profile_path": str(profile_path.resolve()),
        "written_facts": written,
        "skipped_facts": skipped,
        "recorded_at": recorded_at,
    }


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args)
        result = update_profile(payload, args)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ProfileUpdateError as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
