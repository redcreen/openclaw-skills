[English](development-plan.md) | [中文](development-plan.zh-CN.md)

# Development Plan

## What This Plan Is For

This plan turns the roadmap into an ordered execution queue for the workspace.

## How To Use It

- use `docs/roadmap.md` for milestone-level orientation
- use this file for the ordered implementation queue
- use `.codex/plan.md` for the current execution line only

## Current Position

The workspace has now closed the intended health-agent V1 inside the modular `health` skill set. The remaining work after this plan is future iteration, not missing closure for the baseline family-doctor replacement.

## Health V1 Closure Target

This roadmap closes only when all of the following are true:

1. After resetting the old health agent, the full `health` suite can be installed with one command.
2. Once installed, the agent can archive incoming health images or facts and continue the doctor-style dialogue on top of those records.
3. Longitudinal review, clinician brief, and reminder capabilities are handled by skills instead of the old monolithic agent.
4. Release readiness is proven by CLI-first acceptance, not by asking the user to perform the basic end-to-end checks manually.
5. Feishu remains optional for backup or mirroring and does not block the local-first health workflow.

## Stage 1: Workspace and Local-First Baseline

### Goal

Define the repository as a multi-skill-set workspace and establish the local-first health baseline.

### Status

Complete.

### Completed Work

- root README pair converted into workspace indexes
- architecture, roadmap, and test-plan pages added
- module-aware `.codex` layer added
- local-first health storage anchored on `~/Documents/personal health`

## Stage 2: Archive and Family-Doctor Baseline

### Goal

Deliver the first archive-and-doctor loop for `health`.

### Status

Complete.

### Completed Work

1. Created the `health` landing README pair.
2. Created `health-archive` and `private-doctor` as standard skill folders.
3. Defined the local storage contract for `~/Documents/personal health`.
4. Implemented the archive, summary, profile-update, and reply-rendering scripts.
5. Published GitHub install entry points and `v0.1.0`.

## Stage 3: Health Suite Install and Doctor-Core Completion

### Goal

Close the core gap between the current skill set and the intended health agent: one-command suite install, proactive onboarding, baseline risk assessment, and doctor dialogue that continues after image archiving.

### Status

Complete.

### Completed Work

1. Added `health/SKILL.md` and `health/SKILLSET.json` so the suite has a stable top-level install entry while keeping nested skills independently installable.
2. Added `archive_health_session.py` to support multi-item archive sessions from one user message.
3. Expanded `private-doctor` with onboarding assessment, baseline risk framing, and first-phase plan generation.
4. Added CLI acceptance that proves archive -> doctor interpretation -> next-step reply on the same local workspace.
5. Refreshed release-facing install docs around the suite entry.

### Exit Criteria

- one command can install the full `health` suite
- after reset, the skill suite can immediately rebuild the core doctor workflow
- CLI proves image archive -> doctor dialogue without relying on manual user QA

## Stage 4: Longitudinal Review and Clinician Briefs

### Goal

Deliver long-term review, trend follow-up, and clinician-facing outputs.

### Status

Complete.

### Completed Work

1. Added `health-review` with daily, weekly, and monthly review generation.
2. Persisted review outputs into `reviews/` with a stable saved-output contract.
3. Added `doctor-brief` for clinician-readable briefs and stage summaries.
4. Persisted clinician outputs into `reports/`.
5. Covered review and brief generation in the CLI acceptance chain.

### Exit Criteria

- longitudinal review exists as a first-class skill instead of ad hoc dialogue only
- clinician-facing summaries are generated from the same local workspace contract
- the suite now supports ongoing tracking and clinic-prep workflows

## Stage 5: Reminders, Migration, and Health V1 Closeout

### Goal

Deliver reminders, reset/migration readiness, and final acceptance for the skill-based health agent.

### Status

Complete.

### Completed Work

1. Added `health-reminders` for recurring reminder rules and due-reminder checks.
2. Added `health-storage-feishu` as the optional bundle export and restore layer for backup or migration readiness.
3. Added a reset and migration playbook so the old health agent can be replaced safely.
4. Built the final CLI acceptance suite for install, archive, doctor dialogue, review, clinician brief, reminders, and bundle restore.
5. Kept Feishu optional instead of making it the required source of truth.

### Exit Criteria

- the old health agent can be reset after backup and replaced by the skill suite
- the full intended health-agent V1 capability is covered by modular skills
- readiness is proven by CLI-first acceptance
