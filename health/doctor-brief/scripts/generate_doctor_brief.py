#!/usr/bin/env python3
"""Generate clinician-readable health briefs from the local health workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_DATA_ROOT = Path("~/Documents/personal health").expanduser()
PROFILE_LINE_RE = re.compile(r"^- (?P<timestamp>[^|]+)\|\s*(?P<body>.+)$")


class BriefError(Exception):
    """Raised when a doctor brief cannot be generated."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a clinician-readable brief from the local health workspace."
    )
    parser.add_argument("--data-root", help="Override the external health data root.")
    parser.add_argument("--days", type=int, default=30, help="Recent lookback window in days.")
    parser.add_argument("--end-date", help="Optional end date in YYYY-MM-DD.")
    parser.add_argument("--save", action="store_true", help="Persist the brief into the local workspace.")
    return parser.parse_args()


def choose_data_root(arg_root: str | None) -> Path:
    if arg_root:
        return Path(arg_root).expanduser()
    env_root = os.environ.get("HEALTH_DATA_ROOT") or os.environ.get("HEALTH_ARCHIVE_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return DEFAULT_DATA_ROOT


def parse_end_date(raw_value: str | None) -> dt.date:
    if not raw_value:
        return dt.datetime.now().astimezone().date()
    try:
        return dt.date.fromisoformat(raw_value)
    except ValueError as exc:
        raise BriefError("end-date must use YYYY-MM-DD.") from exc


def load_archive_entries(log_path: Path) -> list[dict[str, Any]]:
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


def parse_literal(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def parse_profile(profile_path: Path) -> dict[str, Any]:
    latest: dict[str, Any] = {}
    if not profile_path.exists():
        return latest
    for line in profile_path.read_text(encoding="utf-8").splitlines():
        match = PROFILE_LINE_RE.match(line)
        if not match:
            continue
        body = match.group("body").strip()
        if "=" not in body:
            continue
        parts: dict[str, Any] = {}
        for chunk in body.split(","):
            if "=" not in chunk:
                continue
            key, value = chunk.split("=", 1)
            parts[key.strip()] = parse_literal(value.strip())
        label = parts.get("label")
        if isinstance(label, str):
            latest[label] = parts.get("value")
    return latest


def parse_date(value: Any) -> dt.date | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def filter_entries(entries: list[dict[str, Any]], start_date: dt.date, end_date: dt.date) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for entry in entries:
        recorded_on = parse_date(entry.get("recorded_on"))
        if recorded_on is None:
            continue
        if start_date <= recorded_on <= end_date:
            filtered.append(entry)
    return sorted(filtered, key=lambda item: (item.get("recorded_on") or "", item.get("recorded_at") or "", item.get("archived_at") or ""))


def float_field(entry: dict[str, Any], name: str) -> float | None:
    value = entry.get("fields", {}).get(name)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def latest_weight_summary(entries: list[dict[str, Any]]) -> str | None:
    weights = [float_field(entry, "weight_kg") for entry in entries]
    weights = [value for value in weights if value is not None]
    if not weights:
        return None
    latest = weights[-1]
    if len(weights) < 2:
        return f"Latest archived weight: {latest:.2f} kg."
    delta = round(latest - weights[-2], 2)
    if delta <= -0.3:
        return f"Latest archived weight: {latest:.2f} kg, down {abs(delta):.2f} kg versus the previous archived reading."
    if delta >= 0.3:
        return f"Latest archived weight: {latest:.2f} kg, up {delta:.2f} kg versus the previous archived reading."
    return f"Latest archived weight: {latest:.2f} kg, broadly stable versus the previous archived reading."


def blood_pressure_summary(entries: list[dict[str, Any]]) -> str | None:
    systolics = [float_field(entry, "systolic_mmhg") for entry in entries]
    diastolics = [float_field(entry, "diastolic_mmhg") for entry in entries]
    systolics = [value for value in systolics if value is not None]
    diastolics = [value for value in diastolics if value is not None]
    if not systolics or not diastolics:
        return None
    avg_sys = round(sum(systolics) / len(systolics), 1)
    avg_dia = round(sum(diastolics) / len(diastolics), 1)
    latest_sys = systolics[-1]
    latest_dia = diastolics[-1]
    return f"Recent archived blood pressure averages about {avg_sys}/{avg_dia} mmHg; latest archived reading is {latest_sys}/{latest_dia} mmHg."


def exercise_summary(entries: list[dict[str, Any]]) -> str | None:
    exercise_entries = [entry for entry in entries if str(entry.get("entry_type") or "").startswith("exercise-")]
    if not exercise_entries:
        return None
    duration = 0.0
    distance = 0.0
    for entry in exercise_entries:
        duration += float_field(entry, "duration_min") or 0.0
        distance += float_field(entry, "distance_km") or 0.0
    return f"Archived exercise in this window: {len(exercise_entries)} session(s), about {round(duration, 1)} minutes total, {round(distance, 2)} km total."


def symptom_summary(entries: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    symptom_entries = [entry for entry in entries if str(entry.get("entry_type") or "") == "symptom"]
    for entry in symptom_entries[:5]:
        fields = entry.get("fields", {})
        label = fields.get("symptom") or fields.get("description") or entry.get("doctor_note") or "symptom recorded"
        lines.append(f"{entry.get('recorded_on')}: {label}")
    return lines


def medication_context(profile: dict[str, Any], entries: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for label in ("current_medications", "medications"):
        value = profile.get(label)
        if value:
            lines.append(f"Profile medication context: {value}")
    medication_entries = [entry for entry in entries if str(entry.get("entry_type") or "") == "medication"]
    for entry in medication_entries[:5]:
        fields = entry.get("fields", {})
        detail = fields.get("medication_name") or fields.get("name") or entry.get("doctor_note") or "medication event"
        lines.append(f"{entry.get('recorded_on')}: {detail}")
    return lines


def profile_snapshot(profile: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if profile.get("age"):
        lines.append(f"Age: {profile['age']}")
    elif profile.get("birth_year"):
        lines.append(f"Birth year: {profile['birth_year']}")
    if profile.get("sex"):
        lines.append(f"Sex: {profile['sex']}")
    if profile.get("height_cm"):
        lines.append(f"Height: {profile['height_cm']} cm")
    if profile.get("main_health_goal"):
        lines.append(f"Main goal: {profile['main_health_goal']}")
    if profile.get("goal_weight_kg"):
        lines.append(f"Goal weight: {profile['goal_weight_kg']} kg")
    if profile.get("known_conditions"):
        lines.append(f"Known conditions: {profile['known_conditions']}")
    elif profile.get("conditions"):
        lines.append(f"Known conditions: {profile['conditions']}")
    return lines


def follow_up_points(entries: list[dict[str, Any]], profile: dict[str, Any]) -> list[str]:
    points: list[str] = []
    bp = blood_pressure_summary(entries)
    if bp and "140/" in bp:
        points.append("Clarify whether recent blood pressure elevations are persistent and whether medication review is needed.")
    if not any(str(entry.get("entry_type") or "").startswith("exercise-") for entry in entries):
        points.append("Exercise data is sparse in the current window; ask about actual activity level.")
    if not profile.get("current_medications") and not profile.get("medications"):
        points.append("Medication context is incomplete and should be clarified.")
    if not points:
        points.append("Continue reviewing recent measurements against symptoms and adherence.")
    return points


def render_markdown(start_date: dt.date, end_date: dt.date, profile_lines: list[str], trend_lines: list[str], medication_lines: list[str], symptom_lines: list[str], follow_up: list[str]) -> str:
    lines = [
        "# Doctor Brief",
        "",
        f"- Brief Window: `{start_date.isoformat()} -> {end_date.isoformat()}`",
        "",
        "## Patient Snapshot",
        "",
    ]
    if profile_lines:
        for item in profile_lines:
            lines.append(f"- {item}")
    else:
        lines.append("- Baseline profile is still sparse.")
    lines.extend(["", "## Trend Summary", ""])
    if trend_lines:
        for item in trend_lines:
            lines.append(f"- {item}")
    else:
        lines.append("- Recent archived trend data is sparse.")
    lines.extend(["", "## Medication Context", ""])
    if medication_lines:
        for item in medication_lines:
            lines.append(f"- {item}")
    else:
        lines.append("- No medication context recorded in the selected window.")
    lines.extend(["", "## Symptom Signals", ""])
    if symptom_lines:
        for item in symptom_lines:
            lines.append(f"- {item}")
    else:
        lines.append("- No symptom entries recorded in the selected window.")
    lines.extend(["", "## Follow-Up Points", ""])
    for item in follow_up:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def save_brief(data_root: Path, end_date: dt.date, markdown: str, payload: dict[str, Any]) -> tuple[str, str]:
    now = dt.datetime.now().astimezone()
    report_dir = data_root / "reports" / end_date.strftime("%Y") / end_date.strftime("%m") / end_date.strftime("%d")
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{now.strftime('%Y%m%dT%H%M%S%z')}_doctor-brief"
    markdown_path = report_dir / f"{stem}.md"
    json_path = report_dir / f"{stem}.json"
    markdown_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return (str(markdown_path.resolve()), str(json_path.resolve()))


def generate_brief(args: argparse.Namespace) -> dict[str, Any]:
    data_root = choose_data_root(args.data_root)
    if not data_root.exists():
        raise BriefError(f"Health data root does not exist: {data_root}")
    if args.days < 1:
        raise BriefError("--days must be >= 1.")
    end_date = parse_end_date(args.end_date)
    start_date = end_date - dt.timedelta(days=args.days - 1)
    entries = filter_entries(load_archive_entries(data_root / "archive-log.jsonl"), start_date, end_date)
    profile = parse_profile(data_root / "profile.md")

    trend_lines = [line for line in (
        latest_weight_summary(entries),
        blood_pressure_summary(entries),
        exercise_summary(entries),
    ) if line]
    medication_lines = medication_context(profile, entries)
    symptom_lines = symptom_summary(entries)
    profile_lines = profile_snapshot(profile)
    follow_up = follow_up_points(entries, profile)

    payload = {
        "status": "ok",
        "data_root": str(data_root.resolve()),
        "brief_window": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": args.days,
        },
        "profile_snapshot": profile_lines,
        "trend_summary": trend_lines,
        "medication_context": medication_lines,
        "symptom_signals": symptom_lines,
        "follow_up_points": follow_up,
    }
    payload["markdown"] = render_markdown(start_date, end_date, profile_lines, trend_lines, medication_lines, symptom_lines, follow_up)
    if args.save:
        markdown_path, json_path = save_brief(data_root, end_date, payload["markdown"], payload)
        payload["saved_markdown_path"] = markdown_path
        payload["saved_json_path"] = json_path
    return payload


def main() -> int:
    args = parse_args()
    try:
        payload = generate_brief(args)
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except BriefError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
