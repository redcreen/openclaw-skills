#!/usr/bin/env python3
"""Archive health evidence into a local-first health workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import mimetypes
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any


DEFAULT_DATA_ROOT = Path("~/document/personal health").expanduser()
SUPPORTED_ENTRY_TYPES = {
    "weight",
    "blood-pressure",
    "exercise-walk",
    "exercise-run",
    "exercise-swim",
    "sleep",
    "symptom",
    "medication",
    "unknown-health",
}
RECORDS_HEADER = """# Health Records

This file is append-only. Each entry records what was archived and where the raw evidence was saved.
"""
PROFILE_HEADER = """# Health Profile

## Facts
"""


class ArchiveError(Exception):
    """Raised when payload validation or archiving fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive a normalized health payload into a local health workspace."
    )
    parser.add_argument(
        "--payload-file",
        help="Path to a JSON payload file.",
    )
    parser.add_argument(
        "--payload-json",
        help="Inline JSON payload.",
    )
    parser.add_argument(
        "--data-root",
        help="Override the payload data_root and default external health workspace.",
    )
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.payload_file and not args.payload_json:
        raise ArchiveError("One of --payload-file or --payload-json is required.")
    if args.payload_file and args.payload_json:
        raise ArchiveError("Use either --payload-file or --payload-json, not both.")

    if args.payload_file:
        payload_text = Path(args.payload_file).read_text(encoding="utf-8")
    else:
        payload_text = args.payload_json

    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        raise ArchiveError(f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise ArchiveError("Payload must be a JSON object.")
    return payload


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    normalized = normalized.strip("-")
    return normalized or "unknown"


def ensure_json_serializable(value: Any, field_name: str) -> Any:
    try:
        json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError as exc:
        raise ArchiveError(f"{field_name} must be JSON-serializable.") from exc
    return value


def parse_recorded_on(raw_value: Any) -> dt.date:
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise ArchiveError("recorded_on is required and must be an ISO date string.")
    try:
        return dt.date.fromisoformat(raw_value.strip())
    except ValueError as exc:
        raise ArchiveError("recorded_on must use YYYY-MM-DD.") from exc


def parse_datetime(raw_value: Any, local_tz: dt.tzinfo) -> dt.datetime | None:
    if raw_value in (None, ""):
        return None
    if not isinstance(raw_value, str):
        raise ArchiveError("recorded_at must be an ISO datetime string.")
    candidate = raw_value.strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ArchiveError("recorded_at must be an ISO datetime string.") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=local_tz)
    return parsed


def format_json_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def normalize_notes(raw_value: Any) -> list[str]:
    if raw_value in (None, "", []):
        return []
    if isinstance(raw_value, str):
        note = raw_value.strip()
        return [note] if note else []
    if not isinstance(raw_value, list):
        raise ArchiveError("notes must be a string or a list.")
    normalized = []
    for item in raw_value:
        if item in (None, ""):
            continue
        normalized.append(str(item).strip())
    return [item for item in normalized if item]


def normalize_profile_updates(raw_value: Any) -> list[dict[str, Any]]:
    if raw_value in (None, "", []):
        return []
    if isinstance(raw_value, str):
        raw_value = [{"text": raw_value}]
    if not isinstance(raw_value, list):
        raise ArchiveError("profile_updates must be a string or a list.")

    normalized: list[dict[str, Any]] = []
    for item in raw_value:
        if isinstance(item, str):
            text = item.strip()
            if text:
                normalized.append({"text": text})
            continue
        if not isinstance(item, dict):
            raise ArchiveError("Each profile_updates item must be a string or an object.")
        cleaned = {}
        for key, value in item.items():
            if not isinstance(key, str) or not key.strip():
                raise ArchiveError("profile_updates keys must be non-empty strings.")
            cleaned[key.strip()] = ensure_json_serializable(value, "profile_updates item")
        if cleaned:
            normalized.append(cleaned)
    return normalized


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_sources(payload: dict[str, Any], entry_type: str) -> list[dict[str, Any]]:
    raw_sources = payload.get("sources")
    if raw_sources is None and payload.get("source_paths") is not None:
        raw_sources = [{"path": item, "role": entry_type} for item in payload["source_paths"]]
    if raw_sources in (None, []):
        return []
    if not isinstance(raw_sources, list):
        raise ArchiveError("sources must be a list.")

    normalized: list[dict[str, Any]] = []
    for item in raw_sources:
        if isinstance(item, str):
            item = {"path": item}
        if not isinstance(item, dict):
            raise ArchiveError("Each source must be a string path or an object.")
        raw_path = item.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ArchiveError("Each source must include a non-empty path.")
        path = Path(raw_path).expanduser()
        if not path.is_file():
            raise ArchiveError(f"Source file does not exist: {path}")
        role = slugify(str(item.get("role") or entry_type))
        media_type = item.get("media_type")
        if media_type is None:
            media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        source = {
            "path": path.resolve(),
            "role": role,
            "media_type": str(media_type),
            "original_name": path.name,
            "size_bytes": path.stat().st_size,
            "sha256": file_sha256(path),
        }
        caption = item.get("caption")
        if caption:
            source["caption"] = str(caption)
        normalized.append(source)
    return normalized


def normalize_fields(raw_fields: Any) -> dict[str, Any]:
    if raw_fields is None:
        return {}
    if not isinstance(raw_fields, dict):
        raise ArchiveError("fields must be an object.")
    normalized = {}
    for key, value in raw_fields.items():
        if not isinstance(key, str) or not key.strip():
            raise ArchiveError("fields keys must be non-empty strings.")
        normalized[key.strip()] = ensure_json_serializable(value, f"field {key!r}")
    return normalized


def choose_data_root(payload: dict[str, Any], arg_root: str | None) -> Path:
    if arg_root:
        return Path(arg_root).expanduser()
    payload_root = payload.get("data_root")
    if isinstance(payload_root, str) and payload_root.strip():
        return Path(payload_root).expanduser()
    env_root = os.environ.get("HEALTH_DATA_ROOT") or os.environ.get("HEALTH_ARCHIVE_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return DEFAULT_DATA_ROOT


def ensure_workspace(data_root: Path) -> dict[str, Path]:
    data_root.mkdir(parents=True, exist_ok=True)
    raw_root = data_root / "raw"
    raw_root.mkdir(exist_ok=True)

    profile_path = data_root / "profile.md"
    if not profile_path.exists():
        profile_path.write_text(PROFILE_HEADER, encoding="utf-8")

    records_path = data_root / "records.md"
    if not records_path.exists():
        records_path.write_text(RECORDS_HEADER, encoding="utf-8")

    log_path = data_root / "archive-log.jsonl"
    if not log_path.exists():
        log_path.touch()

    return {
        "data_root": data_root.resolve(),
        "raw_root": raw_root.resolve(),
        "profile_path": profile_path.resolve(),
        "records_path": records_path.resolve(),
        "log_path": log_path.resolve(),
    }


def canonicalize_source(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "role": source["role"],
        "sha256": source["sha256"],
        "size_bytes": source["size_bytes"],
    }


def build_entry_key(
    entry_type: str,
    recorded_on: dt.date,
    recorded_at: dt.datetime | None,
    fields: dict[str, Any],
    notes: list[str],
    sources: list[dict[str, Any]],
    profile_updates: list[dict[str, Any]],
) -> str:
    canonical = {
        "entry_type": entry_type,
        "recorded_on": recorded_on.isoformat(),
        "recorded_at": recorded_at.isoformat() if recorded_at else None,
        "fields": fields,
        "notes": notes,
        "sources": [canonicalize_source(item) for item in sources],
        "profile_updates": profile_updates,
    }
    payload = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def existing_entry_is_usable(summary: dict[str, Any], data_root: Path) -> bool:
    record_path = Path(summary["record_path"])
    if not record_path.is_file():
        return False
    for item in summary.get("raw_files", []):
        raw_path = data_root / item["saved_path"]
        if not raw_path.is_file():
            return False
    return True


def find_existing_entry(log_path: Path, entry_key: str, data_root: Path) -> dict[str, Any] | None:
    if not log_path.exists():
        return None
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if payload.get("entry_key") != entry_key:
                continue
            if existing_entry_is_usable(payload, data_root):
                return payload
    return None


def pick_extension(source: dict[str, Any]) -> str:
    suffix = source["path"].suffix.lower()
    if suffix:
        return suffix
    guessed = mimetypes.guess_extension(source["media_type"])
    return guessed or ".bin"


def timestamp_label(value: dt.datetime) -> str:
    label = value.strftime("%Y%m%dT%H%M%S%z")
    return label or value.strftime("%Y%m%dT%H%M%S")


def make_unique_destination(directory: Path, stem: str, suffix: str) -> Path:
    candidate = directory / f"{stem}{suffix}"
    counter = 2
    while candidate.exists():
        candidate = directory / f"{stem}_{counter:02d}{suffix}"
        counter += 1
    return candidate


def copy_sources(
    sources: list[dict[str, Any]],
    data_root: Path,
    recorded_on: dt.date,
    filename_time: dt.datetime,
    archived_at: dt.datetime,
    entry_id: str,
) -> list[dict[str, Any]]:
    raw_day_dir = data_root / "raw" / recorded_on.strftime("%Y") / recorded_on.strftime("%m") / recorded_on.strftime("%d")
    raw_day_dir.mkdir(parents=True, exist_ok=True)

    saved_items: list[dict[str, Any]] = []
    for source in sources:
        suffix = pick_extension(source)
        stem = f"{timestamp_label(filename_time)}_{source['role']}"
        destination = make_unique_destination(raw_day_dir, stem, suffix)
        shutil.copy2(source["path"], destination)
        meta_path = Path(f"{destination}.meta.json")
        saved_path = destination.relative_to(data_root).as_posix()
        meta = {
            "entry_id": entry_id,
            "archived_at": archived_at.isoformat(),
            "original_path": str(source["path"]),
            "original_name": source["original_name"],
            "role": source["role"],
            "media_type": source["media_type"],
            "size_bytes": source["size_bytes"],
            "sha256": source["sha256"],
            "saved_path": saved_path,
        }
        if source.get("caption"):
            meta["caption"] = source["caption"]
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        saved_items.append(
            {
                "role": source["role"],
                "saved_path": saved_path,
                "meta_path": meta_path.relative_to(data_root).as_posix(),
                "sha256": source["sha256"],
                "size_bytes": source["size_bytes"],
            }
        )
    return saved_items


def last_date_heading(content: str) -> str | None:
    for line in reversed(content.splitlines()):
        if line.startswith("## "):
            return line[3:].strip()
    return None


def render_record_entry(summary: dict[str, Any]) -> str:
    title_time = summary.get("recorded_at") or summary["archived_at"]
    lines = [
        f"### {title_time} | {summary['entry_type']}",
        f"- Entry ID: `{summary['entry_id']}`",
        f"- Entry Key: `{summary['entry_key']}`",
        f"- Recorded On: `{summary['recorded_on']}`",
        f"- Recorded At: `{summary.get('recorded_at') or 'unspecified'}`",
        f"- Archived At: `{summary['archived_at']}`",
    ]
    if summary["fields"]:
        lines.append("- Fields:")
        for key in sorted(summary["fields"]):
            lines.append(f"  - `{key}`: `{format_json_value(summary['fields'][key])}`")
    if summary["notes"]:
        lines.append("- Notes:")
        for note in summary["notes"]:
            lines.append(f"  - {note}")
    if summary.get("doctor_note"):
        lines.append(f"- Doctor Note: {summary['doctor_note']}")
    if summary["raw_files"]:
        lines.append("- Raw Evidence:")
        for item in summary["raw_files"]:
            lines.append(f"  - `{item['saved_path']}`")
    if summary["profile_updates"]:
        lines.append("- Profile Updates:")
        for item in summary["profile_updates"]:
            lines.append(f"  - `{format_json_value(item)}`")
    return "\n".join(lines) + "\n\n"


def append_record(records_path: Path, summary: dict[str, Any]) -> None:
    if records_path.exists():
        content = records_path.read_text(encoding="utf-8")
    else:
        content = RECORDS_HEADER
        records_path.write_text(content, encoding="utf-8")

    with records_path.open("a", encoding="utf-8") as handle:
        if content and not content.endswith("\n"):
            handle.write("\n")
        if last_date_heading(content) != summary["recorded_on"]:
            if content and not content.endswith("\n\n"):
                handle.write("\n")
            handle.write(f"## {summary['recorded_on']}\n\n")
        elif content and not content.endswith("\n\n"):
            handle.write("\n")
        handle.write(render_record_entry(summary))


def render_profile_update_line(item: dict[str, Any], archived_at: str) -> str:
    if "text" in item and len(item) == 1:
        return f"- {archived_at} | {item['text']}"
    formatted = ", ".join(
        f"{key}={format_json_value(value)}" for key, value in sorted(item.items())
    )
    return f"- {archived_at} | {formatted}"


def append_profile_updates(profile_path: Path, profile_updates: list[dict[str, Any]], archived_at: str) -> None:
    if not profile_updates:
        return
    if profile_path.exists():
        content = profile_path.read_text(encoding="utf-8")
    else:
        content = PROFILE_HEADER
        profile_path.write_text(content, encoding="utf-8")

    with profile_path.open("a", encoding="utf-8") as handle:
        if content and not content.endswith("\n"):
            handle.write("\n")
        if not content.endswith("\n\n"):
            handle.write("\n")
        for item in profile_updates:
            handle.write(render_profile_update_line(item, archived_at) + "\n")


def append_log(log_path: Path, summary: dict[str, Any]) -> None:
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(summary, ensure_ascii=False, sort_keys=True) + "\n")


def build_summary(
    *,
    entry_id: str,
    entry_key: str,
    entry_type: str,
    recorded_on: dt.date,
    recorded_at: dt.datetime | None,
    archived_at: dt.datetime,
    fields: dict[str, Any],
    notes: list[str],
    doctor_note: str | None,
    raw_files: list[dict[str, Any]],
    profile_updates: list[dict[str, Any]],
    workspace_paths: dict[str, Path],
    deduplicated: bool,
) -> dict[str, Any]:
    return {
        "status": "archived",
        "deduplicated": deduplicated,
        "entry_id": entry_id,
        "entry_key": entry_key,
        "entry_type": entry_type,
        "recorded_on": recorded_on.isoformat(),
        "recorded_at": recorded_at.isoformat() if recorded_at else None,
        "archived_at": archived_at.isoformat(),
        "fields": fields,
        "notes": notes,
        "doctor_note": doctor_note,
        "raw_files": raw_files,
        "profile_updates": profile_updates,
        "data_root": str(workspace_paths["data_root"]),
        "record_path": str(workspace_paths["records_path"]),
        "profile_path": str(workspace_paths["profile_path"]),
        "log_path": str(workspace_paths["log_path"]),
    }


def archive(payload: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    local_tz = dt.datetime.now().astimezone().tzinfo or dt.timezone.utc
    entry_type = slugify(
        str(
            payload.get("entry_type")
            or payload.get("evidence_type")
            or payload.get("record_type")
            or ""
        )
    )
    if entry_type not in SUPPORTED_ENTRY_TYPES:
        raise ArchiveError(
            "entry_type is required and must be one of: "
            + ", ".join(sorted(SUPPORTED_ENTRY_TYPES))
        )

    data_root = choose_data_root(payload, args.data_root)
    workspace_paths = ensure_workspace(data_root)

    recorded_on = parse_recorded_on(payload.get("recorded_on") or payload.get("date"))
    recorded_at = parse_datetime(payload.get("recorded_at") or payload.get("measured_at"), local_tz)
    archived_at = dt.datetime.now().astimezone()
    filename_time = recorded_at or archived_at

    fields = normalize_fields(payload.get("fields"))
    notes = normalize_notes(payload.get("notes") or payload.get("note"))
    doctor_note = payload.get("doctor_note")
    if doctor_note is not None:
        doctor_note = str(doctor_note).strip() or None
    profile_updates = normalize_profile_updates(payload.get("profile_updates"))
    sources = normalize_sources(payload, entry_type)

    entry_key = build_entry_key(
        entry_type,
        recorded_on,
        recorded_at,
        fields,
        notes,
        sources,
        profile_updates,
    )
    existing = find_existing_entry(workspace_paths["log_path"], entry_key, workspace_paths["data_root"])
    if existing is not None:
        existing["deduplicated"] = True
        return existing

    entry_id = f"{recorded_on.isoformat()}-{entry_type}-{entry_key[:8]}"
    raw_files = copy_sources(
        sources,
        workspace_paths["data_root"],
        recorded_on,
        filename_time,
        archived_at,
        entry_id,
    )

    summary = build_summary(
        entry_id=entry_id,
        entry_key=entry_key,
        entry_type=entry_type,
        recorded_on=recorded_on,
        recorded_at=recorded_at,
        archived_at=archived_at,
        fields=fields,
        notes=notes,
        doctor_note=doctor_note,
        raw_files=raw_files,
        profile_updates=profile_updates,
        workspace_paths=workspace_paths,
        deduplicated=False,
    )
    append_record(workspace_paths["records_path"], summary)
    append_profile_updates(workspace_paths["profile_path"], profile_updates, archived_at.isoformat())
    append_log(workspace_paths["log_path"], summary)
    return summary


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args)
        result = archive(payload, args)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ArchiveError as exc:
        error = {
            "status": "not archived",
            "error": str(exc),
        }
        print(json.dumps(error, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
