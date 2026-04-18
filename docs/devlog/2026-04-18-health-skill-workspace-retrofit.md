# 2026-04-18 Health Skill Workspace Retrofit

## Problem

The repository started as a generic multi-skill workspace, but the incoming direction was stronger than that:

- different domains such as `health` and `order` must stay isolated
- root docs must index multiple skill sets and multiple individual skills
- health is no longer a single mixed agent; it is becoming a reusable skill set
- health V1 must be local-first instead of Feishu-first

Without restructuring at the workspace level, future skills would inherit an ambiguous layout and repeat the same coupling problems seen in the earlier health agent.

## Decision

Treat the repo as a `large` project with first-class modules.

The resulting structure is:

- root README pair as workspace index
- `docs/` as shared workspace documentation
- top-level skill-set folders such as `health/`
- per-skill folders under each set with `SKILL.md`, `agents/openai.yaml`, and per-skill README pair
- `.codex/module-dashboard.md` plus module files for `health` and future `order`

## Key Tradeoffs

### Why top-level skill-set folders

This is the correct boundary for domain separation. A flat workspace would make health and order look like peer skills without any domain guardrail, which is too weak for the requested isolation.

### Why per-skill README pairs despite generic skill guidance preferring fewer docs

This repo is both a development workspace and a distribution/index surface. The user explicitly needs root, skill-set, and per-skill install routing. That justifies lightweight per-skill READMEs in addition to `SKILL.md`.

### Why local-first for health

Recent health-agent logs showed that recognition was often present while durable write confidence was not. Moving the source of truth to local files is the simplest way to make archive success explicit before adding optional external adapters back in.

## Consequences

- future `order` work should start under `order/`, not inside `health/`
- shared runtime reuse across domains now requires an explicit new boundary
- `health-archive` becomes the first functional slice because it solves the user's trust problem about whether data was really recorded
- `private-doctor` becomes the second functional slice because it solves the role problem of being more than a recorder

## Validation Performed

- created module-aware control-surface files
- added root, skill-set, and per-skill README routing
- created `health-archive` and `private-doctor` skill skeletons
- verified the expected key files exist

## Next Step

Implement the local storage contract and first real archive workflow inside `health-archive`.
