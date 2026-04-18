# 2026-04-18 public doc i18n gate convergence

## Context

The repository already had English/Chinese public docs and per-skill README pairs, but the install-facing health docs were not being treated as a governed bilingual surface.

## Problem

There were two separate drifts:

1. `.codex/doc-governance.json` marked `health/**/*.md` as public docs, which was too broad. That pulled in `SKILL.md`, internal references, and devlog entries.
2. The actual user-facing doc pairs did not have the required `[English](...) | [中文](...)` switch line at the top, so the i18n validator would have failed once it was pointed at the right files.

## Root Cause

The repo-level public-doc contract was underspecified. It knew `health` was a first-class module, but it did not distinguish user-facing landing/install README files from internal skill contract and reference docs.

## Fix

1. Narrowed `publicDocIncludeGlobs` to the real public surfaces:
   - root `README`
   - public `docs/*`
   - `health/README*`
   - `health/*/README*`
2. Added the required bilingual switch line to the governed public doc pairs.
3. Added per-skill README pairs to `requiredPaths` so install-facing docs stay part of the durable structure.

## Validation

Ran:

```bash
python3 ~/.codex/skills/project-assistant/scripts/validate_public_docs_i18n.py . --format json
```

Result:

- `ok: true`
- no missing counterparts
- no switch-line warnings

## Outcome

The repo now matches the intended rule: bilingual public docs apply to actual user-facing install and landing pages, not every markdown file under a skill folder.
