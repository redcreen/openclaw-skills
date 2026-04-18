# Development Plan

## What This Plan Is For

This plan turns the roadmap into an ordered execution queue for the workspace.

## How To Use It

- use `docs/roadmap.md` for milestone-level orientation
- use this file for the ordered implementation queue
- use `.codex/plan.md` for the current execution line only

## Current Position

The workspace has completed the first functional and install-template pass for `health` and is now in Stage 5 release/guardrail work.

## Stage 1: Workspace Governance Baseline

### Goal

Define the repository as a multi-skill-set workspace with root indexing, durable docs, and module-aware control files.

### Status

Complete.

### Completed Work

- root README pair converted into workspace indexes
- architecture, roadmap, and test-plan pages added
- module-aware `.codex` layer added

## Stage 2: Health Skill-Set Baseline

### Goal

Create `health/` as the first isolated skill-set root with independent public docs and standard skill folders.

### Status

Complete.

### Completed Work

1. Created the `health` landing README pair.
2. Created `health-archive` as a standard skill folder.
3. Created `private-doctor` as a standard skill folder.
4. Defined install and storage expectations in the skill-set docs.

## Stage 3: Health-Archive Functional Delivery

### Goal

Deliver local-first health archiving with explicit success reporting.

### Status

Complete.

### Completed Work

1. Defined the local storage contract for `~/document/personal health`.
2. Added an archive format reference and field map.
3. Implemented `scripts/archive_health_record.py`.
4. Wired the skill workflow to use the script result as the archive truth source.
5. Verified archive creation and duplicate replay behavior with a local smoke test.

## Stage 4: Private-Doctor Functional Delivery

### Goal

Deliver concise family-doctor behavior that explains, advises, and plans instead of acting like a passive recorder.

### Status

Complete.

### Completed Work

1. Added `scripts/summarize_health_workspace.py`.
2. Added `scripts/update_health_profile.py`.
3. Added `scripts/render_doctor_reply.py`.
4. Added `scripts/validate_doctor_reply.py`.
5. Added doctor workflow, onboarding, and reply-contract references.
6. Verified summary, profile updates, and doctor-reply rendering against the same local health workspace.

## Stage 5: Future Skill-Set Expansion and Guardrails

### Goal

Add future skill sets without mixing domains or re-opening structure drift.

### Status

Active.

### Completed Work

1. Added `scripts/validate_skill_boundaries.py` for runtime isolation checks.
2. Added GitHub direct-install reference docs.
3. Added `scripts/generate_skill_install_manifest.py` to generate per-skill install URLs and prompts.
4. Updated the root README, `health` landing page, and per-skill READMEs with copy-paste GitHub install templates.

### Ordered Queue

1. Bind a real GitHub `owner/repo` and first stable tag.
2. Run an install acceptance test starting from a GitHub URL.
3. Create the `order/` module only when the first order skill is defined.
4. Add more per-module validation and release guidance as the workspace grows.
