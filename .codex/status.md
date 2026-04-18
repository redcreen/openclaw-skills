# Project Status

## Delivery Tier
- Tier: `large`
- Why this tier: the repo now has to carry a full health-agent replacement roadmap, staged skill delivery, release packaging, and CLI-first acceptance
- Last reviewed: 2026-04-18

## Current Phase

Health full-capability planning retrofit complete; Stage 3 implementation ready.

## Active Slice

Health suite install and doctor-core completion.

## Current Execution Line

- Objective: implement one-command suite install, onboarding, initial assessment, and archive-to-doctor continuity for the `health` skill set
- Plan Link: health suite install and doctor-core completion
- Runway: one checkpoint-sized execution line
- Progress: 0 / 6 tasks complete
- Stop Conditions:
  - suite install needs host support outside the current GitHub + skill-installer model
  - the medical scope expands beyond the agreed health-agent V1 boundary
  - migration/reset expectations require product decisions outside this repo

## Execution Tasks

- [ ] EL-1 define and implement the one-command `health` suite install flow
- [ ] EL-2 expand the baseline health profile schema for onboarding and three-high context
- [ ] EL-3 add initial risk framing and first-phase planning to `private-doctor`
- [ ] EL-4 verify image-or-fact archive -> doctor dialogue through CLI
- [ ] EL-5 decide whether archive needs a multi-image single-session helper
- [ ] EL-6 refresh release-facing docs and manifests for the suite-install entry

## Development Log Capture

- Trigger Level: high
- Pending Capture: no
- Last Entry: `docs/devlog/2026-04-18-health-full-capability-planning-retrofit.md`

## Architecture Supervision
- Signal: `green`
- Signal Basis: the roadmap now closes against real health-agent capability, not only repo structure or release wiring
- Root Cause Hypothesis: the earlier roadmap over-focused on baseline infrastructure and under-specified how to close onboarding, reviews, reminders, and CLI acceptance
- Correct Layer: roadmap, development plan, module planning, and capability mapping
- Automatic Review Trigger: review again when a new health skill is added or the suite-install contract changes
- Escalation Gate: continue automatically

## Current Escalation State
- Current Gate: continue automatically
- Reason: the planning surface now matches the intended health-agent V1 target and is ready for direct implementation
- Next Review Trigger: a future slice changes the install model, medical scope, or migration expectations

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
- public repo and `v0.1.0` release published
- public-doc i18n gate converged and passes
- health roadmap, development plan, architecture, and capability map now target full health-agent V1 closure

## In Progress

- Stage 3 implementation has been defined but not started
- suite-install packaging and CLI acceptance design still need code

## Blockers / Open Decisions

- choose the exact one-command suite-install surface: bundle manifest, helper script, or both
- decide how much of Feishu backup/export belongs in Stage 5 versus a later optional adapter release

## Next 3 Actions
1. Implement the one-command `health` suite install flow.
2. Expand `private-doctor` onboarding and initial assessment around the health V1 profile schema.
3. Add a CLI scenario that proves image archive -> doctor dialogue without user manual QA.
