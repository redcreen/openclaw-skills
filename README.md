[English](README.md) | [中文](README.zh-CN.md)

# OpenClaw Skills Workspace

This repository is a multi-skill workspace for OpenClaw. It groups installable skills by top-level skill set such as `health/` and `order/`, while keeping every individual skill independently runnable.

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
| [`health`](health/README.md) | Personal health profile, archiving, interpretation, and planning | [`health-archive`](health/health-archive/README.md), [`private-doctor`](health/private-doctor/README.md) | Install one or more folders under `health/<skill-name>/` | Health data defaults to `~/document/personal health`; users choose the path during installation; Feishu stays off by default |
| `order` | Reserved for future order-related skills | none yet | not started | Must stay isolated from `health` when added |

## Install Model

Install at the skill-folder level, not at the skill-set level.

1. Choose the domain skill set, such as `health/`.
2. Open the README for the exact skill you want.
3. Install the folder that contains that skill's `SKILL.md`.
4. Apply only the configuration required by that skill.

## GitHub Direct Install

After the repository is published, prefer a copy-paste GitHub URL in the OpenClaw chat instead of asking users to browse the repo manually.

- stable install should be pinned to a tag:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.1.0/health/health-archive`
- development install may point to `main`:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/private-doctor`
- maintainers can generate the exact per-skill prompts with `python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.1.0`

## Skill Documentation

- Chinese overview: [README.zh-CN.md](README.zh-CN.md)
- Docs landing page: [docs/README.md](docs/README.md)
- GitHub install guide: [docs/reference/openclaw-skills/github-install.md](docs/reference/openclaw-skills/github-install.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- Roadmap: [docs/roadmap.md](docs/roadmap.md)
- Test plan: [docs/test-plan.md](docs/test-plan.md)
