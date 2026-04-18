#!/usr/bin/env python3
"""Verify the installed OpenClaw health-agent upgrade."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_WORKSPACE = Path("~/.openclaw/workspace-health").expanduser()
DEFAULT_DATA_ROOT = Path("~/Documents/personal health").expanduser()
EXPECTED_SKILLS = [
    "health",
    "health-archive",
    "private-doctor",
    "health-review",
    "doctor-brief",
    "health-reminders",
    "health-storage-feishu",
]


class VerifyError(Exception):
    """Raised when the upgraded health agent does not verify."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify the installed OpenClaw health-agent health-suite upgrade."
    )
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE), help="Path to workspace-health.")
    parser.add_argument("--data-root", default=str(DEFAULT_DATA_ROOT), help="Path to local-first health data root.")
    return parser.parse_args()


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=str(cwd) if cwd else None, capture_output=True, text=True)


def run_json(command: list[str], *, cwd: Path | None = None) -> dict[str, Any]:
    result = run(command, cwd=cwd)
    if result.returncode != 0:
        raise VerifyError(f"Command failed: {' '.join(command)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise VerifyError(f"Command did not return JSON: {' '.join(command)}\n{result.stdout}") from exc


def ensure_installed(workspace: Path) -> list[str]:
    install_root = workspace / "skills"
    found = sorted(path.name for path in install_root.iterdir() if path.is_dir()) if install_root.exists() else []
    missing = [name for name in EXPECTED_SKILLS if not (install_root / name / "SKILL.md").is_file()]
    if missing:
        raise VerifyError("Missing installed workspace skills: " + ", ".join(missing))
    return found


def ensure_skill_runtime_paths(workspace: Path) -> None:
    install_root = workspace / "skills"
    violations: list[str] = []
    for skill_name in EXPECTED_SKILLS:
        skill_root = install_root / skill_name
        if not skill_root.exists():
            continue
        markdown_files = [skill_root / "SKILL.md"]
        references = skill_root / "references"
        if references.exists():
            markdown_files.extend(sorted(references.rglob("*.md")))
        for path in markdown_files:
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            if re.search(r"python3\s+scripts/", text):
                violations.append(str(path))
    if violations:
        raise VerifyError(
            "Installed health skills still contain workspace-broken bare script paths: "
            + ", ".join(violations)
        )


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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_installed_acceptance(workspace: Path) -> dict[str, Any]:
    install_root = workspace / "skills"
    temp_root = Path(tempfile.mkdtemp(prefix="openclaw-health-install-check-"))
    try:
        data_root = temp_root / "personal health"
        sources = create_dummy_sources(temp_root / "sources")

        session_payload = {
            "data_root": str(data_root),
            "session_label": "workspace-install-check",
            "entries": [
                {
                    "entry_type": "weight",
                    "recorded_on": "2026-04-18",
                    "fields": {"weight_kg": 81.9},
                    "sources": [{"path": sources["weight"], "role": "weight"}],
                },
                {
                    "entry_type": "exercise-walk",
                    "recorded_on": "2026-04-18",
                    "fields": {"steps": 6123},
                    "sources": [{"path": sources["exercise"], "role": "exercise"}],
                },
            ],
        }
        session_path = temp_root / "session.json"
        write_json(session_path, session_payload)
        archive_session = run_json(
            [
                sys.executable,
                str(install_root / "health-archive" / "scripts" / "archive_health_session.py"),
                "--payload-file",
                str(session_path),
            ]
        )

        profile_payload = {
            "data_root": str(data_root),
            "facts": [
                {"label": "age", "value": 44},
                {"label": "height_cm", "value": 178},
                {"label": "main_health_goal", "value": "control weight and blood pressure"},
            ],
        }
        profile_path = temp_root / "profile.json"
        write_json(profile_path, profile_payload)
        profile_result = run_json(
            [
                sys.executable,
                str(install_root / "private-doctor" / "scripts" / "update_health_profile.py"),
                "--payload-file",
                str(profile_path),
            ]
        )

        bp_payload = {
            "data_root": str(data_root),
            "entry_type": "blood-pressure",
            "recorded_on": "2026-04-18",
            "fields": {"systolic_mmhg": 118, "diastolic_mmhg": 76, "pulse_bpm": 72},
            "sources": [{"path": sources["blood_pressure"], "role": "blood-pressure"}],
        }
        bp_path = temp_root / "bp.json"
        write_json(bp_path, bp_payload)
        archive_result = run_json(
            [
                sys.executable,
                str(install_root / "health-archive" / "scripts" / "archive_health_record.py"),
                "--payload-file",
                str(bp_path),
            ]
        )
        archive_result_path = temp_root / "archive-result.json"
        write_json(archive_result_path, archive_result)

        summary = run_json(
            [
                sys.executable,
                str(install_root / "private-doctor" / "scripts" / "summarize_health_workspace.py"),
                "--data-root",
                str(data_root),
                "--days",
                "14",
            ]
        )
        summary_path = temp_root / "summary.json"
        write_json(summary_path, summary)
        reply = run_json(
            [
                sys.executable,
                str(install_root / "private-doctor" / "scripts" / "render_doctor_reply.py"),
                "--summary-file",
                str(summary_path),
                "--archive-result-file",
                str(archive_result_path),
                "--language",
                "zh",
                "--mode",
                "routine",
            ]
        )
        reply_path = temp_root / "reply.json"
        write_json(reply_path, reply)
        reply_validation = run_json(
            [
                sys.executable,
                str(install_root / "private-doctor" / "scripts" / "validate_doctor_reply.py"),
                "--reply-file",
                str(reply_path),
            ]
        )
        review = run_json(
            [
                sys.executable,
                str(install_root / "health-review" / "scripts" / "generate_health_review.py"),
                "--data-root",
                str(data_root),
                "--mode",
                "weekly",
                "--save",
            ]
        )
        review_result_path = temp_root / "review.json"
        write_json(review_result_path, review)
        review_validation = run_json(
            [
                sys.executable,
                str(install_root / "health-review" / "scripts" / "validate_health_review.py"),
                "--review-file",
                str(review_result_path),
            ]
        )
        brief = run_json(
            [
                sys.executable,
                str(install_root / "doctor-brief" / "scripts" / "generate_doctor_brief.py"),
                "--data-root",
                str(data_root),
                "--days",
                "30",
                "--save",
            ]
        )
        brief_result_path = temp_root / "brief.json"
        write_json(brief_result_path, brief)
        brief_validation = run_json(
            [
                sys.executable,
                str(install_root / "doctor-brief" / "scripts" / "validate_doctor_brief.py"),
                "--brief-file",
                str(brief_result_path),
            ]
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
                }
            ]
        }
        reminder_payload_path = temp_root / "reminders.json"
        write_json(reminder_payload_path, reminder_payload)
        reminder_result = run_json(
            [
                sys.executable,
                str(install_root / "health-reminders" / "scripts" / "health_reminders.py"),
                "upsert",
                "--data-root",
                str(data_root),
                "--payload-file",
                str(reminder_payload_path),
            ]
        )
        due_result = run_json(
            [
                sys.executable,
                str(install_root / "health-reminders" / "scripts" / "health_reminders.py"),
                "due",
                "--data-root",
                str(data_root),
                "--at",
                "2026-04-18T08:00:00+08:00",
                "--save",
            ]
        )
        due_result_path = temp_root / "due.json"
        write_json(due_result_path, due_result)
        reminder_validation = run_json(
            [
                sys.executable,
                str(install_root / "health-reminders" / "scripts" / "validate_reminder_reply.py"),
                "--reply-file",
                str(due_result_path),
            ]
        )
        export_bundle = run_json(
            [
                sys.executable,
                str(install_root / "health-storage-feishu" / "scripts" / "export_health_workspace_bundle.py"),
                "--data-root",
                str(data_root),
                "--format",
                "zip",
            ]
        )
        export_result_path = temp_root / "export.json"
        write_json(export_result_path, export_bundle)
        export_validation = run_json(
            [
                sys.executable,
                str(install_root / "health-storage-feishu" / "scripts" / "validate_bundle_reply.py"),
                "--reply-file",
                str(export_result_path),
            ]
        )
        restore_root = temp_root / "restored-health"
        restore_result = run_json(
            [
                sys.executable,
                str(install_root / "health-storage-feishu" / "scripts" / "import_health_workspace_bundle.py"),
                "--bundle-file",
                export_bundle["bundle_path"],
                "--data-root",
                str(restore_root),
                "--overwrite",
            ]
        )
        restore_result_path = temp_root / "restore.json"
        write_json(restore_result_path, restore_result)
        restore_validation = run_json(
            [
                sys.executable,
                str(install_root / "health-storage-feishu" / "scripts" / "validate_bundle_reply.py"),
                "--reply-file",
                str(restore_result_path),
            ]
        )

        return {
            "status": "ok",
            "archive_session_status": archive_session["status"],
            "profile_result_status": profile_result["status"],
            "archive_result_status": archive_result["status"],
            "reply_status": reply["status"],
            "reply_validation_status": reply_validation["status"],
            "reply_markdown": reply.get("markdown"),
            "review_path": review.get("saved_markdown_path"),
            "review_validation_status": review_validation["status"],
            "brief_path": brief.get("saved_markdown_path"),
            "brief_validation_status": brief_validation["status"],
            "reminder_status": reminder_result["status"],
            "due_reminder_count": due_result["due_count"],
            "reminder_validation_status": reminder_validation["status"],
            "bundle_path": export_bundle["bundle_path"],
            "export_validation_status": export_validation["status"],
            "restored_count": restore_result["restored_count"],
            "restore_validation_status": restore_validation["status"],
        }
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    data_root = Path(args.data_root).expanduser().resolve()

    try:
        installed = ensure_installed(workspace)
        ensure_skill_runtime_paths(workspace)
        acceptance = run_installed_acceptance(workspace)
        result = {
            "status": "ok",
            "workspace": str(workspace),
            "data_root": str(data_root),
            "installed_dirs": installed,
            "acceptance": acceptance,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except VerifyError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
