#!/usr/bin/env python3
"""CLI acceptance for the health skill suite."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


INSTALLER = Path.home() / ".codex" / "skills" / ".system" / "skill-installer" / "scripts" / "install-skill-from-github.py"
EXPECTED_SKILLS = [
    "health-archive",
    "private-doctor",
    "health-review",
    "doctor-brief",
    "health-reminders",
    "health-storage-feishu",
]


class AcceptanceError(Exception):
    """Raised when CLI acceptance fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the health-suite CLI acceptance flow."
    )
    parser.add_argument("--repo", default="redcreen/openclaw-skills", help="GitHub repo in owner/repo format.")
    parser.add_argument("--ref", default="main", help="Git ref to install from.")
    parser.add_argument("--keep-temp", action="store_true", help="Keep the temporary acceptance workspace.")
    return parser.parse_args()


def run_json(command: list[str], *, env: dict[str, str] | None = None) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise AcceptanceError(f"Command failed: {' '.join(command)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AcceptanceError(f"Command did not return JSON: {' '.join(command)}\n{result.stdout}") from exc


def run_text(command: list[str], *, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(command, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise AcceptanceError(f"Command failed: {' '.join(command)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result.stdout


def create_dummy_sources(source_dir: Path) -> dict[str, str]:
    source_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "weight": source_dir / "weight.png",
        "blood_pressure": source_dir / "blood-pressure.png",
        "exercise": source_dir / "exercise.png",
    }
    for key, path in files.items():
        path.write_bytes(f"dummy-{key}".encode("utf-8"))
    return {key: str(path) for key, path in files.items()}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_install_mode(skills_root: Path) -> tuple[str, Path]:
    installed_dirs = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
    missing_skills = [skill for skill in EXPECTED_SKILLS if skill not in installed_dirs]
    if not missing_skills:
        return "expanded", skills_root

    umbrella_root = skills_root / "health"
    if not umbrella_root.is_dir():
        raise AcceptanceError("Missing installed skills: " + ", ".join(missing_skills))

    missing_nested = [skill for skill in EXPECTED_SKILLS if not (umbrella_root / skill).is_dir()]
    if missing_nested:
        raise AcceptanceError("Umbrella install is missing nested skills: " + ", ".join(missing_nested))
    return "umbrella", umbrella_root


def skill_script(base_root: Path, skill_name: str, script_name: str) -> str:
    return str(base_root / skill_name / "scripts" / script_name)


def main() -> int:
    args = parse_args()
    temp_root = Path(tempfile.mkdtemp(prefix="health-suite-accept-"))
    if args.keep_temp:
        print(f"Using temp root: {temp_root}", file=sys.stderr)
    try:
        codex_home = temp_root / "codex-home"
        codex_home.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ)
        env["CODEX_HOME"] = str(codex_home)

        install_output = run_text(
            [
                sys.executable,
                str(INSTALLER),
                "--repo",
                args.repo,
                "--ref",
                args.ref,
                "--path",
                "health",
            ],
            env=env,
        )

        skills_root = codex_home / "skills"
        installed_targets = sorted(path.name for path in skills_root.iterdir() if path.is_dir())
        install_mode, skill_base_root = resolve_install_mode(skills_root)

        data_root = temp_root / "personal health"
        source_dir = temp_root / "sources"
        sources = create_dummy_sources(source_dir)

        session_payload = {
            "data_root": str(data_root),
            "session_label": "acceptance-session",
            "entries": [
                {
                    "entry_type": "weight",
                    "recorded_on": "2026-04-18",
                    "recorded_at": "2026-04-18T08:00:00+08:00",
                    "fields": {"weight_kg": 84.2},
                    "sources": [{"path": sources["weight"], "role": "weight"}],
                },
                {
                    "entry_type": "exercise-walk",
                    "recorded_on": "2026-04-18",
                    "recorded_at": "2026-04-18T19:00:00+08:00",
                    "fields": {"duration_min": 42, "distance_km": 3.8, "steps": 5400},
                    "sources": [{"path": sources["exercise"], "role": "exercise"}],
                },
                {
                    "entry_type": "symptom",
                    "recorded_on": "2026-04-18",
                    "fields": {"symptom": "morning headache"},
                    "notes": ["轻度头痛，上午缓解"],
                },
                {
                    "entry_type": "medication",
                    "recorded_on": "2026-04-18",
                    "fields": {"medication_name": "Azilsartan 20mg", "medication_schedule": "nightly"},
                },
            ],
        }
        session_payload_path = temp_root / "archive-session.json"
        write_json(session_payload_path, session_payload)

        archive_session = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "health-archive", "archive_health_session.py"),
                "--payload-file",
                str(session_payload_path),
            ],
            env=env,
        )
        if archive_session.get("status") not in {"archived", "partially archived"}:
            raise AcceptanceError("Archive session did not succeed.")

        profile_payload = {
            "data_root": str(data_root),
            "facts": [
                {"label": "age", "value": 44},
                {"label": "sex", "value": "male"},
                {"label": "height_cm", "value": 178},
                {"label": "main_health_goal", "value": "control weight and blood pressure"},
                {"label": "known_conditions", "value": ["elevated blood pressure risk"]},
                {"label": "current_medications", "value": ["Azilsartan 20mg nightly"]},
                {"label": "blood_pressure_background", "value": "recent elevated readings under observation"},
                {"label": "lipid_background", "value": "lipid risk under observation"},
                {"label": "glucose_background", "value": "glucose risk not yet confirmed"},
            ],
        }
        profile_payload_path = temp_root / "profile-payload.json"
        write_json(profile_payload_path, profile_payload)

        profile_update = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "private-doctor", "update_health_profile.py"),
                "--payload-file",
                str(profile_payload_path),
            ],
            env=env,
        )

        follow_up_archive_payload = {
            "data_root": str(data_root),
            "entry_type": "blood-pressure",
            "recorded_on": "2026-04-18",
            "recorded_at": "2026-04-18T20:30:00+08:00",
            "fields": {"systolic_mmhg": 136, "diastolic_mmhg": 86, "pulse_bpm": 74},
            "sources": [{"path": sources["blood_pressure"], "role": "blood-pressure"}],
            "doctor_note": "晚间复测",
        }
        follow_up_archive_path = temp_root / "follow-up-archive.json"
        write_json(follow_up_archive_path, follow_up_archive_payload)

        archive_result = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "health-archive", "archive_health_record.py"),
                "--payload-file",
                str(follow_up_archive_path),
            ],
            env=env,
        )

        summary = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "private-doctor", "summarize_health_workspace.py"),
                "--data-root",
                str(data_root),
                "--days",
                "14",
            ],
            env=env,
        )
        summary_path = temp_root / "summary.json"
        write_json(summary_path, summary)

        assessment = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "private-doctor", "assess_health_profile.py"),
                "--summary-file",
                str(summary_path),
                "--language",
                "zh",
            ],
            env=env,
        )

        archive_result_path = temp_root / "archive-result.json"
        write_json(archive_result_path, archive_result)
        rendered_reply = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "private-doctor", "render_doctor_reply.py"),
                "--summary-file",
                str(summary_path),
                "--archive-result-file",
                str(archive_result_path),
                "--language",
                "zh",
                "--mode",
                "routine",
            ],
            env=env,
        )
        reply_path = temp_root / "reply.json"
        write_json(reply_path, rendered_reply)
        validated_reply = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "private-doctor", "validate_doctor_reply.py"),
                "--reply-file",
                str(reply_path),
            ],
            env=env,
        )

        review = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "health-review", "generate_health_review.py"),
                "--data-root",
                str(data_root),
                "--mode",
                "weekly",
                "--save",
            ],
            env=env,
        )

        brief = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "doctor-brief", "generate_doctor_brief.py"),
                "--data-root",
                str(data_root),
                "--days",
                "30",
                "--save",
            ],
            env=env,
        )

        reminder_payload = {
            "reminders": [
                {
                    "id": "morning-weight",
                    "label": "晨起体重提醒",
                    "kind": "measurement",
                    "target_entry_type": "weight",
                    "time_local": "08:00",
                    "days_of_week": [0, 1, 2, 3, 4, 5, 6],
                    "message": "请记录今天的晨起体重。",
                },
                {
                    "id": "night-review",
                    "label": "晚间复盘提醒",
                    "kind": "review",
                    "time_local": "21:00",
                    "days_of_week": [0, 1, 2, 3, 4, 5, 6],
                    "message": "请做今天的健康复盘。",
                },
            ]
        }
        reminder_payload_path = temp_root / "reminders.json"
        write_json(reminder_payload_path, reminder_payload)
        reminder_upsert = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "health-reminders", "health_reminders.py"),
                "upsert",
                "--data-root",
                str(data_root),
                "--payload-file",
                str(reminder_payload_path),
            ],
            env=env,
        )
        due_reminders = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "health-reminders", "health_reminders.py"),
                "due",
                "--data-root",
                str(data_root),
                "--at",
                "2026-04-18T21:00:00+08:00",
                "--save",
            ],
            env=env,
        )

        export_bundle = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "health-storage-feishu", "export_health_workspace_bundle.py"),
                "--data-root",
                str(data_root),
                "--format",
                "zip",
            ],
            env=env,
        )

        restore_root = temp_root / "restored-health"
        restore_bundle = run_json(
            [
                sys.executable,
                skill_script(skill_base_root, "health-storage-feishu", "import_health_workspace_bundle.py"),
                "--bundle-file",
                export_bundle["bundle_path"],
                "--data-root",
                str(restore_root),
                "--overwrite",
            ],
            env=env,
        )

        result = {
            "status": "ok",
            "repo": args.repo,
            "ref": args.ref,
            "install_mode": install_mode,
            "installed_targets": installed_targets,
            "installed_skills": EXPECTED_SKILLS,
            "suite_install_output": install_output.strip().splitlines(),
            "data_root": str(data_root.resolve()),
            "archive_session_status": archive_session["status"],
            "profile_update_status": profile_update["status"],
            "archive_result_status": archive_result["status"],
            "assessment_status": assessment["status"],
            "rendered_reply_status": rendered_reply["status"],
            "validated_reply_status": validated_reply["status"],
            "review_saved_markdown_path": review.get("saved_markdown_path"),
            "brief_saved_markdown_path": brief.get("saved_markdown_path"),
            "due_reminder_count": due_reminders.get("due_count"),
            "bundle_path": export_bundle.get("bundle_path"),
            "restored_count": restore_bundle.get("restored_count"),
            "temp_root": str(temp_root.resolve()),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        if not args.keep_temp:
            shutil.rmtree(temp_root, ignore_errors=True)
        return 0
    except AcceptanceError as exc:
        print(json.dumps({"status": "error", "error": str(exc), "temp_root": str(temp_root.resolve())}, ensure_ascii=False, indent=2, sort_keys=True))
        if not args.keep_temp:
            shutil.rmtree(temp_root, ignore_errors=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
