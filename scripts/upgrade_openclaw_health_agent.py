#!/usr/bin/env python3
"""Non-destructive upgrade for the local OpenClaw health agent."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
HEALTH_SUITE_SOURCE = REPO_ROOT / "health"
DEFAULT_WORKSPACE = Path("~/.openclaw/workspace-health").expanduser()
DEFAULT_WORKSPACE_MIRROR = Path("~/.openclaw/workspace/agents/health").expanduser()
DEFAULT_AGENT_RUNTIME = Path("~/.openclaw/agents/health").expanduser()
DEFAULT_DATA_ROOT = Path("~/Documents/personal health").expanduser()

INJECTED_FILES = [
    "AGENTS.md",
    "BOOTSTRAP.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "MEMORY.md",
    "README.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md",
]
LEGACY_ITEMS = [
    "memory",
    "backups",
    "docs",
    "scripts",
    "archive",
    "projects",
    "group-shared",
    "work",
]
SUITE_INSTALL_MAP = {
    "health": HEALTH_SUITE_SOURCE,
    "health-archive": HEALTH_SUITE_SOURCE / "health-archive",
    "private-doctor": HEALTH_SUITE_SOURCE / "private-doctor",
    "health-review": HEALTH_SUITE_SOURCE / "health-review",
    "doctor-brief": HEALTH_SUITE_SOURCE / "doctor-brief",
    "health-reminders": HEALTH_SUITE_SOURCE / "health-reminders",
    "health-storage-feishu": HEALTH_SUITE_SOURCE / "health-storage-feishu",
}


class UpgradeError(Exception):
    """Raised when the OpenClaw health-agent upgrade fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upgrade the local OpenClaw health agent to the health-suite workflow."
    )
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE), help="Path to the active workspace-health directory.")
    parser.add_argument(
        "--workspace-mirror",
        default=str(DEFAULT_WORKSPACE_MIRROR),
        help="Path to the legacy workspace mirror for health.",
    )
    parser.add_argument(
        "--agent-runtime",
        default=str(DEFAULT_AGENT_RUNTIME),
        help="Path to the health agent runtime directory containing sessions and model config.",
    )
    parser.add_argument("--data-root", default=str(DEFAULT_DATA_ROOT), help="Path to the local-first health data root.")
    parser.add_argument(
        "--backup-root",
        help="Optional explicit backup root. Defaults to <data-root>/legacy/openclaw-upgrade-backups/<timestamp>.",
    )
    parser.add_argument(
        "--health-source",
        default=str(HEALTH_SUITE_SOURCE),
        help="Source directory for the health suite to install into the workspace.",
    )
    parser.add_argument("--skip-verify", action="store_true", help="Skip the follow-up verification run.")
    return parser.parse_args()


def now_stamp() -> str:
    return dt.datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")


def run_json(command: list[str], *, cwd: Path | None = None) -> dict[str, Any]:
    result = subprocess.run(command, cwd=str(cwd) if cwd else None, capture_output=True, text=True)
    if result.returncode != 0:
        raise UpgradeError(
            f"Command failed: {' '.join(command)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise UpgradeError(f"Command did not return JSON: {' '.join(command)}\n{result.stdout}") from exc


def ensure_copy(src: Path, dest: Path) -> None:
    if not src.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def backup_sources(workspace: Path, workspace_mirror: Path, agent_runtime: Path, backup_root: Path) -> dict[str, list[str]]:
    copied: dict[str, list[str]] = {
        "workspace": [],
        "workspace_mirror": [],
        "agent_runtime": [],
    }

    workspace_backup = backup_root / "workspace-health"
    workspace_backup.mkdir(parents=True, exist_ok=True)
    for name in INJECTED_FILES + LEGACY_ITEMS:
        src = workspace / name
        if not src.exists():
            continue
        ensure_copy(src, workspace_backup / name)
        copied["workspace"].append(name)

    if workspace_mirror.exists():
        ensure_copy(workspace_mirror, backup_root / "workspace-agents-health")
        copied["workspace_mirror"].append(str(workspace_mirror))

    if agent_runtime.exists():
        ensure_copy(agent_runtime, backup_root / "agent-runtime-health")
        copied["agent_runtime"].append(str(agent_runtime))
    return copied


def clean_install_target(target: Path) -> None:
    if not target.exists():
        return
    if target.is_dir():
        shutil.rmtree(target)
    else:
        target.unlink()


def install_health_suite(health_source: Path, workspace: Path, backup_root: Path) -> list[str]:
    install_root = workspace / "skills"
    install_root.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    previous_root = backup_root / "previous-installed-skills"
    for name, source in SUITE_INSTALL_MAP.items():
        if not source.exists():
            raise UpgradeError(f"Missing health source directory: {source}")
        target = install_root / name
        if target.exists():
            ensure_copy(target, previous_root / name)
            clean_install_target(target)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
        installed.append(name)
    return installed


def upsert_marked_block(path: Path, marker: str, block_body: str) -> None:
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    block = f"{start}\n{block_body.rstrip()}\n{end}\n\n"
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    if start in current and end in current:
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n*", re.DOTALL)
        updated = pattern.sub(block, current, count=1)
    else:
        updated = block + current
    path.write_text(updated, encoding="utf-8")


def replace_markdown_section(content: str, heading: str, replacement: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\n.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(content):
        return pattern.sub(replacement.rstrip() + "\n\n", content, count=1)
    return content


def update_workspace_prompts(workspace: Path, data_root: Path) -> None:
    agents_block = f"""## Health Suite Upgrade Rules

- This workspace now runs against the local-first health suite installed under `skills/`.
- The current health source of truth is `{data_root}`.
- Prefer the installed health skills for archive, profile, review, brief, reminder, and backup tasks.
- Do not treat Feishu as the primary write path. Any older Feishu-first notes are historical only.
- On new health input: archive first, then interpret and advise.
- If the user sends a likely health image or short health fact, assume they want health help even if they do not know the right prompt.
- Do not wait for the user to say \"act like a family doctor\" or \"please record this\".
- On new archive-worthy health evidence, make the archive result explicit: record status, recorded facts, and saved location.
- After the archive result, give a brief but complete doctor interpretation plus the next practical action.
- If the profile is sparse, interpret first and then ask only the next 1-3 highest-value onboarding questions.
- Do not collapse a processed health-image reply into a one-line answer.
"""
    memory_block = f"""## 当前系统真相（Health V1 升级后）

- 当前主存储路径：`{data_root}`
- 当前健康技能安装路径：`skills/health/` 以及同级 health 子技能目录
- 如果本文件更下方仍提到“飞书主表 / 飞书主存储”，一律视为历史背景，不再代表当前写入规则
- 旧 workspace-health、旧 mirror、旧 agent 运行态都已做升级前备份，升级以 local-first 为准
"""
    readme_block = f"""## 当前运行状态

- 当前 health agent 已切换到 local-first health suite 模式
- 当前主数据目录：`{data_root}`
- 当前技能目录：`skills/`
- 旧工作区文档、脚本、会话和历史备份已做升级前快照
"""

    upsert_marked_block(workspace / "AGENTS.md", "OPENCLAW_HEALTH_SUITE_UPGRADE", agents_block)
    upsert_marked_block(workspace / "MEMORY.md", "OPENCLAW_HEALTH_SUITE_RUNTIME_TRUTH", memory_block)
    upsert_marked_block(workspace / "README.md", "OPENCLAW_HEALTH_SUITE_STATUS", readme_block)

    memory_path = workspace / "MEMORY.md"
    if memory_path.exists():
        memory_text = memory_path.read_text(encoding="utf-8")
        memory_text = replace_markdown_section(
            memory_text,
            "飞书健康表格",
            f"""## 本地健康工作区（当前主路径）

- 当前主数据目录：`{data_root}`
- 当前健康数据、档案、记录、复盘、摘要、提醒都以 local-first 工作区为准
- 旧 Feishu 健康表格只作为历史来源与可选备份背景，不再是当前主存储
- 如果需要找升级前资料，请优先查看 `legacy/openclaw-upgrade-backups/` 与旧 workspace 备份
""",
        )
        memory_text = memory_text.replace(
            "## 当前系统状态（2026-04-02）",
            "## 历史系统状态（2026-04-02，升级前）",
            1,
        )
        memory_path.write_text(memory_text, encoding="utf-8")


def parse_memory_profile(memory_path: Path) -> list[dict[str, Any]]:
    text = memory_path.read_text(encoding="utf-8")

    def match(pattern: str) -> str | None:
        found = re.search(pattern, text)
        return found.group(1).strip() if found else None

    facts: list[dict[str, Any]] = []
    mapping = {
        "user_name": match(r"- \*\*姓名\*\*: ([^\n]+)"),
        "age": match(r"- \*\*年龄\*\*: ([0-9]+)岁"),
        "height_cm": match(r"- \*\*身高\*\*: ([0-9]+)cm"),
        "recent_weight_change": match(r"- \*\*近期体重变化\*\*: ([^\n]+)"),
        "diet_change": match(r"- \*\*饮食变化\*\*: ([^\n]+)"),
        "lifestyle_change": match(r"- \*\*生活方式变化\*\*: ([^\n]+)"),
        "exercise_status": match(r"- \*\*运动现状\*\*: ([^\n]+)"),
        "medication_background": match(r"- \*\*用药背景\*\*: ([^\n]+)"),
        "confirmed_medications": match(r"- \*\*已确认药物\*\*: ([^\n]+)"),
        "antihypertensive_regimen": match(r"- \*\*降压药补充\*\*: ([^\n]+)"),
        "current_medication_habit": match(r"- \*\*当前服药习惯\*\*: ([^\n]+)"),
        "exercise_hobby": match(r"- \*\*运动爱好\*\*: ([^\n]+)"),
        "short_term_goal": match(r"- \*\*短期目标\*\*: ([^\n]+)"),
        "mid_term_goal": match(r"- \*\*中期目标\*\*: ([^\n]+)"),
        "long_term_goal": match(r"- \*\*长期目标\*\*: ([^\n]+)"),
        "ideal_goal": match(r"- \*\*理想目标\*\*: ([^\n]+)"),
        "current_judgment": match(r"- \*\*当前判断\*\*: ([^\n]+)"),
    }
    for label, value in mapping.items():
        if value is None:
            continue
        normalized: Any = int(value) if label in {"age", "height_cm"} and value.isdigit() else value
        facts.append({"label": label, "value": normalized})

    return facts


def parse_datetime_local(raw_value: str) -> tuple[str, str]:
    value = raw_value.strip()
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.datetime.now().astimezone().tzinfo)
    return parsed.date().isoformat(), parsed.isoformat()


def parse_xlsx_summary(summary_path: Path) -> list[dict[str, Any]]:
    if not summary_path.exists():
        return []
    entries: list[dict[str, Any]] = []
    current_sheet: str | None = None
    for raw_line in summary_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("===== SHEET:") and line.endswith("====="):
            current_sheet = line.replace("===== SHEET:", "").replace("=====", "").strip()
            continue
        if not line or line.startswith("rows=") or line.startswith("SHEETS:") or line.startswith("日期时间"):
            continue
        if "\t" not in line or current_sheet is None:
            continue
        parts = [part.strip() for part in line.split("\t")]
        if not re.match(r"^\d{4}-\d{2}-\d{2} ", parts[0]):
            continue
        recorded_on, recorded_at = parse_datetime_local(parts[0])
        if current_sheet == "体重记录" and len(parts) >= 4:
            notes = []
            if len(parts) >= 4 and parts[3] not in {"", "-"}:
                notes.append(parts[3])
            entries.append(
                {
                    "entry_type": "weight",
                    "recorded_on": recorded_on,
                    "recorded_at": recorded_at,
                    "fields": {"weight_kg": float(parts[1])},
                    "notes": notes,
                    "doctor_note": "legacy import from historical workbook",
                }
            )
        if current_sheet == "血压记录" and len(parts) >= 5:
            fields: dict[str, Any] = {
                "systolic_mmhg": int(parts[1]),
                "diastolic_mmhg": int(parts[2]),
            }
            if parts[3] not in {"", "-"}:
                fields["pulse_bpm"] = int(parts[3])
            notes = []
            if parts[4] not in {"", "-"}:
                notes.append(parts[4])
            entries.append(
                {
                    "entry_type": "blood-pressure",
                    "recorded_on": recorded_on,
                    "recorded_at": recorded_at,
                    "fields": fields,
                    "notes": notes,
                    "doctor_note": "legacy import from historical workbook",
                }
            )
    return entries


def parse_recent_memory(memory_dir: Path) -> list[dict[str, Any]]:
    if not memory_dir.exists():
        return []
    entries: list[dict[str, Any]] = []
    for path in sorted(memory_dir.glob("2026-04-*.md")):
        text = path.read_text(encoding="utf-8")
        file_date = path.stem

        if path.stem == "2026-04-05":
            if "2026-04-04 已记录晨测数据" in text:
                wm = re.search(r"2026-04-04 已记录晨测数据：体重 ([0-9.]+)kg，血压 ([0-9]+)/([0-9]+) mmHg，脉搏 ([0-9]+)", text)
                if wm:
                    entries.append(
                        {
                            "entry_type": "weight",
                            "recorded_on": "2026-04-04",
                            "fields": {"weight_kg": float(wm.group(1))},
                            "notes": ["legacy import from daily memory", "standard morning measurement"],
                        }
                    )
                    entries.append(
                        {
                            "entry_type": "blood-pressure",
                            "recorded_on": "2026-04-04",
                            "fields": {
                                "systolic_mmhg": int(wm.group(2)),
                                "diastolic_mmhg": int(wm.group(3)),
                                "pulse_bpm": int(wm.group(4)),
                            },
                            "notes": ["legacy import from daily memory", "standard morning measurement"],
                        }
                    )
            symptom = re.search(r"后脑勺“([^”]+)”.*?脖子发紧", text)
            if symptom:
                entries.append(
                    {
                        "entry_type": "symptom",
                        "recorded_on": "2026-04-05",
                        "fields": {"symptom": f"后脑勺{symptom.group(1)}，伴脖子发紧"},
                        "notes": ["步行约1小时后出现，血压回家后测正常", "legacy import from daily memory"],
                    }
                )
            continue

        weight_match = re.search(r"体重\s*([0-9.]+)kg", text)
        bp_match = re.search(r"血压\s*([0-9]+)\s*/\s*([0-9]+)", text)
        pulse_match = re.search(r"(?:脉搏|心率)[:：]?\s*([0-9]+)", text)
        steps_match = re.search(r"步数\s*([0-9]+)\s*步", text)
        notes = []
        if "晨测" in text:
            notes.append("standard morning measurement")
        notes.append("legacy import from daily memory")

        if weight_match:
            entries.append(
                {
                    "entry_type": "weight",
                    "recorded_on": file_date,
                    "fields": {"weight_kg": float(weight_match.group(1))},
                    "notes": notes,
                }
            )
        if bp_match:
            fields: dict[str, Any] = {
                "systolic_mmhg": int(bp_match.group(1)),
                "diastolic_mmhg": int(bp_match.group(2)),
            }
            if pulse_match:
                fields["pulse_bpm"] = int(pulse_match.group(1))
            entries.append(
                {
                    "entry_type": "blood-pressure",
                    "recorded_on": file_date,
                    "fields": fields,
                    "notes": notes,
                }
            )
        if steps_match:
            entries.append(
                {
                    "entry_type": "exercise-walk",
                    "recorded_on": file_date,
                    "fields": {"steps": int(steps_match.group(1))},
                    "notes": ["legacy import from daily memory"],
                }
            )
    return entries


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_record_entry(summary: dict[str, Any]) -> str:
    def fmt(value: Any) -> str:
        if isinstance(value, str):
            return value
        return json.dumps(value, ensure_ascii=False, sort_keys=True)

    title_time = summary.get("recorded_at") or summary["archived_at"]
    lines = [
        f"### {title_time} | {summary['entry_type']}",
        f"- Entry ID: `{summary['entry_id']}`",
        f"- Entry Key: `{summary['entry_key']}`",
        f"- Recorded On: `{summary['recorded_on']}`",
        f"- Recorded At: `{summary.get('recorded_at') or 'unspecified'}`",
        f"- Archived At: `{summary['archived_at']}`",
    ]
    if summary.get("fields"):
        lines.append("- Fields:")
        for key in sorted(summary["fields"]):
            lines.append(f"  - `{key}`: `{fmt(summary['fields'][key])}`")
    if summary.get("notes"):
        lines.append("- Notes:")
        for note in summary["notes"]:
            lines.append(f"  - {note}")
    if summary.get("doctor_note"):
        lines.append(f"- Doctor Note: {summary['doctor_note']}")
    if summary.get("raw_files"):
        lines.append("- Raw Evidence:")
        for item in summary["raw_files"]:
            lines.append(f"  - `{item['saved_path']}`")
    if summary.get("profile_updates"):
        lines.append("- Profile Updates:")
        for item in summary["profile_updates"]:
            lines.append(f"  - `{fmt(item)}`")
    return "\n".join(lines) + "\n\n"


def rebuild_records_markdown(entries: list[dict[str, Any]]) -> str:
    header = """# Health Records

This file is append-only. Each entry records what was archived and where the raw evidence was saved.
"""
    ordered = sorted(
        entries,
        key=lambda item: (
            item.get("recorded_on") or "",
            item.get("recorded_at") or item.get("archived_at") or "",
            item.get("entry_type") or "",
            item.get("entry_id") or "",
        ),
    )
    chunks = [header, "\n"]
    current_date: str | None = None
    for entry in ordered:
        entry_date = entry.get("recorded_on") or "unknown-date"
        if entry_date != current_date:
            chunks.append(f"## {entry_date}\n\n")
            current_date = entry_date
        chunks.append(render_record_entry(entry))
    return "".join(chunks)


def normalize_existing_local_data(data_root: Path) -> dict[str, Any]:
    log_path = data_root / "archive-log.jsonl"
    records_path = data_root / "records.md"
    profile_path = data_root / "profile.md"
    if not log_path.exists():
        return {"normalized": False, "entry_count": 0, "deduplicated_entries": 0}

    by_key: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    raw_count = 0
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        entry_key = payload.get("entry_key")
        if not isinstance(entry_key, str) or not entry_key:
            continue
        raw_count += 1
        payload["data_root"] = str(data_root)
        payload["profile_path"] = str(profile_path)
        payload["record_path"] = str(records_path)
        payload["log_path"] = str(log_path)
        payload["status"] = "archived"
        by_key[entry_key] = payload
        order.append(entry_key)

    if not by_key:
        return {"normalized": False, "entry_count": 0, "deduplicated_entries": 0}

    seen: set[str] = set()
    ordered_unique_keys: list[str] = []
    for entry_key in order:
        if entry_key in seen:
            continue
        seen.add(entry_key)
        ordered_unique_keys.append(entry_key)

    entries = [by_key[key] for key in ordered_unique_keys]
    log_path.write_text(
        "".join(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n" for entry in entries),
        encoding="utf-8",
    )
    records_path.write_text(rebuild_records_markdown(entries), encoding="utf-8")
    return {
        "normalized": True,
        "entry_count": len(entries),
        "deduplicated_entries": raw_count - len(entries),
    }


def migrate_health_data(workspace: Path, data_root: Path) -> dict[str, Any]:
    suite_root = workspace / "skills" / "health"
    session_script = suite_root / "health-archive" / "scripts" / "archive_health_session.py"
    profile_script = suite_root / "private-doctor" / "scripts" / "update_health_profile.py"
    if not session_script.exists() or not profile_script.exists():
        raise UpgradeError("Installed health suite is incomplete inside workspace-health/skills.")

    memory_path = workspace / "MEMORY.md"
    facts = parse_memory_profile(memory_path) if memory_path.exists() else []
    profile_payload = {"data_root": str(data_root), "facts": facts}
    profile_payload_path = data_root / "legacy" / "migration-profile-payload.json"
    write_json(profile_payload_path, profile_payload)
    profile_result = run_json([sys.executable, str(profile_script), "--payload-file", str(profile_payload_path)])

    summary_path = workspace / "backups" / "tmp_uploaded_xlsx_summary.txt"
    entries = parse_xlsx_summary(summary_path)
    entries.extend(parse_recent_memory(workspace / "memory"))
    session_payload = {
        "data_root": str(data_root),
        "session_label": "openclaw-health-upgrade",
        "entries": entries,
    }
    session_payload_path = data_root / "legacy" / "migration-archive-session.json"
    write_json(session_payload_path, session_payload)
    archive_result = run_json([sys.executable, str(session_script), "--payload-file", str(session_payload_path)])

    migration_report = {
        "profile_result": profile_result,
        "archive_result": archive_result,
        "entry_count": len(entries),
        "facts_count": len(facts),
        "sources": {
            "memory": str(memory_path),
            "xlsx_summary": str(summary_path),
            "daily_memory_dir": str(workspace / "memory"),
        },
    }
    report_path = data_root / "legacy" / "openclaw-health-upgrade-report.json"
    write_json(report_path, migration_report)
    migration_report["report_path"] = str(report_path.resolve())
    return migration_report


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    workspace_mirror = Path(args.workspace_mirror).expanduser().resolve()
    agent_runtime = Path(args.agent_runtime).expanduser().resolve()
    health_source = Path(args.health_source).expanduser().resolve()
    data_root = Path(args.data_root).expanduser().resolve()
    stamp = now_stamp()
    backup_root = (
        Path(args.backup_root).expanduser().resolve()
        if args.backup_root
        else data_root / "legacy" / "openclaw-upgrade-backups" / stamp
    )

    try:
        if not workspace.exists():
            raise UpgradeError(f"workspace-health does not exist: {workspace}")
        data_root.mkdir(parents=True, exist_ok=True)
        backup_root.mkdir(parents=True, exist_ok=True)

        backups = backup_sources(workspace, workspace_mirror, agent_runtime, backup_root)
        installed = install_health_suite(health_source, workspace, backup_root)
        update_workspace_prompts(workspace, data_root)
        normalized_data = normalize_existing_local_data(data_root)
        migration = migrate_health_data(workspace, data_root)

        result: dict[str, Any] = {
            "status": "ok",
            "workspace": str(workspace),
            "data_root": str(data_root),
            "backup_root": str(backup_root),
            "installed_skills": installed,
            "backed_up": backups,
            "normalized_data": normalized_data,
            "migration": migration,
        }

        if not args.skip_verify:
            verifier = REPO_ROOT / "scripts" / "verify_openclaw_health_agent_install.py"
            if verifier.exists():
                result["verification"] = run_json(
                    [
                        sys.executable,
                        str(verifier),
                        "--workspace",
                        str(workspace),
                        "--data-root",
                        str(data_root),
                    ]
                )
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except UpgradeError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
