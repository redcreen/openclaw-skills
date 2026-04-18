#!/usr/bin/env python3
"""Generate longitudinal health reviews from the local health workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any


DEFAULT_DATA_ROOT = Path("~/document/personal health").expanduser()


class ReviewError(Exception):
    """Raised when a health review cannot be generated."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a health review from the local health workspace."
    )
    parser.add_argument("--data-root", help="Override the external health data root.")
    parser.add_argument(
        "--mode",
        choices=("daily", "weekly", "monthly", "custom"),
        default="weekly",
        help="Review window mode.",
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Custom lookback window in days. Required for custom mode.",
    )
    parser.add_argument(
        "--end-date",
        help="Optional review end date in YYYY-MM-DD. Defaults to today in the local timezone.",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Persist the review markdown into the local workspace.",
    )
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
        raise ReviewError("end-date must use YYYY-MM-DD.") from exc


def lookback_days(mode: str, custom_days: int | None) -> int:
    if mode == "daily":
        return 1
    if mode == "weekly":
        return 7
    if mode == "monthly":
        return 30
    if custom_days is None or custom_days < 1:
        raise ReviewError("--days is required for custom mode and must be >= 1.")
    return custom_days


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


def latest_weight(entries: list[dict[str, Any]]) -> tuple[float | None, float | None]:
    weights = [float_field(entry, "weight_kg") for entry in entries]
    weights = [value for value in weights if value is not None]
    if not weights:
        return (None, None)
    latest = weights[-1]
    previous = weights[-2] if len(weights) >= 2 else None
    return (latest, previous)


def blood_pressure_average(entries: list[dict[str, Any]]) -> tuple[float | None, float | None]:
    systolics = [float_field(entry, "systolic_mmhg") for entry in entries]
    diastolics = [float_field(entry, "diastolic_mmhg") for entry in entries]
    systolics = [value for value in systolics if value is not None]
    diastolics = [value for value in diastolics if value is not None]
    avg_sys = round(sum(systolics) / len(systolics), 1) if systolics else None
    avg_dia = round(sum(diastolics) / len(diastolics), 1) if diastolics else None
    return (avg_sys, avg_dia)


def exercise_totals(entries: list[dict[str, Any]]) -> dict[str, Any]:
    exercise_entries = [entry for entry in entries if str(entry.get("entry_type") or "").startswith("exercise-")]
    duration = 0.0
    distance = 0.0
    for entry in exercise_entries:
        duration += float_field(entry, "duration_min") or 0.0
        distance += float_field(entry, "distance_km") or 0.0
    return {
        "sessions": len(exercise_entries),
        "duration_min": round(duration, 1),
        "distance_km": round(distance, 2),
    }


def count_type(entries: list[dict[str, Any]], entry_type: str) -> int:
    return sum(1 for entry in entries if str(entry.get("entry_type") or "") == entry_type)


def review_takeaways(entries: list[dict[str, Any]], mode: str) -> tuple[list[str], list[str]]:
    highlights: list[str] = []
    next_focus: list[str] = []

    latest, previous = latest_weight(entries)
    if latest is not None:
        if previous is None:
            highlights.append("已有体重记录，但趋势样本仍少。")
        else:
            delta = round(latest - previous, 2)
            if delta <= -0.3:
                highlights.append(f"体重较上一条下降 {abs(delta):.2f}kg。")
            elif delta >= 0.3:
                highlights.append(f"体重较上一条上升 {delta:.2f}kg。")
            else:
                highlights.append("体重整体比较平稳。")
    else:
        next_focus.append("补一条体重记录。")

    avg_sys, avg_dia = blood_pressure_average(entries)
    if avg_sys is not None and avg_dia is not None:
        if avg_sys >= 140 or avg_dia >= 90:
            highlights.append(f"这一阶段血压均值约 {avg_sys}/{avg_dia} mmHg，偏高。")
            next_focus.append("继续按同口径复测血压。")
        elif avg_sys >= 130 or avg_dia >= 85:
            highlights.append(f"这一阶段血压均值约 {avg_sys}/{avg_dia} mmHg，高于理想值。")
            next_focus.append("继续观察血压趋势。")
        else:
            highlights.append(f"这一阶段血压均值约 {avg_sys}/{avg_dia} mmHg。")
    else:
        next_focus.append("补血压记录。")

    exercise = exercise_totals(entries)
    if exercise["sessions"] > 0:
        highlights.append(
            f"共记录 {exercise['sessions']} 次运动，累计约 {exercise['duration_min']} 分钟。"
        )
    else:
        next_focus.append("补至少 1 次运动记录。")

    symptom_count = count_type(entries, "symptom")
    medication_count = count_type(entries, "medication")
    if symptom_count > 0:
        highlights.append(f"这一阶段记录到 {symptom_count} 条症状信息。")
        next_focus.append("继续观察症状变化。")
    if medication_count > 0:
        highlights.append(f"这一阶段记录到 {medication_count} 条用药相关信息。")

    if not highlights:
        highlights.append("这一阶段可用记录还比较少，结论以补数据为主。")

    if not next_focus:
        if mode == "daily":
            next_focus.append("明天继续按同口径记录。")
        else:
            next_focus.append("继续保持同口径记录，方便看趋势。")

    return (highlights, next_focus)


def render_markdown(mode: str, start_date: dt.date, end_date: dt.date, record_count: int, highlights: list[str], next_focus: list[str]) -> str:
    title = {
        "daily": "Daily Health Review",
        "weekly": "Weekly Health Review",
        "monthly": "Monthly Health Review",
        "custom": "Health Review",
    }.get(mode, "Health Review")
    lines = [
        f"# {title}",
        "",
        f"- Review Window: `{start_date.isoformat()} -> {end_date.isoformat()}`",
        f"- Records Included: `{record_count}`",
        "",
        "## Main Takeaways",
        "",
    ]
    for item in highlights:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Focus", ""])
    for item in next_focus:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def save_review(data_root: Path, mode: str, end_date: dt.date, markdown: str, payload: dict[str, Any]) -> tuple[str, str]:
    now = dt.datetime.now().astimezone()
    review_dir = data_root / "reviews" / end_date.strftime("%Y") / end_date.strftime("%m") / end_date.strftime("%d")
    review_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{now.strftime('%Y%m%dT%H%M%S%z')}_{mode}-review"
    markdown_path = review_dir / f"{stem}.md"
    json_path = review_dir / f"{stem}.json"
    markdown_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return (str(markdown_path.resolve()), str(json_path.resolve()))


def generate_review(args: argparse.Namespace) -> dict[str, Any]:
    data_root = choose_data_root(args.data_root)
    if not data_root.exists():
        raise ReviewError(f"Health data root does not exist: {data_root}")
    end_date = parse_end_date(args.end_date)
    days = lookback_days(args.mode, args.days)
    start_date = end_date - dt.timedelta(days=days - 1)
    entries = filter_entries(load_archive_entries(data_root / "archive-log.jsonl"), start_date, end_date)
    highlights, next_focus = review_takeaways(entries, args.mode)
    payload = {
        "status": "ok",
        "mode": args.mode,
        "data_root": str(data_root.resolve()),
        "review_window": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days,
        },
        "record_count": len(entries),
        "highlights": highlights,
        "next_focus": next_focus,
    }
    payload["markdown"] = render_markdown(args.mode, start_date, end_date, len(entries), highlights, next_focus)
    if args.save:
        markdown_path, json_path = save_review(data_root, args.mode, end_date, payload["markdown"], payload)
        payload["saved_markdown_path"] = markdown_path
        payload["saved_json_path"] = json_path
    return payload


def main() -> int:
    args = parse_args()
    try:
        payload = generate_review(args)
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ReviewError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
