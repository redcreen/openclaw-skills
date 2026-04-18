[English](development-plan.md) | [中文](development-plan.zh-CN.md)

# Development Plan

## What This Plan Is For

This plan turns the roadmap into an ordered execution queue for the workspace.

## How To Use It

- use `docs/roadmap.md` for milestone-level orientation
- use this file for the ordered implementation queue
- use `.codex/plan.md` for the current execution line only

## Current Position

The workspace has completed the `health` baseline, but it has not yet closed the full intended health-agent capability. The next work is to turn the existing health skill set into a complete, reset-ready family-doctor suite.

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
- local-first health storage anchored on `~/document/personal health`

## Stage 2: Archive and Family-Doctor Baseline

### Goal

Deliver the first archive-and-doctor loop for `health`.

### Status

Complete.

### Completed Work

1. Created the `health` landing README pair.
2. Created `health-archive` and `private-doctor` as standard skill folders.
3. Defined the local storage contract for `~/document/personal health`.
4. Implemented the archive, summary, profile-update, and reply-rendering scripts.
5. Published GitHub install entry points and `v0.1.0`.

## Stage 3: Health Suite Install and Doctor-Core Completion

### Goal

Close the core gap between the current skill set and the intended health agent: one-command suite install, proactive onboarding, baseline risk assessment, and doctor dialogue that continues after image archiving.

### Status

Active.

### Existing Base

1. `health-archive` already supports verified local-first archive writes.
2. `private-doctor` already supports basic profile maintenance and doctor-style reply rendering.
3. The repository is public and already has tag-based install docs.

### Ordered Queue

1. Define the `health` suite install contract:
   - one command installs multiple health skill folders
   - runtime still stays modular
   - `health/` is not turned into a fake monolithic skill
2. Ship the health-suite install entry:
   - bundle manifest or helper command
   - release-facing docs for full-suite install
3. Expand the baseline profile schema for:
   - identity and goals
   - blood pressure / lipid / glucose context
   - current medication
   - lifestyle and main concerns
4. Complete the doctor-core behavior in `private-doctor`:
   - proactive onboarding
   - baseline risk framing
   - first-phase action plan
   - explicit follow-up focus
5. Add CLI acceptance for the core loop:
   - image or fact archive
   - read from the local workspace
   - continue with doctor-style interpretation and next steps
6. Decide whether archive needs a multi-image single-session helper as part of the same slice.

### Exit Criteria

- one command can install the full `health` suite
- after reset, the skill suite can immediately rebuild the core doctor workflow
- CLI proves image archive -> doctor dialogue without relying on manual user QA

## Stage 4: Longitudinal Review and Clinician Briefs

### Goal

Deliver long-term review, trend follow-up, and clinician-facing outputs.

### Status

Planned.

### Ordered Queue

1. Add `health-review`:
   - daily review
   - weekly summary
   - monthly or stage review
2. Persist review outputs into the local workspace:
   - `reviews/`
   - stable output contract and metadata
3. Add `doctor-brief`:
   - clinician-readable brief
   - stage summary for visits
4. Persist clinician outputs into the local workspace:
   - `reports/`
   - stable doctor-brief format
5. Add CLI acceptance:
   - records -> review output
   - records -> clinician brief

### Exit Criteria

- longitudinal review exists as a first-class skill instead of ad hoc dialogue only
- clinician-facing summaries are generated from the same local workspace contract
- the suite now supports ongoing tracking and clinic-prep workflows

## Stage 5: Reminders, Migration, and Health V1 Closeout

### Goal

Deliver reminders, reset/migration readiness, and final acceptance for the skill-based health agent.

### Status

Planned.

### Ordered Queue

1. Add `health-reminders` or an equivalent scheduling contract:
   - fixed reminders
   - lightweight fallback reminders
   - do not push all timing logic into one chat skill
2. Add reset and migration readiness:
   - backup flow before resetting the old health agent
   - Feishu export or backup path
   - restore path into the local workspace
3. Decide and, if kept, add optional `health-storage-feishu`:
   - mirror/export only
   - never the main source of truth
4. Build the final CLI acceptance suite:
   - full-suite install
   - archive
   - doctor dialogue
   - review
   - clinician brief
   - reminder basics
5. Use CLI acceptance as the release gate instead of asking the user to do the foundational testing.

### Exit Criteria

- the old health agent can be reset after backup and replaced by the skill suite
- the full intended health-agent V1 capability is covered by modular skills
- readiness is proven by CLI-first acceptance
