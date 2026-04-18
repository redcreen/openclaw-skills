# Project Status

## Delivery Tier
- Tier: `large`
- Why this tier: the repo now has to carry a full health-agent replacement roadmap, staged skill delivery, release packaging, and CLI-first acceptance
- Last reviewed: 2026-04-18

## Current Phase

Health V1 released; the latest stable patch tag is `v0.2.1`.

## Active Slice

No active delivery slice. Health V1 is released; future work is optional iteration.

## Current Execution Line

- Objective: keep the released `health` suite stable and leave future work optional
- Plan Link: health V1 released
- Runway: one release-maintenance checkpoint at a time
- Progress: 6 / 6 tasks complete
- Stop Conditions:
  - the medical scope expands beyond the agreed health-agent V1 boundary
  - migration/reset expectations require product decisions outside this repo

## Execution Tasks

- [x] EL-1 define and implement the one-command `health` suite install flow
- [x] EL-2 expand the baseline health profile schema for onboarding and three-high context
- [x] EL-3 add initial risk framing and first-phase planning to `private-doctor`
- [x] EL-4 verify image-or-fact archive -> doctor dialogue through CLI
- [x] EL-5 decide whether archive needs a multi-image single-session helper
- [x] EL-6 publish the stable release and rerun CLI acceptance against the release tag

## Development Log Capture

- Trigger Level: high
- Pending Capture: no
- Last Entry: `docs/devlog/2026-04-18-health-v0.2.1-patch-release.md`

## Architecture Supervision
- Signal: `green`
- Signal Basis: the stable release is published and the suite contract is now explicit
- Root Cause Hypothesis: future drift would come from post-release changes, not an incomplete V1 baseline
- Correct Layer: future iteration and regression control
- Automatic Review Trigger: review again when a new health release starts
- Escalation Gate: continue automatically

## Current Escalation State
- Current Gate: continue automatically
- Reason: health V1 is released and no blocking capability gap remains
- Next Review Trigger: a future slice reopens the health module

## Done

- large-project classification applied
- module-aware control surface added
- root README pair converted toward index-driven entry docs
- durable roadmap, development plan, and test-plan pages added
- `health` skill-set landing docs added
- `health-archive` and `private-doctor` skill skeletons created
- `health-archive` local-first storage contract documented
- `health-archive/scripts/archive_health_record.py` implemented
- archive smoke test passed, including duplicate replay detection
- `private-doctor` summary and profile-update scripts implemented
- `private-doctor` reply renderer and reply validator implemented
- `private-doctor` workflow, onboarding, and reply-contract references added
- private-doctor smoke test passed against the local health workspace
- repo-level boundary validator implemented
- GitHub install reference docs added
- `scripts/generate_skill_install_manifest.py` implemented
- public repo and `v0.2.1` patch release published
- public-doc i18n gate converged and passes
- health roadmap, development plan, architecture, and capability map now target full health-agent V1 closure
- `health/` now has a stable umbrella suite entry plus `SKILLSET.json`
- `health-review`, `doctor-brief`, `health-reminders`, and `health-storage-feishu` implemented
- reply-contract validators now cover `health-review`, `doctor-brief`, `health-reminders`, and `health-storage-feishu`
- health reset playbook documented
- CLI acceptance covers install, archive, doctor dialogue, review, brief, reminders, and restore

## In Progress

- none

## Blockers / Open Decisions

- none

## Next 3 Actions
1. Keep health V1 stable while preparing any future optional enhancements.
2. Do not expand `order` until there is a real order-side delivery need.
3. Reopen the module only when a concrete post-V1 slice exists.
