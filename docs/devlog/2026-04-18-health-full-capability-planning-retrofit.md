[English](README.md) | [中文](README.zh-CN.md)

# 2026-04-18 health full-capability planning retrofit

## Context

The repository already had a clean local-first health baseline, but the planning surface still mostly reflected workspace governance, first-release packaging, and baseline skill delivery.

## Problem

That plan was not sufficient for the real product target. The user expectation is higher:

1. the old health agent can be reset after backup
2. the full `health` suite can be installed in one command
3. the installed suite behaves like a complete family-doctor workflow
4. CLI-first validation exists before asking the user to do acceptance testing

## Decision

Retool the planning stack from “baseline health skills plus release plumbing” into “full health-agent V1 closure”.

This required changes to:

- roadmap
- development plan
- architecture
- health landing docs
- module planning
- capability mapping

## Main Changes

1. Reframed the roadmap around five stages that end with full health-agent V1 closure.
2. Added an explicit health capability map so the original health-agent intent is traceable to concrete skills and stages.
3. Declared one-command suite install as a distribution goal without collapsing runtime boundaries into a fake monolith.
4. Made CLI-first acceptance a hard roadmap requirement instead of a nice-to-have.
5. Deferred `order` expansion behind health V1 completion.

## Result

The planning surface now answers the real question: what still needs to be built before the old health agent can be reset and replaced by a modular skill suite.

## Validation

Validated the updated public-doc set with:

```bash
python3 ~/.codex/skills/project-assistant/scripts/validate_public_docs_i18n.py . --format json
```

The bilingual public-doc validator passed after the planning retrofit.
