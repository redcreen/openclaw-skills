#!/usr/bin/env python3
"""Verify the installed OpenClaw health-agent upgrade."""

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
                "--language",
                "zh",
                "--mode",
                "routine",
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

        return {
            "status": "ok",
            "archive_session_status": archive_session["status"],
            "profile_result_status": profile_result["status"],
            "archive_result_status": archive_result["status"],
            "reply_status": reply["status"],
            "review_path": review.get("saved_markdown_path"),
            "brief_path": brief.get("saved_markdown_path"),
            "reminder_status": reminder_result["status"],
            "bundle_path": export_bundle["bundle_path"],
            "restored_count": restore_result["restored_count"],
        }
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    data_root = Path(args.data_root).expanduser().resolve()

    try:
        installed = ensure_installed(workspace)
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
