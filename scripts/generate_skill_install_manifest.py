#!/usr/bin/env python3
"""Generate GitHub install URLs and copy-paste prompts for installable skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


IGNORED_TOP_LEVEL = {
    ".codex",
    "docs",
    "scripts",
    "__pycache__",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate GitHub install URLs for installable skills."
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="GitHub repository in owner/repo format.",
    )
    parser.add_argument(
        "--ref",
        default="main",
        help="Git ref to pin the install URL to. Default: main",
    )
    parser.add_argument(
        "--domain",
        help="Optional top-level skill-set filter, such as health.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text", "markdown"],
        default="text",
        help="Output format.",
    )
    return parser.parse_args(argv)


def validate_repo(value: str) -> tuple[str, str]:
    parts = [part for part in value.split("/") if part]
    if len(parts) != 2:
        raise ValueError("--repo must be in owner/repo format.")
    return parts[0], parts[1]


def discover_skills(root: Path, domain: str | None) -> list[Path]:
    skills: list[Path] = []
    for top_level in sorted(root.iterdir()):
        if not top_level.is_dir():
            continue
        if top_level.name in IGNORED_TOP_LEVEL or top_level.name.startswith("."):
            continue
        if domain and top_level.name != domain:
            continue
        for child in sorted(top_level.iterdir()):
            if child.is_dir() and (child / "SKILL.md").is_file():
                skills.append(child.resolve())
    return skills


def build_entries(root: Path, repo: str, ref: str, skill_dirs: list[Path]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for skill_dir in skill_dirs:
        relative_path = skill_dir.relative_to(root).as_posix()
        skill_set, skill_name = relative_path.split("/", 1)
        github_url = f"https://github.com/{repo}/tree/{ref}/{relative_path}"
        entries.append(
            {
                "skill_set": skill_set,
                "skill_name": skill_name,
                "path": relative_path,
                "github_url": github_url,
                "install_prompt_zh": f"安装技能：{github_url}",
                "install_prompt_en": f"Install skill: {github_url}",
            }
        )
    return entries


def build_suite_entry(repo: str, ref: str, domain: str) -> dict[str, str]:
    github_url = f"https://github.com/{repo}/tree/{ref}/{domain}"
    return {
        "skill_set": domain,
        "skill_name": domain,
        "path": domain,
        "github_url": github_url,
        "install_prompt_zh": f"安装技能：{github_url}",
        "install_prompt_en": f"Install skill: {github_url}",
    }


def render_text(repo: str, ref: str, entries: list[dict[str, str]]) -> str:
    lines = [
        f"Repository: {repo}",
        f"Ref: {ref}",
        "",
    ]
    for index, entry in enumerate(entries, start=1):
        lines.extend(
            [
                f"{index}. {entry['path']}",
                f"   GitHub URL: {entry['github_url']}",
                f"   OpenClaw Prompt (ZH): {entry['install_prompt_zh']}",
                f"   OpenClaw Prompt (EN): {entry['install_prompt_en']}",
            ]
        )
    return "\n".join(lines)


def render_markdown(repo: str, ref: str, entries: list[dict[str, str]]) -> str:
    lines = [
        f"# Skill Install Manifest",
        "",
        f"- Repository: `{repo}`",
        f"- Ref: `{ref}`",
        "",
        "| Skill | GitHub URL | OpenClaw Prompt (ZH) | OpenClaw Prompt (EN) |",
        "| --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['path']}`",
                    f"`{entry['github_url']}`",
                    f"`{entry['install_prompt_zh']}`",
                    f"`{entry['install_prompt_en']}`",
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        validate_repo(args.repo)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    root = repo_root()
    skills = discover_skills(root, args.domain)
    if not skills:
        message = "No installable skills found."
        if args.domain:
            message = f"No installable skills found under top-level domain: {args.domain}"
        print(message, file=sys.stderr)
        return 1

    entries = build_entries(root, args.repo, args.ref, skills)
    suite_entry = build_suite_entry(args.repo, args.ref, args.domain) if args.domain else None

    if args.format == "json":
        payload = {
            "repo": args.repo,
            "ref": args.ref,
            "skill_count": len(entries),
            "skills": entries,
        }
        if suite_entry is not None:
            payload["skill_set"] = suite_entry
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.format == "markdown":
        if suite_entry is not None:
            entries = [suite_entry] + entries
        print(render_markdown(args.repo, args.ref, entries))
        return 0

    if suite_entry is not None:
        entries = [suite_entry] + entries
    print(render_text(args.repo, args.ref, entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
