[English](github-install.md) | [中文](github-install.zh-CN.md)

# GitHub Install Guide

This document defines the standard public install entry for this workspace once it is published.

## Goal

Users should not need to understand the repository layout. They should be able to paste one skill's GitHub URL into the OpenClaw chat and install it directly.

## Recommended Install Format

For published installs, pin to a tag:

```text
Install skill suite: https://github.com/redcreen/openclaw-skills/tree/main/health
Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.1.0/health/health-archive
Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.1.0/health/private-doctor
```

For development or internal testing, `main` is acceptable:

```text
Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-archive
```

## Maintainer Release Steps

1. Publish the repository to GitHub.
2. Create a stable tag such as `v0.1.0`.
3. Run the generator:

```bash
python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.1.0 --format markdown
```

4. Copy the generated GitHub URL or `Install skill: ...` prompt into release notes, README files, or handoff docs.

## Why Tag-First

- `main` keeps moving, so it is not a stable public install target
- `tree/<tag>/<skill-path>` pins the installed content to one version
- skill-folder URLs preserve skill-level isolation instead of encouraging a full `health/` install as one monolith

## Current Constraint

- the bound public repository is `redcreen/openclaw-skills`
- `health/` can now act as a suite-install entry because it contains `SKILLSET.json`, which expands into multiple installed skills
