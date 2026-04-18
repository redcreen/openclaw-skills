#!/usr/bin/env python3
"""Manage local-first health reminder rules and due reminders."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any


DEFAULT_DATA_ROOT = Path("~/Documents/personal health").expanduser()
VALID_KINDS = {"measurement", "medication", "exercise", "review", "general"}


class ReminderError(Exception):
    """Raised when reminder rules cannot be managed."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage local health reminder rules."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    upsert = subparsers.add_parser("upsert", help="Create or update reminder rules.")
    upsert.add_argument("--payload-file", help="Path to a JSON payload file.")
    upsert.add_argument("--payload-json", help="Inline JSON payload.")
    upsert.add_argument("--data-root", help="Override the external health data root.")

    due = subparsers.add_parser("due", help="Evaluate reminders due at a given time.")
    due.add_argument("--data-root", help="Override the external health data root.")
    due.add_argument("--at", help="ISO datetime for due-check. Defaults to now.")
    due.add_argument("--window-minutes", type=int, default=90, help="Trigger window around the scheduled time.")
    due.add_argument("--save", action="store_true", help="Persist the due-check snapshot into the local workspace.")

    listing = subparsers.add_parser("list", help="List active reminder rules.")
    listing.add_argument("--data-root", help="Override the external health data root.")

    return parser


def choose_data_root(arg_root: str | None) -> Path:
    if arg_root:
        return Path(arg_root).expanduser()
    env_root = os.environ.get("HEALTH_DATA_ROOT") or os.environ.get("HEALTH_ARCHIVE_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return DEFAULT_DATA_ROOT


def reminders_dir(data_root: Path) -> Path:
    path = data_root / "reminders"
    path.mkdir(parents=True, exist_ok=True)
    return path


def reminder_plan_path(data_root: Path) -> Path:
    return reminders_dir(data_root) / "reminder-plan.json"


def load_plan(data_root: Path) -> dict[str, Any]:
    path = reminder_plan_path(data_root)
    if not path.exists():
        return {"status": "ok", "reminders": []}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReminderError(f"Invalid reminder plan JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ReminderError("Reminder plan must be a JSON object.")
    reminders = payload.get("reminders")
    if not isinstance(reminders, list):
        raise ReminderError("Reminder plan must contain a reminders list.")
    payload["reminders"] = reminders
    return payload


def load_payload(payload_file: str | None, payload_json: str | None) -> dict[str, Any]:
    if payload_file and payload_json:
        raise ReminderError("Use either --payload-file or --payload-json, not both.")
    if not payload_file and not payload_json:
        raise ReminderError("One of --payload-file or --payload-json is required.")
    raw = Path(payload_file).read_text(encoding="utf-8") if payload_file else payload_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReminderError(f"Invalid JSON payload: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReminderError("Payload must be a JSON object.")
    return payload


def normalize_days(value: Any) -> list[int]:
    if value in (None, "", []):
        return []
    if not isinstance(value, list):
        raise ReminderError("days_of_week must be a list of integers.")
    normalized: list[int] = []
    for item in value:
        if not isinstance(item, int) or item < 0 or item > 6:
            raise ReminderError("days_of_week values must be integers from 0 to 6.")
        normalized.append(item)
    return sorted(set(normalized))


def normalize_time(value: Any) -> str:
    if not isinstance(value, str) or len(value.strip()) != 5 or value[2] != ":":
        raise ReminderError("time_local must use HH:MM.")
    hour = int(value[:2])
    minute = int(value[3:])
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ReminderError("time_local must use a valid HH:MM value.")
    return f"{hour:02d}:{minute:02d}"


def normalize_rule(item: dict[str, Any], fallback_index: int) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ReminderError("Each reminder must be an object.")
    label = item.get("label")
    if not isinstance(label, str) or not label.strip():
        raise ReminderError("Each reminder must include a non-empty label.")
    kind = str(item.get("kind") or "general").strip().lower()
    if kind not in VALID_KINDS:
        raise ReminderError("kind must be one of: measurement, medication, exercise, review, general.")
    rule_id = item.get("id")
    if not isinstance(rule_id, str) or not rule_id.strip():
        rule_id = f"reminder-{fallback_index}"
    rule = {
        "id": rule_id.strip(),
        "label": label.strip(),
        "kind": kind,
        "time_local": normalize_time(item.get("time_local")),
        "enabled": bool(item.get("enabled", True)),
        "days_of_week": normalize_days(item.get("days_of_week")),
        "message": str(item.get("message") or label).strip(),
    }
    target_entry_type = item.get("target_entry_type")
    if target_entry_type:
        rule["target_entry_type"] = str(target_entry_type).strip()
    notes = item.get("notes")
    if notes:
        rule["notes"] = str(notes).strip()
    return rule


def upsert_plan(data_root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    raw_rules = payload.get("reminders")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ReminderError("Payload must contain a non-empty reminders list.")
    plan = load_plan(data_root)
    existing = {item.get("id"): item for item in plan.get("reminders", []) if isinstance(item, dict)}
    written: list[dict[str, Any]] = []
    for index, item in enumerate(raw_rules, start=1):
        rule = normalize_rule(item, index)
        existing[rule["id"]] = rule
        written.append(rule)
    merged_rules = sorted(existing.values(), key=lambda item: item["id"])
    result = {
        "status": "ok",
        "updated_at": dt.datetime.now().astimezone().isoformat(),
        "reminders": merged_rules,
    }
    path = reminder_plan_path(data_root)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "status": "ok",
        "plan_path": str(path.resolve()),
        "updated_rules": written,
        "rule_count": len(merged_rules),
    }


def load_archive_entries(data_root: Path) -> list[dict[str, Any]]:
    log_path = data_root / "archive-log.jsonl"
    if not log_path.exists():
        return []
    entries: list[dict[str, Any]] = []
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                entries.append(payload)
    return entries


def parse_recorded_on(value: Any) -> dt.date | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def satisfied_today(rule: dict[str, Any], entries: list[dict[str, Any]], today: dt.date) -> bool:
    target_entry_type = str(rule.get("target_entry_type") or "").strip()
    kind = rule.get("kind")
    for entry in entries:
        recorded_on = parse_recorded_on(entry.get("recorded_on"))
        if recorded_on != today:
            continue
        entry_type = str(entry.get("entry_type") or "")
        if target_entry_type and entry_type == target_entry_type:
            return True
        if kind == "measurement" and entry_type in {"weight", "blood-pressure"}:
            return True
        if kind == "exercise" and entry_type.startswith("exercise-"):
            return True
        if kind == "medication" and entry_type == "medication":
            return True
    return False


def due_now(rule: dict[str, Any], at_time: dt.datetime, window_minutes: int) -> bool:
    if not rule.get("enabled", True):
        return False
    days_of_week = rule.get("days_of_week") or []
    if days_of_week and at_time.weekday() not in days_of_week:
        return False
    schedule_hour, schedule_minute = [int(part) for part in str(rule["time_local"]).split(":")]
    scheduled = at_time.replace(hour=schedule_hour, minute=schedule_minute, second=0, microsecond=0)
    delta_minutes = abs((at_time - scheduled).total_seconds()) / 60.0
    return delta_minutes <= max(window_minutes, 1)


def summarize_due_rules(due_rules: list[dict[str, Any]], at_time: dt.datetime) -> tuple[str, list[str], list[str], list[str]]:
    if not due_rules:
        return (
            "no reminders due",
            ["No active reminder is due right now."],
            ["No enabled rule matched the current due window."],
            ["Keep following the current plan and check again at the next reminder window."],
        )

    what_is_due: list[str] = []
    why_it_is_due: list[str] = []
    what_to_do_next: list[str] = []
    for rule in due_rules:
        label = str(rule.get("label") or "Reminder").strip()
        kind = str(rule.get("kind") or "general").strip()
        target_entry_type = str(rule.get("target_entry_type") or "").strip()
        time_local = str(rule.get("time_local") or "unspecified")
        message = str(rule.get("message") or label).strip()
        what_is_due.append(f"{label}: {message}")
        reason_target = target_entry_type or kind
        why_it_is_due.append(
            f"{label} is scheduled for {time_local}, and no matching {reason_target} record has been archived for {at_time.date().isoformat()}."
        )
        if kind == "measurement":
            what_to_do_next.append(f"Record the planned measurement for {label} and rerun the due check if needed.")
        elif kind == "medication":
            what_to_do_next.append(f"Take or confirm the medication for {label}, then archive it if that is part of the workflow.")
        elif kind == "exercise":
            what_to_do_next.append(f"Complete the planned exercise for {label} or adjust the rule if the schedule has changed.")
        elif kind == "review":
            what_to_do_next.append(f"Complete the planned health review for {label} and save the result.")
        else:
            what_to_do_next.append(f"Handle {label} now or update the reminder rule if this is no longer needed.")
    return ("due now", what_is_due, why_it_is_due, what_to_do_next)


def render_due_markdown(
    at_time: dt.datetime,
    reminder_status: str,
    what_is_due: list[str],
    why_it_is_due: list[str],
    what_to_do_next: list[str],
) -> str:
    lines = [
        "# Due Health Reminders",
        "",
        f"- Checked At: `{at_time.isoformat()}`",
        f"- Reminder Status: `{reminder_status}`",
        "",
        "## What Is Due",
        "",
    ]
    for item in what_is_due:
        lines.append(f"- {item}")
    lines.extend(["", "## Why It Is Due", ""])
    for item in why_it_is_due:
        lines.append(f"- {item}")
    lines.extend(["", "## What To Do Next", ""])
    for item in what_to_do_next:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def save_due_snapshot(data_root: Path, at_time: dt.datetime, payload: dict[str, Any]) -> tuple[str, str]:
    snapshot_dir = reminders_dir(data_root) / at_time.strftime("%Y") / at_time.strftime("%m") / at_time.strftime("%d")
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{at_time.strftime('%Y%m%dT%H%M%S%z')}_due-reminders"
    markdown_path = snapshot_dir / f"{stem}.md"
    json_path = snapshot_dir / f"{stem}.json"
    markdown_path.write_text(payload["markdown"], encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return (str(markdown_path.resolve()), str(json_path.resolve()))


def due_check(data_root: Path, at_value: str | None, window_minutes: int, save: bool) -> dict[str, Any]:
    plan = load_plan(data_root)
    at_time = dt.datetime.now().astimezone() if not at_value else dt.datetime.fromisoformat(at_value.replace("Z", "+00:00"))
    if at_time.tzinfo is None:
        at_time = at_time.replace(tzinfo=dt.datetime.now().astimezone().tzinfo)
    entries = load_archive_entries(data_root)
    today = at_time.date()
    due_rules: list[dict[str, Any]] = []
    for rule in plan.get("reminders", []):
        if not isinstance(rule, dict):
            continue
        if due_now(rule, at_time, window_minutes) and not satisfied_today(rule, entries, today):
            due_rules.append(rule)
    reminder_status, what_is_due, why_it_is_due, what_to_do_next = summarize_due_rules(due_rules, at_time)
    payload = {
        "status": "ok",
        "checked_at": at_time.isoformat(),
        "data_root": str(data_root.resolve()),
        "due_count": len(due_rules),
        "due_rules": due_rules,
        "reminder_status": reminder_status,
        "what_is_due": what_is_due,
        "why_it_is_due": why_it_is_due,
        "what_to_do_next": what_to_do_next,
    }
    payload["markdown"] = render_due_markdown(at_time, reminder_status, what_is_due, why_it_is_due, what_to_do_next)
    if save:
        markdown_path, json_path = save_due_snapshot(data_root, at_time, payload)
        payload["saved_markdown_path"] = markdown_path
        payload["saved_json_path"] = json_path
    return payload


def list_rules(data_root: Path) -> dict[str, Any]:
    plan = load_plan(data_root)
    return {
        "status": "ok",
        "data_root": str(data_root.resolve()),
        "plan_path": str(reminder_plan_path(data_root).resolve()),
        "rule_count": len(plan.get("reminders", [])),
        "reminders": plan.get("reminders", []),
    }


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "upsert":
            data_root = choose_data_root(args.data_root)
            payload = load_payload(args.payload_file, args.payload_json)
            result = upsert_plan(data_root, payload)
        elif args.command == "due":
            data_root = choose_data_root(args.data_root)
            result = due_check(data_root, args.at, args.window_minutes, args.save)
        else:
            data_root = choose_data_root(args.data_root)
            result = list_rules(data_root)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ReminderError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
