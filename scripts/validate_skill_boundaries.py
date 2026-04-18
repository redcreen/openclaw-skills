#!/usr/bin/env python3
"""Validate that runtime skill files do not reference sibling skill folders."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "README.md",
    "README.zh-CN.md",
]
RUNTIME_PATTERNS = [
    "SKILL.md",
    "agents/**/*.yaml",
    "scripts/**/*",
]
IGNORED_TOP_LEVEL = {
    ".codex",
    "docs",
    "scripts",
    "__pycache__",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def discover_skills(root: Path) -> list[Path]:
    skills: list[Path] = []
    for top_level in sorted(root.iterdir()):
        if not top_level.is_dir() or top_level.name in IGNORED_TOP_LEVEL or top_level.name.startswith("."):
            continue
        for child in sorted(top_level.iterdir()):
            if child.is_dir() and (child / "SKILL.md").is_file():
                skills.append(child.resolve())
    return skills


def load_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def runtime_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in RUNTIME_PATTERNS:
        for path in skill_dir.glob(pattern):
            if path.is_file():
                files.append(path)
    return sorted(set(files))


def validate_required_files(skill_dir: Path, root: Path) -> list[dict[str, str]]:
    issues = []
    for relative in REQUIRED_FILES:
        path = skill_dir / relative
        if not path.is_file():
            issues.append(
                {
                    "type": "missing-required-file",
                    "skill": skill_dir.relative_to(root).as_posix(),
                    "file": relative,
                }
            )
    return issues


def validate_cross_references(skill_dirs: list[Path], root: Path) -> list[dict[str, str]]:
    violations = []
    skill_refs = {
        skill_dir: {
            "relative": skill_dir.relative_to(root).as_posix(),
            "absolute": str(skill_dir),
        }
        for skill_dir in skill_dirs
    }

    for owner in skill_dirs:
        owner_ref = skill_refs[owner]["relative"]
        for file_path in runtime_files(owner):
            content = load_text(file_path)
            if content is None:
                continue
            for target, refs in skill_refs.items():
                if target == owner:
                    continue
                for marker in (refs["relative"], refs["relative"] + "/", refs["absolute"]):
                    if marker and marker in content:
                        violations.append(
                            {
                                "type": "cross-skill-reference",
                                "owner_skill": owner_ref,
                                "file": file_path.relative_to(root).as_posix(),
                                "forbidden_reference": refs["relative"],
                                "matched_text": marker,
                            }
                        )
                        break
    return violations


def main() -> int:
    root = repo_root()
    skills = discover_skills(root)
    issues: list[dict[str, str]] = []

    for skill_dir in skills:
        issues.extend(validate_required_files(skill_dir, root))
    issues.extend(validate_cross_references(skills, root))

    result = {
        "status": "ok" if not issues else "error",
        "repo_root": str(root),
        "skill_count": len(skills),
        "skills": [skill_dir.relative_to(root).as_posix() for skill_dir in skills],
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
