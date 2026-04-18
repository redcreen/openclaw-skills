# Architecture

## System Shape

This repository is a module-aware OpenClaw skill workspace.

- each top-level folder such as `health/` or `order/` represents one isolated skill set
- each nested skill folder such as `health/health-archive/` represents one installable skill
- each skill owns its own `SKILL.md`, UI metadata, prompts, references, and assets

## Topology

```text
<repo root>/
  <skill-set>/
    README.md
    README.zh-CN.md
    <skill-name>/
      SKILL.md
      agents/openai.yaml
      README.md
      README.zh-CN.md
```

## Boundary Rules

- a skill set must not absorb another domain's business rules
- a skill must not import, call, or load runtime assets from sibling skills
- a skill in one set must not reuse runtime resources from another set
- repository-level documentation may be shared across the workspace
- if true reuse becomes necessary, it must be introduced as an explicit shared boundary instead of a shortcut through another skill folder

## Module Inventory

### `health`

- purpose: personal health profile, archive, interpretation, and planning
- current skills: `health-archive`, `private-doctor`
- default external data root: `~/document/personal health`
- Feishu policy: disabled by default; future optional storage adapter only

### `order`

- purpose: reserved for future order-related skills
- current state: planned, not yet scaffolded
- rule: must not reuse `health` runtime logic, prompts, or assets

## Data and Runtime Boundaries

- user data must live outside the repository
- a skill may define a default external data root, but installation must let the user override it
- the `health` set defaults to `~/document/personal health`
- skill status must be reported from the storage operation that actually happened, not from inference

## Documentation Model

- root `README*` files act as workspace indexes
- each skill set owns its own landing README pair
- each skill owns its own README pair for install and usage
- `docs/` owns shared workspace docs such as architecture, roadmap, test plan, and development plan

## Rejected Shortcuts

- putting all health behavior into one large mixed agent folder
- copying a skill from one domain and adapting it informally for another domain
- treating Feishu or another external system as the only record of truth when local-first storage is the intended contract
