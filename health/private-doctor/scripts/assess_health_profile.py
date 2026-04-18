#!/usr/bin/env python3
"""Assess the baseline health profile and generate an initial family-doctor view."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class AssessmentError(Exception):
    """Raised when a baseline assessment cannot be generated."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assess the baseline health profile from a summary JSON payload."
    )
    parser.add_argument("--summary-file", help="Path to a summary JSON file.")
    parser.add_argument("--summary-json", help="Inline summary JSON.")
    parser.add_argument(
        "--language",
        choices=("zh", "en"),
        default="zh",
        help="Assessment language.",
    )
    return parser.parse_args()


def load_summary(args: argparse.Namespace) -> dict[str, Any]:
    if args.summary_file and args.summary_json:
        raise AssessmentError("Use either --summary-file or --summary-json, not both.")
    if not args.summary_file and not args.summary_json:
        raise AssessmentError("One of --summary-file or --summary-json is required.")
    raw = Path(args.summary_file).read_text(encoding="utf-8") if args.summary_file else args.summary_json
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AssessmentError(f"Invalid summary JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise AssessmentError("Summary must be a JSON object.")
    return payload


def latest_profile_map(summary: dict[str, Any]) -> dict[str, Any]:
    latest = summary.get("profile", {}).get("latest_by_label", {})
    if not isinstance(latest, dict):
        return {}
    return latest


def profile_value(latest: dict[str, Any], *labels: str) -> Any:
    for label in labels:
        candidate = latest.get(label)
        if isinstance(candidate, dict):
            return candidate.get("value")
        if candidate is not None:
            return candidate
    return None


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(stringify(item) for item in value)
    return str(value)


def lower_text(*values: Any) -> str:
    return " ".join(stringify(value).lower() for value in values if value not in (None, "", []))


def missing_profile_fields(latest: dict[str, Any]) -> list[str]:
    checks = [
        ("年龄或出生年" , ("age", "birth_year")),
        ("性别", ("sex",)),
        ("身高", ("height_cm",)),
        ("主要健康目标", ("main_health_goal", "goal_weight_kg")),
        ("已知疾病", ("known_conditions", "conditions")),
        ("当前用药", ("current_medications", "medications")),
        ("血压相关背景", ("blood_pressure_background", "hypertension_history")),
        ("血脂相关背景", ("lipid_background", "hyperlipidemia_history")),
        ("血糖相关背景", ("glucose_background", "diabetes_history", "prediabetes_history")),
    ]
    missing: list[str] = []
    for label, candidates in checks:
        if not any(profile_value(latest, candidate) not in (None, "", []) for candidate in candidates):
            missing.append(label)
    return missing


def bmi_line(summary: dict[str, Any], latest: dict[str, Any], language: str) -> tuple[str | None, list[str]]:
    weight = summary.get("metrics", {}).get("weight", {})
    height_cm = profile_value(latest, "height_cm")
    if not isinstance(weight, dict) or not isinstance(height_cm, (int, float)):
        return (None, [])
    latest_entry = weight.get("latest", {})
    latest_weight = latest_entry.get("fields", {}).get("weight_kg") if isinstance(latest_entry, dict) else None
    if not isinstance(latest_weight, (int, float)) or height_cm <= 0:
        return (None, [])
    bmi = round(float(latest_weight) / ((float(height_cm) / 100.0) ** 2), 1)
    risks: list[str] = []
    if language == "zh":
        if bmi >= 28:
            risks.append("bmi-obesity")
            return (f"按当前身高体重估算，BMI 约 {bmi}，处于肥胖范围。", risks)
        if bmi >= 24:
            risks.append("bmi-overweight")
            return (f"按当前身高体重估算，BMI 约 {bmi}，处于超重范围。", risks)
        return (f"按当前身高体重估算，BMI 约 {bmi}。", risks)
    if bmi >= 28:
        risks.append("bmi-obesity")
        return (f"Estimated BMI is about {bmi}, in an obesity range.", risks)
    if bmi >= 24:
        risks.append("bmi-overweight")
        return (f"Estimated BMI is about {bmi}, in an overweight range.", risks)
    return (f"Estimated BMI is about {bmi}.", risks)


def blood_pressure_line(summary: dict[str, Any], language: str) -> tuple[str | None, list[str]]:
    bp = summary.get("metrics", {}).get("blood_pressure", {})
    if not isinstance(bp, dict):
        return (None, [])
    avg = bp.get("recent_average", {})
    avg_sys = avg.get("systolic_mmhg") if isinstance(avg, dict) else None
    avg_dia = avg.get("diastolic_mmhg") if isinstance(avg, dict) else None
    if not isinstance(avg_sys, (int, float)) or not isinstance(avg_dia, (int, float)):
        return (None, [])
    risks: list[str] = []
    if language == "zh":
        if avg_sys >= 140 or avg_dia >= 90:
            risks.append("high-blood-pressure")
            return (f"最近血压均值约 {avg_sys}/{avg_dia} mmHg，提示血压风险偏高。", risks)
        if avg_sys >= 130 or avg_dia >= 85:
            risks.append("elevated-blood-pressure")
            return (f"最近血压均值约 {avg_sys}/{avg_dia} mmHg，高于理想值。", risks)
        return (f"最近血压均值约 {avg_sys}/{avg_dia} mmHg。", risks)
    if avg_sys >= 140 or avg_dia >= 90:
        risks.append("high-blood-pressure")
        return (f"Recent blood pressure averages about {avg_sys}/{avg_dia} mmHg, suggesting elevated blood-pressure risk.", risks)
    if avg_sys >= 130 or avg_dia >= 85:
        risks.append("elevated-blood-pressure")
        return (f"Recent blood pressure averages about {avg_sys}/{avg_dia} mmHg, above the ideal range.", risks)
    return (f"Recent blood pressure averages about {avg_sys}/{avg_dia} mmHg.", risks)


def condition_lines(latest: dict[str, Any], language: str) -> tuple[list[str], list[str]]:
    conditions = profile_value(latest, "known_conditions", "conditions")
    medications = profile_value(latest, "current_medications", "medications")
    text = lower_text(conditions, medications)
    lines: list[str] = []
    risks: list[str] = []
    if any(token in text for token in ("高血压", "hypertension", "blood pressure")):
        risks.append("known-blood-pressure-context")
        lines.append("已有血压相关背景。" if language == "zh" else "Existing blood-pressure context is already present.")
    if any(token in text for token in ("高血脂", "血脂", "cholesterol", "lipid", "statin")):
        risks.append("known-lipid-context")
        lines.append("已有血脂相关背景。" if language == "zh" else "Existing lipid-related context is already present.")
    if any(token in text for token in ("糖", "glucose", "diabetes", "metformin", "insulin", "prediabetes")):
        risks.append("known-glucose-context")
        lines.append("已有血糖相关背景。" if language == "zh" else "Existing glucose-related context is already present.")
    return (lines, risks)


def first_phase_plan(summary: dict[str, Any], latest: dict[str, Any], language: str, missing: list[str], risk_flags: list[str]) -> list[str]:
    steps: list[str] = []
    if missing:
        if language == "zh":
            steps.append("先补齐：" + "、".join(missing[:4]) + "。")
        else:
            steps.append("Fill in first: " + ", ".join(missing[:4]) + ".")
    if any(flag in risk_flags for flag in ("high-blood-pressure", "elevated-blood-pressure", "known-blood-pressure-context")):
        steps.append(
            "接下来连续 3-5 天按同口径记录血压。" if language == "zh"
            else "Next, record blood pressure under the same conditions for 3-5 more days."
        )
    exercise = summary.get("metrics", {}).get("exercise", {})
    if not isinstance(exercise, dict) or exercise.get("sessions", 0) == 0:
        steps.append(
            "补至少 1 次可持续运动记录。" if language == "zh"
            else "Add at least one sustainable exercise record."
        )
    steps.append(
        "不要根据单次波动自行调整药物，涉及停药/减药请先和医生确认。"
        if language == "zh"
        else "Do not change medication based on one reading alone; confirm stop/reduce decisions with a clinician."
    )
    return steps


def follow_up_focus(language: str, missing: list[str], risk_flags: list[str]) -> list[str]:
    items: list[str] = []
    if any(flag in risk_flags for flag in ("high-blood-pressure", "elevated-blood-pressure")):
        items.append("优先看血压趋势是否持续偏高。" if language == "zh" else "Prioritize whether blood pressure stays elevated across time.")
    if any(flag in risk_flags for flag in ("bmi-overweight", "bmi-obesity")):
        items.append("继续看体重下降是否稳定且可持续。" if language == "zh" else "Keep watching whether weight change stays steady and sustainable.")
    if missing:
        items.append("补全基础档案后再做更稳的长期判断。" if language == "zh" else "Complete the baseline profile before making stronger long-term conclusions.")
    if not items:
        items.append("继续按同口径记录，逐步提高趋势判断把握。" if language == "zh" else "Keep recording under comparable conditions to strengthen trend confidence.")
    return items


def render_markdown(language: str, profile_status: str, assessment_lines: list[str], plan_lines: list[str], next_questions: list[str]) -> str:
    if language == "zh":
        lines = [
            f"档案状态：{profile_status}",
            "初步判断：" + ("；".join(assessment_lines) if assessment_lines else "当前资料还不足以形成稳定初评。"),
            "第一阶段建议：" + ("；".join(plan_lines) if plan_lines else "先补基础资料。"),
            "下一步问题：" + ("；".join(next_questions) if next_questions else "暂无额外问题。"),
        ]
        return "\n".join(lines)
    lines = [
        f"Profile Status: {profile_status}",
        "Initial Assessment: " + (" ".join(assessment_lines) if assessment_lines else "Current data is still too sparse for a stable initial assessment."),
        "First-Phase Plan: " + (" ".join(plan_lines) if plan_lines else "Start by filling the baseline profile."),
        "Next Questions: " + (" ".join(next_questions) if next_questions else "No further questions right now."),
    ]
    return "\n".join(lines)


def assess(summary: dict[str, Any], language: str) -> dict[str, Any]:
    latest = latest_profile_map(summary)
    missing = missing_profile_fields(latest)
    assessment_lines: list[str] = []
    risk_flags: list[str] = []

    bp_line, bp_risks = blood_pressure_line(summary, language)
    if bp_line:
        assessment_lines.append(bp_line)
        risk_flags.extend(bp_risks)

    bmi_summary, bmi_risks = bmi_line(summary, latest, language)
    if bmi_summary:
        assessment_lines.append(bmi_summary)
        risk_flags.extend(bmi_risks)

    condition_summary, condition_risks = condition_lines(latest, language)
    assessment_lines.extend(condition_summary)
    risk_flags.extend(condition_risks)

    if missing:
        assessment_lines.append(
            "基础档案还不完整，当前初评需要随着补档持续修正。"
            if language == "zh"
            else "The baseline profile is still incomplete, so the initial assessment should be refined as the profile fills out."
        )

    profile_status = (
        f"基础档案未完整，仍缺 {len(missing)} 类关键信息。"
        if language == "zh" and missing
        else "基础档案已具备初评条件。"
        if language == "zh"
        else f"The baseline profile is incomplete; {len(missing)} key area(s) are still missing."
        if missing
        else "The baseline profile is strong enough for a first-pass assessment."
    )

    plan_lines = first_phase_plan(summary, latest, language, missing, risk_flags)
    next_questions = missing[:4] if missing else follow_up_focus(language, missing, risk_flags)
    markdown = render_markdown(language, profile_status, assessment_lines, plan_lines, next_questions)
    return {
        "status": "ok",
        "language": language,
        "profile_status": profile_status,
        "missing_profile_fields": missing,
        "risk_flags": sorted(set(risk_flags)),
        "assessment_lines": assessment_lines,
        "first_phase_plan": plan_lines,
        "next_questions": next_questions,
        "markdown": markdown,
    }


def main() -> int:
    args = parse_args()
    try:
        summary = load_summary(args)
        result = assess(summary, args.language)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except AssessmentError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
