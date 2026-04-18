# Project Plan

## Current Phase

Health full-capability planning is locked; Stage 3 implementation is next.

## Current Execution Line

- Objective: implement Stage 3 so the `health` suite can be installed in one command and can immediately handle onboarding, initial assessment, and image-driven archive-to-doctor dialogue
- Plan Link: health suite install and doctor-core completion
- Runway: one checkpoint-sized execution line
- Progress: 0 / 6 tasks complete
- Stop Conditions:
  - suite install requires host support that cannot be represented by the current GitHub + skill-installer model
  - the medical scope expands beyond the agreed family-doctor V1 boundary
  - the reset or migration path needs product decisions outside the repo
- Validation:
  - one command installs the full `health` suite from a stable tag
  - CLI proves archive -> doctor dialogue on the same local workspace
  - onboarding and initial assessment work without manual patching of files

## Execution Tasks

- [ ] EL-1 define and implement the one-command `health` suite install flow
- [ ] EL-2 expand the baseline health profile schema for onboarding and three-high context
- [ ] EL-3 add initial risk framing and first-phase planning to `private-doctor`
- [ ] EL-4 verify image-or-fact archive -> doctor dialogue through CLI
- [ ] EL-5 decide whether archive needs a multi-image single-session helper
- [ ] EL-6 refresh release-facing docs and manifests for the suite-install entry

## Development Log Capture

- Trigger Level: high
- Auto-Capture When:
  - a repo-level structure replaces a looser folder convention
  - a new shared contract is introduced for multiple skills
  - an architecture or documentation retrofit changes how maintainers add future skill sets
  - a tradeoff about cross-skill reuse or capability packaging is made explicit
- Skip When:
  - the work is purely copy-editing
  - a file change only mirrors already agreed structure
  - no durable reasoning changed

## Architecture Supervision
- Signal: `green`
- Problem Class: capability gap between the released `health` baseline and the intended health-agent V1
- Root Cause Hypothesis: the repo already solved structure and baseline scripts, but it has not yet closed suite-install, onboarding, and end-to-end acceptance
- Correct Layer: modular health-skill delivery plus CLI acceptance
- Rejected Shortcut: shipping another monolithic health agent or pretending the current two-skill baseline is already complete
- Escalation Gate: continue automatically

## Escalation Model

- Continue Automatically: health-suite implementation stays within the agreed local-first family-doctor direction
- Raise But Continue: a design detail drifts but can still converge inside the current roadmap
- Require User Decision: medical scope, install UX, or migration expectations materially change the intended product

## Slices
- Slice: workspace and local-first baseline
  - Objective: establish the repo, health landing docs, and local-first data contract
  - Dependencies: maintainer agreement on module isolation
  - Risks: structure drift and storage drift
  - Validation: root docs, architecture, and local data contract agree
  - Exit Condition: health is ready for implementation instead of folder debate

- Slice: archive and family-doctor baseline
  - Objective: deliver `health-archive` and `private-doctor` as the first usable loop
  - Dependencies: workspace and local-first baseline
  - Risks: record state remains ambiguous or the doctor layer collapses into a recorder
  - Validation: archive writes are explicit and doctor replies are grounded in local records
  - Exit Condition: baseline archive and doctor dialogue are usable

- Slice: health suite install and doctor-core completion
  - Objective: close one-command suite install, onboarding, initial assessment, and archive-to-doctor continuity
  - Dependencies: archive and family-doctor baseline
  - Risks: users still need the old health agent to get the core workflow
  - Validation: one-command install plus CLI archive -> doctor dialogue
  - Exit Condition: reset-ready core health workflow exists

- Slice: longitudinal review and clinician briefs
  - Objective: add review/report skills for sustained follow-up and clinic prep
  - Dependencies: health suite install and doctor-core completion
  - Risks: the suite still behaves like a recorder plus single-shot advice tool
  - Validation: local `reviews/` and `reports/` outputs exist and are CLI-testable
  - Exit Condition: long-term tracking and doctor brief workflows are covered

- Slice: reminders, migration, and health V1 closeout
  - Objective: add reminders, reset/migration readiness, and final acceptance for the full skill-based health agent
  - Dependencies: longitudinal review and clinician briefs
  - Risks: the user still has to manually bridge the old agent or manually test the core flow
  - Validation: reminder path exists, reset/migration playbook exists, and CLI acceptance covers the full suite
  - Exit Condition: the intended health-agent V1 is fully covered by modular skills
