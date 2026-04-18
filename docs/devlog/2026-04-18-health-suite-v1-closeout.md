[English](README.md) | [中文](README.zh-CN.md)

# 2026-04-18 Health Suite V1 Closeout

## Context

The repository already had the core health implementation on `main`, but the public install surface and the living status docs still looked like the suite was only planned.

That mismatch was risky because:

- users could still see stale `v0.1.0` install examples
- suite install depended too much on a locally patched installer flow
- roadmap and control-surface docs still described Stage 3 to Stage 5 as incomplete

## Decision

Close health V1 as a real released suite instead of stopping at “main works”.

Key decisions:

1. Add `health/SKILL.md` and `health/agents/openai.yaml` so `health/` is a real umbrella install target.
2. Keep `health/SKILLSET.json` so hosts that understand suite manifests can still expand the nested skills directly.
3. Bind the public install docs to `v0.2.0`.
4. Add a reset playbook and require CLI acceptance as the release proof.

## Why Both `SKILL.md` And `SKILLSET.json`

`SKILLSET.json` alone was not stable enough as the only answer because it depends on host-side installer support.

The umbrella `SKILL.md` gives a second safe path:

- if the host understands suite manifests, install expands into multiple health skills
- if the host only installs one folder, `health/` still works as one family-doctor suite entry

This keeps install UX simple without collapsing runtime boundaries inside `health/`.

## Outcome

- `health/` is now a stable suite entry
- live docs explain suite install, single-skill install, reset, and restore
- roadmap and capability docs say `done` where the implementation is actually done
- CLI acceptance proves install, archive, doctor dialogue, review, brief, reminders, and restore
- `v0.2.0` becomes the stable public install target for health V1
