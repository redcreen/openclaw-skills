#!/usr/bin/env python3
"""Render stable doctor-style replies from the local health summary JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


GAP_LABELS = {
    "zh": {
        "age_or_birth_year": "年龄或出生年",
        "sex": "性别",
        "height_cm": "身高",
        "main_health_goal": "主要健康目标",
        "known_conditions": "已知疾病",
        "current_medications": "当前用药",
    },
    "en": {
        "age_or_birth_year": "age or birth year",
        "sex": "sex",
        "height_cm": "height",
        "main_health_goal": "main health goal",
        "known_conditions": "known conditions",
        "current_medications": "current medications",
    },
}


class ReplyRenderError(Exception):
    """Raised when reply rendering inputs are invalid."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a stable family-doctor reply from a health summary."
    )
    parser.add_argument("--summary-file", help="Path to a summary JSON file.")
    parser.add_argument("--summary-json", help="Inline summary JSON.")
    parser.add_argument("--archive-result-file", help="Optional archive result JSON file.")
    parser.add_argument("--archive-result-json", help="Optional inline archive result JSON.")
    parser.add_argument(
        "--language",
        choices=("zh", "en"),
        default="zh",
        help="Reply language.",
    )
    parser.add_argument(
        "--mode",
        choices=("routine", "onboarding", "trend"),
        default="routine",
        help="Reply mode.",
    )
    return parser.parse_args()


def load_json_object(file_arg: str | None, json_arg: str | None, label: str, required: bool) -> dict[str, Any] | None:
    if file_arg and json_arg:
        raise ReplyRenderError(f"Use either --{label}-file or --{label}-json, not both.")
    if not file_arg and not json_arg:
        if required:
            raise ReplyRenderError(f"One of --{label}-file or --{label}-json is required.")
        return None
    raw = Path(file_arg).read_text(encoding="utf-8") if file_arg else json_arg
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ReplyRenderError(f"Invalid {label} JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReplyRenderError(f"{label} must be a JSON object.")
    return payload


def language_map(language: str) -> dict[str, str]:
    return GAP_LABELS.get(language, GAP_LABELS["zh"])


def join_sentences(sentences: list[str], language: str) -> str:
    separator = "" if language == "zh" else " "
    return separator.join(sentence for sentence in sentences if sentence)


def map_gap_labels(gaps: list[str], language: str) -> list[str]:
    labels = language_map(language)
    return [labels.get(gap, gap) for gap in gaps]


def archive_status(archive_result: dict[str, Any] | None, language: str) -> tuple[str, str, str]:
    if not archive_result:
        if language == "zh":
            return ("not_verified", "not-verified", "本次未在此 skill 中核验归档")
        return ("not_verified", "not-verified", "Not verified in this skill")

    status = str(archive_result.get("status") or "").strip().lower()
    deduplicated = bool(archive_result.get("deduplicated"))
    if status == "archived":
        if deduplicated:
            return (
                "already_archived",
                "observed-write-result",
                "已核验，档案中已有同一条记录" if language == "zh" else "Verified; the same archive entry already exists",
            )
        return (
            "archived",
            "observed-write-result",
            "已核验，已入档" if language == "zh" else "Verified and archived",
        )
    if status == "partially archived":
        return (
            "partially_archived",
            "observed-write-result",
            "已部分入档，仍有内容待补" if language == "zh" else "Partially archived; some content still needs follow-up",
        )
    return (
        "not_archived",
        "observed-write-result",
        "未入档" if language == "zh" else "Not archived",
    )


def weight_sentence(summary: dict[str, Any], language: str) -> str | None:
    weight = summary.get("metrics", {}).get("weight")
    if not isinstance(weight, dict):
        return None
    delta = weight.get("delta_kg")
    if language == "zh":
        if delta is None:
            return "最近只有 1 条体重记录，暂时还不足以下趋势结论。"
        if delta <= -0.3:
            return f"最近体重较上一条下降 {abs(delta):.2f}kg。"
        if delta >= 0.3:
            return f"最近体重较上一条上升 {delta:.2f}kg。"
        return "最近体重整体比较平稳。"
    if delta is None:
        return "Only one recent weight reading is available, so trend confidence is still limited."
    if delta <= -0.3:
        return f"Weight is down {abs(delta):.2f} kg versus the previous archived reading."
    if delta >= 0.3:
        return f"Weight is up {delta:.2f} kg versus the previous archived reading."
    return "Weight is broadly stable versus the previous archived reading."


def blood_pressure_sentence(summary: dict[str, Any], language: str) -> tuple[str | None, str | None]:
    bp = summary.get("metrics", {}).get("blood_pressure")
    if not isinstance(bp, dict):
        return (None, None)
    latest = bp.get("latest", {})
    fields = latest.get("fields", {}) if isinstance(latest, dict) else {}
    systolic = fields.get("systolic_mmhg")
    diastolic = fields.get("diastolic_mmhg")
    watchpoint = None
    sentence = None
    if isinstance(systolic, (int, float)) and isinstance(diastolic, (int, float)):
        if systolic >= 140 or diastolic >= 90:
            sentence = "最近血压偏高，需要按同口径复测看是否持续。" if language == "zh" else "Recent blood pressure is in a high range and should be rechecked under the same conditions."
            watchpoint = "high-blood-pressure"
        elif systolic >= 130 or diastolic >= 85:
            sentence = "最近血压高于理想值，但还不算急迫异常。" if language == "zh" else "Recent blood pressure is above the ideal range, but not in an urgent range."
            watchpoint = "elevated-blood-pressure"
        elif systolic < 90 or diastolic < 60:
            sentence = "最近血压偏低，需要结合症状判断。" if language == "zh" else "Recent blood pressure is low and should be interpreted with symptoms."
            watchpoint = "low-blood-pressure"
        else:
            sentence = "最近血压处于非紧急范围内。" if language == "zh" else "Recent blood pressure is in a non-urgent range."
    return (sentence, watchpoint)


def exercise_sentence(summary: dict[str, Any], language: str) -> str | None:
    exercise = summary.get("metrics", {}).get("exercise")
    if not isinstance(exercise, dict):
        return None
    sessions = exercise.get("sessions")
    if not isinstance(sessions, int):
        return None
    if language == "zh":
        return f"最近已归档 {sessions} 次运动记录。"
    return f"{sessions} recent exercise session(s) are archived."


def doctor_view(summary: dict[str, Any], mode: str, language: str) -> tuple[str, str | None]:
    sentences: list[str] = []
    weight = weight_sentence(summary, language)
    bp, watchpoint = blood_pressure_sentence(summary, language)
    exercise = exercise_sentence(summary, language)
    profile_gaps = summary.get("profile", {}).get("gaps", [])

    if mode == "onboarding":
        if language == "zh":
            if profile_gaps:
                sentences.append("目前已经有初步健康记录，但档案还不够完整。")
            else:
                sentences.append("基础档案已经可用，可以进入持续跟踪。")
        else:
            if profile_gaps:
                sentences.append("A baseline health record exists, but the profile is still incomplete.")
            else:
                sentences.append("The baseline profile is usable and ready for ongoing follow-up.")

    for item in (bp, weight, exercise):
        if item:
            sentences.append(item)
        if len(sentences) >= 2 and mode != "onboarding":
            break

    if not sentences:
        if language == "zh":
            sentences.append("当前本地健康记录还很少，需要先补一些基础数据。")
        else:
            sentences.append("The local health record is still sparse and needs more baseline data.")

    return (join_sentences(sentences[:3], language), watchpoint)


def advice(summary: dict[str, Any], mode: str, language: str, watchpoint: str | None) -> str:
    gaps = summary.get("profile", {}).get("gaps", [])
    exercise = summary.get("metrics", {}).get("exercise")
    weight = summary.get("metrics", {}).get("weight")
    bp = summary.get("metrics", {}).get("blood_pressure")

    if language == "zh":
        if watchpoint == "high-blood-pressure":
            return "今天按标准条件再测 1 次血压；如果连续偏高或伴不适，联系医生。"
        if watchpoint == "low-blood-pressure":
            return "先结合症状复测一次；如果头晕、乏力明显，尽快联系医生。"
        if gaps:
            return "先补齐" + "、".join(map_gap_labels(gaps[:3], language)) + "，后续判断会更稳。"
        if not exercise:
            return "本周补至少 1 次可持续运动记录，方便后续看生活方式变化。"
        if isinstance(weight, dict) and weight.get("recent_count", 0) < 2:
            return "继续按同口径记录 3-5 天晨测，再看趋势会更稳。"
        if isinstance(bp, dict) and bp.get("recent_count", 0) < 2:
            return "继续按同口径补几次血压记录，判断会比单次更可靠。"
        return "继续按当前节奏记录晨测、运动和关键症状变化。"

    if watchpoint == "high-blood-pressure":
        return "Repeat blood pressure once today under standard conditions; seek clinician advice if it stays high or symptoms appear."
    if watchpoint == "low-blood-pressure":
        return "Repeat it once and interpret it with symptoms; seek clinician advice if dizziness or fatigue is obvious."
    if gaps:
        return "Fill in " + ", ".join(map_gap_labels(gaps[:3], language)) + " first so later interpretation is more reliable."
    if not exercise:
        return "Add at least one sustainable exercise record this week so lifestyle changes are easier to interpret."
    if isinstance(weight, dict) and weight.get("recent_count", 0) < 2:
        return "Keep the same measurement routine for 3-5 more days before drawing a stronger trend conclusion."
    if isinstance(bp, dict) and bp.get("recent_count", 0) < 2:
        return "Add a few more blood pressure readings under the same conditions before drawing a stronger conclusion."
    return "Keep recording morning measurements, exercise, and key symptom changes."


def plan(summary: dict[str, Any], mode: str, language: str) -> str | None:
    gaps = summary.get("profile", {}).get("gaps", [])
    weight = summary.get("metrics", {}).get("weight")
    bp = summary.get("metrics", {}).get("blood_pressure")
    exercise = summary.get("metrics", {}).get("exercise")

    if language == "zh":
        if mode == "onboarding":
            if gaps:
                return "请先补：" + "、".join(map_gap_labels(gaps[:4], language)) + "。"
            return "继续累计 3-5 天同口径记录。"
        if gaps:
            return "先把" + "、".join(map_gap_labels(gaps[:2], language)) + "补齐。"
        if not exercise:
            return "补 1 次运动记录，并继续晨测。"
        if isinstance(weight, dict) and weight.get("recent_count", 0) < 2:
            return "继续累计几天体重记录。"
        if isinstance(bp, dict) and bp.get("recent_count", 0) < 2:
            return "继续累计几次血压记录。"
        return None

    if mode == "onboarding":
        if gaps:
            return "Please fill in: " + ", ".join(map_gap_labels(gaps[:4], language)) + "."
        return "Next, keep building 3-5 days of comparable records."
    if gaps:
        return "Next, fill in " + ", ".join(map_gap_labels(gaps[:2], language)) + "."
    if not exercise:
        return "Next, add one exercise record and keep the morning measurements going."
    if isinstance(weight, dict) and weight.get("recent_count", 0) < 2:
        return "Next, keep collecting a few more weight readings."
    if isinstance(bp, dict) and bp.get("recent_count", 0) < 2:
        return "Next, keep collecting a few more blood pressure readings."
    return None


def profile_status(summary: dict[str, Any], language: str) -> tuple[str, str]:
    gaps = summary.get("profile", {}).get("gaps", [])
    if language == "zh":
        if gaps:
            return ("incomplete", f"基础档案未完整，仍缺 {len(gaps)} 类关键信息。")
        return ("ready", "基础档案已可用。")
    if gaps:
        return ("incomplete", f"The baseline profile is incomplete; {len(gaps)} key category(s) are still missing.")
    return ("ready", "The baseline profile is usable.")


def render_markdown(mode: str, language: str, sections: dict[str, Any]) -> str:
    if language == "zh":
        lines = []
        if mode == "onboarding":
            lines.append(f"记录状态：{sections['record_status']}")
            lines.append(f"档案状态：{sections['profile_status']}")
            lines.append(f"医生判断：{sections['doctor_view']}")
            lines.append(f"下一步问题：{sections['next_questions']}")
            return "\n".join(lines)
        lines.append(f"记录状态：{sections['record_status']}")
        lines.append(f"医生判断：{sections['doctor_view']}")
        lines.append(f"建议：{sections['advice']}")
        if sections.get("plan"):
            lines.append(f"下一步：{sections['plan']}")
        return "\n".join(lines)

    lines = []
    if mode == "onboarding":
        lines.append(f"Record Status: {sections['record_status']}")
        lines.append(f"Profile Status: {sections['profile_status']}")
        lines.append(f"Doctor View: {sections['doctor_view']}")
        lines.append(f"Next Questions: {sections['next_questions']}")
        return "\n".join(lines)
    lines.append(f"Record Status: {sections['record_status']}")
    lines.append(f"Doctor View: {sections['doctor_view']}")
    lines.append(f"Advice: {sections['advice']}")
    if sections.get("plan"):
        lines.append(f"Plan: {sections['plan']}")
    return "\n".join(lines)


def render_reply(summary: dict[str, Any], archive_result: dict[str, Any] | None, language: str, mode: str) -> dict[str, Any]:
    record_status_code, archive_status_source, record_status_text = archive_status(archive_result, language)
    doctor_view_text, watchpoint = doctor_view(summary, mode, language)
    plan_text = plan(summary, mode, language)

    if mode == "onboarding":
        profile_status_code, profile_status_text = profile_status(summary, language)
        sections = {
            "record_status": record_status_text,
            "profile_status": profile_status_text,
            "doctor_view": doctor_view_text,
            "next_questions": plan_text or (
                "暂无额外问题。" if language == "zh" else "No further questions right now."
            ),
        }
        markdown = render_markdown(mode, language, sections)
        return {
            "status": "ok",
            "mode": mode,
            "language": language,
            "archive_status_source": archive_status_source,
            "record_status_code": record_status_code,
            "profile_status_code": profile_status_code,
            "sections": sections,
            "markdown": markdown,
        }

    sections = {
        "record_status": record_status_text,
        "doctor_view": doctor_view_text,
        "advice": advice(summary, mode, language, watchpoint),
        "plan": plan_text,
    }
    markdown = render_markdown(mode, language, sections)
    return {
        "status": "ok",
        "mode": mode,
        "language": language,
        "archive_status_source": archive_status_source,
        "record_status_code": record_status_code,
        "watchpoint": watchpoint,
        "sections": sections,
        "markdown": markdown,
    }


def main() -> int:
    args = parse_args()
    try:
        summary = load_json_object(args.summary_file, args.summary_json, "summary", required=True)
        archive_result = load_json_object(
            args.archive_result_file,
            args.archive_result_json,
            "archive-result",
            required=False,
        )
        rendered = render_reply(summary, archive_result, args.language, args.mode)
        print(json.dumps(rendered, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ReplyRenderError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
