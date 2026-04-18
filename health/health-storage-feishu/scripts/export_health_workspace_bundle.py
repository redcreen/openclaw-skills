#!/usr/bin/env python3
"""Export the local health workspace into a portable bundle."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import zipfile
from pathlib import Path


DEFAULT_DATA_ROOT = Path("~/Documents/personal health").expanduser()


class ExportError(Exception):
    """Raised when the health workspace cannot be exported."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the local health workspace into a portable bundle."
    )
    parser.add_argument("--data-root", help="Override the external health data root.")
    parser.add_argument(
        "--format",
        choices=("json", "zip"),
        default="zip",
        help="Bundle format.",
    )
    return parser.parse_args()


def choose_data_root(arg_root: str | None) -> Path:
    if arg_root:
        return Path(arg_root).expanduser()
    env_root = os.environ.get("HEALTH_DATA_ROOT") or os.environ.get("HEALTH_ARCHIVE_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return DEFAULT_DATA_ROOT


def bundle_dir(data_root: Path) -> Path:
    path = data_root / "exports"
    path.mkdir(parents=True, exist_ok=True)
    return path


def tracked_files(data_root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in sorted(data_root.rglob("*")):
        if not path.is_file():
            continue
        if "exports" in path.parts:
            continue
        paths.append(path)
    return paths


def export_payload(data_root: Path) -> dict:
    files = tracked_files(data_root)
    return {
        "status": "ok",
        "exported_at": dt.datetime.now().astimezone().isoformat(),
        "data_root": str(data_root.resolve()),
        "file_count": len(files),
        "files": [path.relative_to(data_root).as_posix() for path in files],
    }


def write_json_bundle(data_root: Path, payload: dict) -> str:
    now = dt.datetime.now().astimezone()
    destination = bundle_dir(data_root) / f"{now.strftime('%Y%m%dT%H%M%S%z')}_health-bundle.json"
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return str(destination.resolve())


def write_zip_bundle(data_root: Path, payload: dict) -> str:
    now = dt.datetime.now().astimezone()
    destination = bundle_dir(data_root) / f"{now.strftime('%Y%m%dT%H%M%S%z')}_health-bundle.zip"
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr("bundle-metadata.json", json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        for relative in payload["files"]:
            bundle.write(data_root / relative, arcname=relative)
    return str(destination.resolve())


def main() -> int:
    args = parse_args()
    try:
        data_root = choose_data_root(args.data_root)
        if not data_root.exists():
            raise ExportError(f"Health data root does not exist: {data_root}")
        payload = export_payload(data_root)
        bundle_path = write_json_bundle(data_root, payload) if args.format == "json" else write_zip_bundle(data_root, payload)
        payload["bundle_path"] = bundle_path
        payload["bundle_format"] = args.format
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except ExportError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
