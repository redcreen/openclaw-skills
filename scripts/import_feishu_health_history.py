#!/usr/bin/env python3
"""Pull full Feishu health history into the local-first health workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import mimetypes
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import requests


DEFAULT_TABLE_IDS = [
    "tblJBYKDMY8fiJ87",  # 健康记录
    "tblEycQHGabGhLCf",  # 健康记录-备份-2026-04-02
]
DEFAULT_FEISHU_ACCOUNT = "feishu5-health"
DEFAULT_DATA_ROOT = Path("~/Documents/personal health").expanduser()
DEFAULT_OPENCLAW_CONFIG = Path("~/.openclaw/openclaw.json").expanduser()
OPEN_FEISHU = "https://open.feishu.cn/open-apis"
REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SCRIPT = REPO_ROOT / "health" / "health-archive" / "scripts" / "archive_health_record.py"


class FeishuImportError(Exception):
    """Raised when the Feishu full-import flow fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pull the full Feishu health history into the local health workspace."
    )
    parser.add_argument("--app-id")
    parser.add_argument("--app-secret")
    parser.add_argument("--app-token")
    parser.add_argument("--feishu-account", default=DEFAULT_FEISHU_ACCOUNT)
    parser.add_argument("--openclaw-config", default=str(DEFAULT_OPENCLAW_CONFIG))
    parser.add_argument("--table-id", action="append", dest="table_ids")
    parser.add_argument("--data-root", default=str(DEFAULT_DATA_ROOT))
    return parser.parse_args()


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def json_dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_json(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise FeishuImportError(
            f"Command failed: {' '.join(command)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise FeishuImportError(f"Command did not return JSON: {' '.join(command)}\n{result.stdout}") from exc


def load_openclaw_account(config_path: Path, account_name: str) -> dict[str, str]:
    if not config_path.exists():
        raise FeishuImportError(f"OpenClaw config not found: {config_path}")
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise FeishuImportError(f"OpenClaw config is not valid JSON: {config_path}") from exc
    try:
        account = config["channels"]["feishu"]["accounts"][account_name]
    except KeyError as exc:
        raise FeishuImportError(f"Feishu account '{account_name}' not found in {config_path}") from exc
    app_id = account.get("appId")
    app_secret = account.get("appSecret")
    if not app_id or not app_secret:
        raise FeishuImportError(f"Feishu account '{account_name}' is missing appId/appSecret in {config_path}")
    return {"app_id": app_id, "app_secret": app_secret}


def resolve_app_config(args: argparse.Namespace) -> dict[str, str]:
    config_path = Path(args.openclaw_config).expanduser()
    resolved: dict[str, str] = {}

    if args.app_id and args.app_secret:
        resolved["app_id"] = args.app_id
        resolved["app_secret"] = args.app_secret
    else:
        resolved.update(load_openclaw_account(config_path, args.feishu_account))

    app_token = args.app_token or os.environ.get("OPENCLAW_HEALTH_FEISHU_APP_TOKEN")
    if not app_token:
        raise FeishuImportError(
            "Feishu app token is required. Pass --app-token or set OPENCLAW_HEALTH_FEISHU_APP_TOKEN."
        )
    resolved["app_token"] = app_token
    return resolved


class FeishuClient:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token: str | None = None

    def tenant_token(self) -> str:
        if self._token:
            return self._token
        response = requests.post(
            f"{OPEN_FEISHU}/auth/v3/tenant_access_token/internal",
            json={"app_id": self.app_id, "app_secret": self.app_secret},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise FeishuImportError(f"Feishu token request failed: {payload}")
        self._token = payload["tenant_access_token"]
        return self._token

    def get_json(self, url: str) -> dict[str, Any]:
        response = requests.get(url, headers={"Authorization": f"Bearer {self.tenant_token()}"}, timeout=60)
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise FeishuImportError(f"Feishu request failed for {url}: {payload}")
        return payload

    def list_tables(self, app_token: str) -> list[dict[str, Any]]:
        return self.get_json(f"{OPEN_FEISHU}/bitable/v1/apps/{app_token}/tables")["data"]["items"]

    def list_fields(self, app_token: str, table_id: str) -> list[dict[str, Any]]:
        return self.get_json(f"{OPEN_FEISHU}/bitable/v1/apps/{app_token}/tables/{table_id}/fields")["data"]["items"]

    def list_records(self, app_token: str, table_id: str) -> list[dict[str, Any]]:
        page_token: str | None = None
        records: list[dict[str, Any]] = []
        while True:
            url = f"{OPEN_FEISHU}/bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size=200"
            if page_token:
                url += f"&page_token={page_token}"
            payload = self.get_json(url)["data"]
            records.extend(payload["items"])
            if not payload.get("has_more"):
                break
            page_token = payload["page_token"]
        return records

    def download(self, url: str) -> requests.Response:
        response = requests.get(url, headers={"Authorization": f"Bearer {self.tenant_token()}"}, timeout=120)
        response.raise_for_status()
        return response


def parse_feishu_datetime(raw_value: Any) -> tuple[str, str | None]:
    if raw_value in (None, "", []):
        raise FeishuImportError("record date is missing")
    if isinstance(raw_value, str) and raw_value.isdigit():
        raw_value = int(raw_value)
    if isinstance(raw_value, (int, float)):
        moment = dt.datetime.fromtimestamp(raw_value / 1000, now().tzinfo)
        return moment.date().isoformat(), moment.isoformat()
    raise FeishuImportError(f"Unsupported Feishu date value: {raw_value!r}")


def parse_number(raw_value: Any) -> float | None:
    if raw_value in (None, "", []):
        return None
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        return None


def parse_pulse(note: str | None) -> int | None:
    if not note:
        return None
    match = re.search(r"(?:心率|脉搏)[:：]?\s*([0-9]+)", note)
    return int(match.group(1)) if match else None


def core_key(entry: dict[str, Any]) -> tuple[Any, ...] | None:
    entry_type = entry["entry_type"]
    recorded_on = entry["recorded_on"]
    fields = entry["fields"]
    if entry_type == "weight":
        weight = fields.get("weight_kg")
        if weight in (None, "", []):
            return None
        return ("weight", recorded_on, round(float(weight), 2))
    if entry_type == "blood-pressure":
        systolic = fields.get("systolic_mmhg")
        diastolic = fields.get("diastolic_mmhg")
        if systolic in (None, "", []) or diastolic in (None, "", []):
            return None
        return (
            "blood-pressure",
            recorded_on,
            int(systolic),
            int(diastolic),
            fields.get("pulse_bpm"),
        )
    return None


def attachment_count(entry: dict[str, Any]) -> int:
    return len(entry.get("attachments", []))


def note_length(entry: dict[str, Any]) -> int:
    return sum(len(item) for item in entry.get("notes", []))


def richer_entry(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    left_score = (attachment_count(left), len(left["fields"]), note_length(left), 1 if left["source_table_name"] == "健康记录" else 0)
    right_score = (attachment_count(right), len(right["fields"]), note_length(right), 1 if right["source_table_name"] == "健康记录" else 0)
    return left if left_score >= right_score else right


def derive_entries(table_name: str, record: dict[str, Any]) -> list[dict[str, Any]]:
    fields = record["fields"]
    recorded_on, recorded_at = parse_feishu_datetime(fields.get("记录日期"))
    note = str(fields.get("备注") or "").strip()
    room_temp = parse_number(fields.get("环境温度"))
    extras: dict[str, Any] = {}
    extra_map = {
        "早餐热量": "breakfast_kcal",
        "午餐热量": "lunch_kcal",
        "晚餐热量": "dinner_kcal",
        "加餐热量": "snack_kcal",
        "总摄入热量": "total_intake_kcal",
    }
    for source_name, target_name in extra_map.items():
        value = parse_number(fields.get(source_name))
        if value is not None:
            extras[target_name] = value

    entries: list[dict[str, Any]] = []
    weight = parse_number(fields.get("体重"))
    if weight is not None:
        payload_fields = {"weight_kg": round(weight, 4), **extras}
        if room_temp is not None:
            payload_fields["room_temp_c"] = round(room_temp, 4)
        entries.append(
            {
                "source_table_name": table_name,
                "source_record_id": record["record_id"],
                "entry_type": "weight",
                "recorded_on": recorded_on,
                "recorded_at": recorded_at,
                "fields": payload_fields,
                "notes": [note] if note else [],
                "attachments": list(fields.get("体重照片") or []),
            }
        )

    systolic = parse_number(fields.get("收缩压"))
    diastolic = parse_number(fields.get("舒张压"))
    if systolic is not None and diastolic is not None:
        payload_fields = {
            "systolic_mmhg": int(round(systolic)),
            "diastolic_mmhg": int(round(diastolic)),
        }
        pulse = parse_pulse(note)
        if pulse is not None:
            payload_fields["pulse_bpm"] = pulse
        if room_temp is not None:
            payload_fields["room_temp_c"] = round(room_temp, 4)
        entries.append(
            {
                "source_table_name": table_name,
                "source_record_id": record["record_id"],
                "entry_type": "blood-pressure",
                "recorded_on": recorded_on,
                "recorded_at": recorded_at,
                "fields": payload_fields,
                "notes": [note] if note else [],
                "attachments": list(fields.get("血压照片") or []),
            }
        )

    return entries


def merge_feishu_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[tuple[Any, ...], dict[str, Any]] = {}
    for entry in entries:
        key = core_key(entry)
        if key is None:
            continue
        if key in merged:
            keep = richer_entry(merged[key], entry)
            if keep is merged[key]:
                existing_tokens = {item["file_token"] for item in merged[key].get("attachments", [])}
                for item in entry.get("attachments", []):
                    if item["file_token"] not in existing_tokens:
                        merged[key]["attachments"].append(item)
                continue
            existing_tokens = {item["file_token"] for item in keep.get("attachments", [])}
            other = merged[key] if keep is entry else entry
            for item in other.get("attachments", []):
                if item["file_token"] not in existing_tokens:
                    keep["attachments"].append(item)
            merged[key] = keep
            continue
        merged[key] = {
            **entry,
            "attachments": list(entry.get("attachments", [])),
        }
    return list(merged.values())


def load_local_entries(log_path: Path) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            entries.append(payload)
    return entries


def render_record_entry(summary: dict[str, Any]) -> str:
    def fmt(value: Any) -> str:
        return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)

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


def save_attachment_for_entry(
    data_root: Path,
    entry: dict[str, Any],
    attachment: dict[str, Any],
    client: FeishuClient,
) -> dict[str, Any]:
    recorded_on = dt.date.fromisoformat(entry["recorded_on"])
    raw_dir = data_root / "raw" / recorded_on.strftime("%Y") / recorded_on.strftime("%m") / recorded_on.strftime("%d")
    raw_dir.mkdir(parents=True, exist_ok=True)

    role = "weight" if entry["entry_type"] == "weight" else "blood-pressure"
    recorded_at = entry.get("recorded_at")
    if recorded_at:
        stamp = dt.datetime.fromisoformat(recorded_at).strftime("%Y%m%dT%H%M%S%z")
    else:
        stamp = now().strftime("%Y%m%dT%H%M%S%z")
    original_name = attachment["name"]
    suffix = Path(original_name).suffix or mimetypes.guess_extension(attachment.get("type") or "") or ".bin"
    target = raw_dir / f"{stamp}_{role}{suffix}"
    counter = 2
    while target.exists():
        target = raw_dir / f"{stamp}_{role}_{counter:02d}{suffix}"
        counter += 1

    response = client.download(attachment["url"])
    target.write_bytes(response.content)
    digest = hashlib.sha256(response.content).hexdigest()
    saved_path = target.relative_to(data_root).as_posix()
    meta_path = Path(f"{target}.meta.json")
    meta = {
        "entry_id": entry["entry_id"],
        "archived_at": now().isoformat(),
        "original_name": original_name,
        "original_url": attachment["url"],
        "source": "feishu",
        "file_token": attachment["file_token"],
        "role": role,
        "media_type": attachment.get("type") or response.headers.get("content-type") or "application/octet-stream",
        "size_bytes": len(response.content),
        "sha256": digest,
        "saved_path": saved_path,
    }
    json_dump(meta_path, meta)
    return {
        "role": role,
        "saved_path": saved_path,
        "meta_path": meta_path.relative_to(data_root).as_posix(),
        "sha256": digest,
        "size_bytes": len(response.content),
    }


def merge_into_existing(local_entry: dict[str, Any], feishu_entry: dict[str, Any], data_root: Path, client: FeishuClient) -> dict[str, Any]:
    updated = json.loads(json.dumps(local_entry, ensure_ascii=False))
    updated.setdefault("fields", {})
    for key, value in feishu_entry["fields"].items():
        if key not in updated["fields"] or updated["fields"][key] in (None, "", []):
            updated["fields"][key] = value
    updated.setdefault("notes", [])
    for note in feishu_entry.get("notes", []):
        if note and note not in updated["notes"]:
            updated["notes"].append(note)
    updated.setdefault("raw_files", [])
    existing_roles = {item["role"] for item in updated["raw_files"]}
    for attachment in feishu_entry.get("attachments", []):
        role = "weight" if feishu_entry["entry_type"] == "weight" else "blood-pressure"
        if role in existing_roles:
            continue
        saved = save_attachment_for_entry(data_root, updated, attachment, client)
        updated["raw_files"].append(saved)
        existing_roles.add(role)
    updated["data_root"] = str(data_root)
    updated["record_path"] = str(data_root / "records.md")
    updated["profile_path"] = str(data_root / "profile.md")
    updated["log_path"] = str(data_root / "archive-log.jsonl")
    return updated


def archive_new_entry(data_root: Path, entry: dict[str, Any], temp_root: Path, client: FeishuClient) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "data_root": str(data_root),
        "entry_type": entry["entry_type"],
        "recorded_on": entry["recorded_on"],
        "recorded_at": entry.get("recorded_at"),
        "fields": entry["fields"],
        "notes": entry.get("notes", []),
        "doctor_note": f"feishu import from {entry['source_table_name']} record {entry['source_record_id']}",
    }
    sources = []
    for attachment in entry.get("attachments", []):
        role = "weight" if entry["entry_type"] == "weight" else "blood-pressure"
        filename = f"{entry['source_record_id']}_{attachment['name']}"
        path = temp_root / filename
        path.write_bytes(client.download(attachment["url"]).content)
        sources.append({"path": str(path), "role": role})
    if sources:
        payload["sources"] = sources
    payload_path = temp_root / f"{entry['source_record_id']}_{entry['entry_type']}.json"
    json_dump(payload_path, payload)
    return run_json([sys.executable, str(ARCHIVE_SCRIPT), "--payload-file", str(payload_path)])


def main() -> int:
    args = parse_args()
    app_config = resolve_app_config(args)
    data_root = Path(args.data_root).expanduser().resolve()
    table_ids = args.table_ids or DEFAULT_TABLE_IDS
    stamp = now().strftime("%Y%m%dT%H%M%S%z")
    export_root = data_root / "legacy" / "feishu-full-pull" / stamp
    export_root.mkdir(parents=True, exist_ok=True)
    temp_root = export_root / "temp"
    temp_root.mkdir(parents=True, exist_ok=True)

    try:
        client = FeishuClient(app_config["app_id"], app_config["app_secret"])
        tables = client.list_tables(app_config["app_token"])
        table_name_map = {item["table_id"]: item["name"] for item in tables}
        json_dump(export_root / "tables.json", tables)

        all_candidates: list[dict[str, Any]] = []
        table_summaries: list[dict[str, Any]] = []
        for table_id in table_ids:
            table_name = table_name_map.get(table_id, table_id)
            fields = client.list_fields(app_config["app_token"], table_id)
            records = client.list_records(app_config["app_token"], table_id)
            json_dump(export_root / f"{table_name}_{table_id}_fields.json", fields)
            json_dump(export_root / f"{table_name}_{table_id}_records.json", records)
            table_summaries.append({"table_id": table_id, "table_name": table_name, "record_count": len(records), "field_count": len(fields)})
            for record in records:
                all_candidates.extend(derive_entries(table_name, record))

        merged_candidates = merge_feishu_entries(all_candidates)
        local_entries = load_local_entries(data_root / "archive-log.jsonl")
        local_index = {}
        for entry in local_entries:
            key = core_key(entry)
            if key is None:
                continue
            local_index[key] = entry

        updated_local_entries = list(local_entries)
        updated_count = 0
        imported_count = 0
        deduplicated_count = 0
        attachments_saved = 0
        new_entries: list[dict[str, Any]] = []

        for candidate in merged_candidates:
            key = core_key(candidate)
            if key is None:
                continue
            existing = local_index.get(key)
            if existing is not None:
                updated = merge_into_existing(existing, candidate, data_root, client)
                if json.dumps(updated, ensure_ascii=False, sort_keys=True) != json.dumps(existing, ensure_ascii=False, sort_keys=True):
                    idx = updated_local_entries.index(existing)
                    updated_local_entries[idx] = updated
                    local_index[key] = updated
                    updated_count += 1
                    attachments_saved += len(updated.get("raw_files", [])) - len(existing.get("raw_files", []))
                continue

            archived = archive_new_entry(data_root, candidate, temp_root, client)
            if archived.get("deduplicated"):
                deduplicated_count += 1
            else:
                imported_count += 1
            attachments_saved += len(archived.get("raw_files", []))
            updated_local_entries.append(archived)
            local_index[key] = archived
            new_entries.append(archived)

        if updated_count:
            log_path = data_root / "archive-log.jsonl"
            records_path = data_root / "records.md"
            log_path.write_text(
                "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in updated_local_entries),
                encoding="utf-8",
            )
            records_path.write_text(rebuild_records_markdown(updated_local_entries), encoding="utf-8")

        report = {
            "status": "ok",
            "data_root": str(data_root),
            "export_root": str(export_root),
            "table_summaries": table_summaries,
            "feishu_candidates_total": len(all_candidates),
            "feishu_candidates_merged": len(merged_candidates),
            "local_entries_before": len(local_entries),
            "local_entries_after": len(updated_local_entries),
            "updated_existing_entries": updated_count,
            "imported_new_entries": imported_count,
            "archive_deduplicated_new_entries": deduplicated_count,
            "attachments_saved": attachments_saved,
            "new_entry_ids": [item["entry_id"] for item in new_entries],
        }
        json_dump(export_root / "import-report.json", report)
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except FeishuImportError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
