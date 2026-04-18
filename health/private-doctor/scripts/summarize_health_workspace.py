#!/usr/bin/env python3
"""Summarize a local health workspace for the private-doctor skill."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_DATA_ROOT = Path("~/document/personal health").expanduser()
PROFILE_LINE_RE = re.compile(r"^- (?P<timestamp>[^|]+)\|\s*(?P<body>.+)$")


class SummaryError(Exception):
    """Raised when the workspace cannot be summarized."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize the local health workspace for doctor-style interpretation."
    )
    parser.add_argument("--data-root", help="Override the external health data root.")
    parser.add_argument("--days", type=int, default=14, help="Recent lookback window in days.")
    parser.add_argument(
        "--recent-limit",
        type=int,
        default=8,
        help="Maximum number of recent entries to include in the summary.",
    )
    return parser.parse_args()


def choose_data_root(arg_root: str | None) -> Path:
    if arg_root:
        return Path(arg_root).expanduser()
    env_root = os.environ.get("HEALTH_DATA_ROOT") or os.environ.get("HEALTH_ARCHIVE_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return DEFAULT_DATA_ROOT


def parse_datetime(raw_value: Any) -> dt.datetime | None:
    if raw_value in (None, ""):
        return None
    if not isinstance(raw_value, str):
        return None
    candidate = raw_value.strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.datetime.now().astimezone().tzinfo)
    return parsed


def parse_date(raw_value: Any) -> dt.date | None:
    if not isinstance(raw_value, str):
        return None
    try:
        return dt.date.fromisoformat(raw_value)
    except ValueError:
        return None


def load_archive_entries(log_path: Path) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []
    entries = []
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


def entry_timestamp(entry: dict[str, Any]) -> dt.datetime:
    for key in ("recorded_at", "archived_at"):
        parsed = parse_datetime(entry.get(key))
        if parsed is not None:
            return parsed
    recorded_on = parse_date(entry.get("recorded_on"))
    if recorded_on is not None:
        return dt.datetime.combine(
            recorded_on,
            dt.time.min,
            tzinfo=dt.datetime.now().astimezone().tzinfo,
        )
    return dt.datetime.min.replace(tzinfo=dt.timezone.utc)


def recent_entries(entries: list[dict[str, Any]], days: int) -> list[dict[str, Any]]:
    if not entries:
        return []
    cutoff = dt.datetime.now().astimezone() - dt.timedelta(days=max(days, 1))
    return [entry for entry in entries if entry_timestamp(entry) >= cutoff]


def compact_entry(entry: dict[str, Any]) -> dict[str, Any]:
    compact = {
        "entry_id": entry.get("entry_id"),
        "entry_type": entry.get("entry_type"),
        "recorded_on": entry.get("recorded_on"),
        "recorded_at": entry.get("recorded_at"),
        "fields": entry.get("fields", {}),
    }
    if entry.get("doctor_note"):
        compact["doctor_note"] = entry["doctor_note"]
    return compact


def float_value(entry: dict[str, Any], field_name: str) -> float | None:
    value = entry.get("fields", {}).get(field_name)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def latest_entries_by_type(entries: list[dict[str, Any]], prefix: str | None = None) -> list[dict[str, Any]]:
    filtered = []
    for entry in entries:
        entry_type = str(entry.get("entry_type") or "")
        if prefix is None and entry_type:
            filtered.append(entry)
        elif prefix is not None and entry_type.startswith(prefix):
            filtered.append(entry)
    return sorted(filtered, key=entry_timestamp)


def summarize_weight(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    weight_entries = [
        entry for entry in sorted(entries, key=entry_timestamp) if float_value(entry, "weight_kg") is not None
    ]
    if not weight_entries:
        return None
    latest = weight_entries[-1]
    previous = weight_entries[-2] if len(weight_entries) >= 2 else None
    latest_value = float_value(latest, "weight_kg")
    previous_value = float_value(previous, "weight_kg") if previous else None
    delta = None
    if latest_value is not None and previous_value is not None:
        delta = round(latest_value - previous_value, 2)
    trend = "unknown"
    if delta is not None:
        if delta <= -0.3:
            trend = "down"
        elif delta >= 0.3:
            trend = "up"
        else:
            trend = "flat"
    return {
        "latest": compact_entry(latest),
        "previous": compact_entry(previous) if previous else None,
        "delta_kg": delta,
        "trend": trend,
        "recent_count": len(weight_entries),
    }


def average(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 1)


def summarize_blood_pressure(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    bp_entries = []
    for entry in sorted(entries, key=entry_timestamp):
        systolic = float_value(entry, "systolic_mmhg")
        diastolic = float_value(entry, "diastolic_mmhg")
        pulse = float_value(entry, "pulse_bpm")
        if systolic is None and diastolic is None and pulse is None:
            continue
        bp_entries.append(entry)
    if not bp_entries:
        return None
    latest = bp_entries[-1]
    systolics = [float_value(entry, "systolic_mmhg") for entry in bp_entries]
    diastolics = [float_value(entry, "diastolic_mmhg") for entry in bp_entries]
    pulses = [float_value(entry, "pulse_bpm") for entry in bp_entries]
    return {
        "latest": compact_entry(latest),
        "recent_count": len(bp_entries),
        "recent_average": {
            "systolic_mmhg": average([value for value in systolics if value is not None]),
            "diastolic_mmhg": average([value for value in diastolics if value is not None]),
            "pulse_bpm": average([value for value in pulses if value is not None]),
        },
    }


def summarize_exercise(entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    exercise_entries = [
        entry
        for entry in sorted(entries, key=entry_timestamp)
        if str(entry.get("entry_type") or "").startswith("exercise-")
    ]
    if not exercise_entries:
        return None
    totals = {
        "sessions": len(exercise_entries),
        "total_duration_min": 0.0,
        "total_distance_km": 0.0,
        "total_steps": 0,
        "by_type": {},
    }
    for entry in exercise_entries:
        entry_type = str(entry.get("entry_type") or "exercise-unknown")
        bucket = totals["by_type"].setdefault(
            entry_type,
            {"sessions": 0, "total_duration_min": 0.0, "total_distance_km": 0.0, "total_steps": 0},
        )
        bucket["sessions"] += 1
        duration = float_value(entry, "duration_min") or 0.0
        distance = float_value(entry, "distance_km") or 0.0
        steps = entry.get("fields", {}).get("steps") or 0
        if not isinstance(steps, int):
            steps = int(steps) if isinstance(steps, float) else 0
        bucket["total_duration_min"] += duration
        bucket["total_distance_km"] += distance
        bucket["total_steps"] += steps
        totals["total_duration_min"] += duration
        totals["total_distance_km"] += distance
        totals["total_steps"] += steps
    totals["sessions"] = len(exercise_entries)
    totals["latest"] = compact_entry(exercise_entries[-1])
    totals["total_duration_min"] = round(totals["total_duration_min"], 1)
    totals["total_distance_km"] = round(totals["total_distance_km"], 2)
    for bucket in totals["by_type"].values():
        bucket["total_duration_min"] = round(bucket["total_duration_min"], 1)
        bucket["total_distance_km"] = round(bucket["total_distance_km"], 2)
    return totals


def parse_literal(raw_value: str) -> Any:
    candidate = raw_value.strip()
    if not candidate:
        return ""
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return candidate


def parse_profile_md(profile_path: Path) -> dict[str, Any]:
    if not profile_path.exists():
        return {"facts": [], "latest_by_label": {}, "raw_lines": []}

    facts: list[dict[str, Any]] = []
    latest_by_label: dict[str, dict[str, Any]] = {}
    raw_lines: list[str] = []

    for line in profile_path.read_text(encoding="utf-8").splitlines():
        raw_lines.append(line)
        match = PROFILE_LINE_RE.match(line)
        if not match:
            continue
        timestamp = match.group("timestamp").strip()
        body = match.group("body").strip()
        fact: dict[str, Any] = {"recorded_at": timestamp}
        if "=" not in body:
            fact["text"] = body
            facts.append(fact)
            continue
        for part in body.split(","):
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            fact[key.strip()] = parse_literal(value)
        facts.append(fact)
        label = fact.get("label")
        if isinstance(label, str) and label.strip():
            latest_by_label[label.strip()] = {
                "value": fact.get("value"),
                "recorded_at": timestamp,
            }
    return {
        "facts": facts,
        "latest_by_label": latest_by_label,
        "raw_lines": raw_lines,
    }


def profile_gaps(latest_by_label: dict[str, dict[str, Any]]) -> list[str]:
    gap_rules = {
        "age_or_birth_year": ["age", "birth_year"],
        "sex": ["sex"],
        "height_cm": ["height_cm"],
        "main_health_goal": ["main_health_goal", "goal_weight_kg"],
        "known_conditions": ["known_conditions", "conditions"],
        "current_medications": ["current_medications", "medications"],
    }
    gaps = []
    for group, labels in gap_rules.items():
        if not any(label in latest_by_label for label in labels):
            gaps.append(group)
    return gaps


def build_doctor_snapshot(
    weight_summary: dict[str, Any] | None,
    bp_summary: dict[str, Any] | None,
    exercise_summary: dict[str, Any] | None,
    recent_count: int,
    gaps: list[str],
) -> dict[str, Any]:
    summary_lines: list[str] = []
    watchpoints: list[str] = []
    follow_up_topics: list[str] = []

    if recent_count == 0:
        follow_up_topics.append("No archived measurements are available yet.")

    if weight_summary is not None:
        delta = weight_summary.get("delta_kg")
        if delta is None:
            summary_lines.append("One archived weight reading is available.")
        elif delta <= -0.3:
            summary_lines.append(f"Weight is down {abs(delta):.2f} kg from the previous archived reading.")
        elif delta >= 0.3:
            summary_lines.append(f"Weight is up {delta:.2f} kg from the previous archived reading.")
        else:
            summary_lines.append("Weight is broadly stable versus the previous archived reading.")

    if bp_summary is not None:
        latest_fields = bp_summary["latest"].get("fields", {})
        systolic = latest_fields.get("systolic_mmhg")
        diastolic = latest_fields.get("diastolic_mmhg")
        if isinstance(systolic, (int, float)) and isinstance(diastolic, (int, float)):
            if systolic >= 140 or diastolic >= 90:
                watchpoints.append("Latest archived blood pressure is in a high range and should be rechecked.")
            elif systolic < 90 or diastolic < 60:
                watchpoints.append("Latest archived blood pressure is in a low range and should be interpreted with symptoms.")
            else:
                summary_lines.append("Latest archived blood pressure sits in a non-urgent range.")
        avg = bp_summary.get("recent_average", {})
        avg_sys = avg.get("systolic_mmhg")
        avg_dia = avg.get("diastolic_mmhg")
        if avg_sys is not None and avg_dia is not None and bp_summary.get("recent_count", 0) >= 2:
            summary_lines.append(f"Recent archived blood pressure averages about {avg_sys}/{avg_dia} mmHg.")

    if exercise_summary is not None:
        sessions = exercise_summary.get("sessions", 0)
        summary_lines.append(f"{sessions} recent archived exercise session(s) are available.")
    else:
        follow_up_topics.append("No recent archived exercise is available.")

    if gaps:
        follow_up_topics.append("Profile gaps remain: " + ", ".join(gaps) + ".")

    return {
        "summary_lines": summary_lines,
        "watchpoints": watchpoints,
        "follow_up_topics": follow_up_topics,
    }


def summarize_workspace(data_root: Path, days: int, recent_limit: int) -> dict[str, Any]:
    if not data_root.exists():
        raise SummaryError(f"Health data root does not exist: {data_root}")

    archive_entries = load_archive_entries(data_root / "archive-log.jsonl")
    ordered_entries = sorted(archive_entries, key=entry_timestamp)
    recent = recent_entries(ordered_entries, days)
    profile = parse_profile_md(data_root / "profile.md")

    weight_summary = summarize_weight(recent)
    bp_summary = summarize_blood_pressure(recent)
    exercise_summary = summarize_exercise(recent)
    gaps = profile_gaps(profile["latest_by_label"])
    snapshot = build_doctor_snapshot(
        weight_summary=weight_summary,
        bp_summary=bp_summary,
        exercise_summary=exercise_summary,
        recent_count=len(recent),
        gaps=gaps,
    )

    return {
        "status": "ok",
        "generated_at": dt.datetime.now().astimezone().isoformat(),
        "data_root": str(data_root.resolve()),
        "record_count": len(ordered_entries),
        "recent_window_days": max(days, 1),
        "recent_count": len(recent),
        "profile": {
            "latest_by_label": profile["latest_by_label"],
            "fact_count": len(profile["facts"]),
            "gaps": gaps,
        },
        "metrics": {
            "weight": weight_summary,
            "blood_pressure": bp_summary,
            "exercise": exercise_summary,
        },
        "doctor_snapshot": snapshot,
        "recent_entries": [compact_entry(entry) for entry in sorted(recent, key=entry_timestamp, reverse=True)[:recent_limit]],
    }


def main() -> int:
    args = parse_args()
    try:
        summary = summarize_workspace(
            choose_data_root(args.data_root),
            args.days,
            args.recent_limit,
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except SummaryError as exc:
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
