#!/usr/bin/env python3
"""Restore a health workspace from a portable bundle."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


DEFAULT_DATA_ROOT = Path("~/Documents/personal health").expanduser()


class ImportError(Exception):
    """Raised when the health workspace bundle cannot be restored."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Restore a portable health workspace bundle."
    )
    parser.add_argument("--bundle-file", required=True, help="Path to a bundle file (.zip or .json).")
    parser.add_argument("--data-root", help="Override the external health data root.")
    parser.add_argument("--overwrite", action="store_true", help="Allow overwriting existing files.")
    return parser.parse_args()


def choose_data_root(arg_root: str | None) -> Path:
    if arg_root:
        return Path(arg_root).expanduser()
    env_root = os.environ.get("HEALTH_DATA_ROOT") or os.environ.get("HEALTH_ARCHIVE_ROOT")
    if env_root:
        return Path(env_root).expanduser()
    return DEFAULT_DATA_ROOT


def restore_zip(bundle_path: Path, data_root: Path, overwrite: bool) -> list[str]:
    restored: list[str] = []
    with zipfile.ZipFile(bundle_path, "r") as bundle:
        for name in bundle.namelist():
            if not name or name == "bundle-metadata.json" or name.endswith("/"):
                continue
            target = data_root / name
            if target.exists() and not overwrite:
                raise ImportError(f"Refusing to overwrite existing file without --overwrite: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(name, "r") as source, open(target, "wb") as destination:
                shutil.copyfileobj(source, destination)
            restored.append(name)
    return restored


def restore_json(bundle_path: Path, data_root: Path) -> list[str]:
    payload = json.loads(bundle_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ImportError("JSON bundle must be a JSON object.")
    return [str(item) for item in payload.get("files", [])]


def main() -> int:
    args = parse_args()
    try:
        bundle_path = Path(args.bundle_file).expanduser()
        if not bundle_path.is_file():
            raise ImportError(f"Bundle file does not exist: {bundle_path}")
        data_root = choose_data_root(args.data_root)
        data_root.mkdir(parents=True, exist_ok=True)

        if bundle_path.suffix.lower() == ".zip":
            restored = restore_zip(bundle_path, data_root, args.overwrite)
        elif bundle_path.suffix.lower() == ".json":
            restored = restore_json(bundle_path, data_root)
        else:
            raise ImportError("Bundle file must use .zip or .json.")

        result = {
            "status": "ok",
            "bundle_path": str(bundle_path.resolve()),
            "data_root": str(data_root.resolve()),
            "restored_count": len(restored),
            "restored_files": restored,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (ImportError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
