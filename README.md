[English](README.md) | [中文](README.zh-CN.md)

# OpenClaw Skills Workspace

This repository is a multi-skill workspace for OpenClaw. It groups installable skills by top-level skill set such as `health/` and `order/`, while keeping every domain isolated and every concrete skill independently runnable.

## Workspace Rules

- one top-level skill set per domain
- one installable skill per folder
- no runtime imports, prompt loading, or asset loading across sibling skills
- no mixing of domain logic across skill sets such as `health` and `order`
- repository docs may be shared, but runtime reuse must be introduced deliberately as a separate boundary

## Repository Layout

```text
openclaw-skills/
  health/
    README.md
    SKILL.md
    SKILLSET.json
    health-archive/
      SKILL.md
    private-doctor/
      SKILL.md
  order/
    ...
  docs/
    README.md
    architecture.md
    roadmap.md
    test-plan.md
```

## Skill Set Index

| Skill Set | Purpose | Available Skills | Install Path | Usage Notes |
| --- | --- | --- | --- | --- |
| [`health`](health/README.md) | Personal health profile, archiving, family-doctor dialogue, reviews, briefs, reminders, and backup | [`health`](health/README.md), [`health-archive`](health/health-archive/README.md), [`private-doctor`](health/private-doctor/README.md), [`health-review`](health/health-review/README.md), [`doctor-brief`](health/doctor-brief/README.md), [`health-reminders`](health/health-reminders/README.md), [`health-storage-feishu`](health/health-storage-feishu/README.md) | Install `health/` for the whole suite, or install any `health/<skill-name>/` folder directly | Health data defaults to `~/document/personal health`; users choose the path during installation; Feishu stays off by default |
| `order` | Reserved for future order-related skills | none yet | not started | Must stay isolated from `health` when added |

## Install Model

Install either the suite entry or the exact skill folder you need.

1. If you want the full family-doctor workflow, install `health/`.
2. If you want only one focused workflow, install the exact folder such as `health/health-archive/`.
3. Read the corresponding README for the behavior and data-root rules.
4. Apply only the configuration required by the selected install target.

## GitHub Direct Install

After the repository is published, prefer a copy-paste GitHub URL in the OpenClaw chat instead of asking users to browse the repo manually.

- stable suite install should be pinned to a tag:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health`
- stable single-skill install may also be pinned to the same tag:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/private-doctor`
- development install may point to `main`:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health`
- maintainers can generate the exact prompts with `python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.2.0 --domain health`

## Skill Documentation

- Chinese overview: [README.zh-CN.md](README.zh-CN.md)
- Docs landing page: [docs/README.md](docs/README.md)
- GitHub install guide: [docs/reference/openclaw-skills/github-install.md](docs/reference/openclaw-skills/github-install.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- Roadmap: [docs/roadmap.md](docs/roadmap.md)
- Test plan: [docs/test-plan.md](docs/test-plan.md)
