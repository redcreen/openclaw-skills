# Project Status

## Delivery Tier
- Tier: `large`
- Why this tier: the repo now needs module-aware governance for isolated skill sets and per-skill distribution docs
- Last reviewed: 2026-04-18

## Current Phase

GitHub-first install routing with a real repo binding and first stable tag.

## Active Slice

Real GitHub install prompts and first-release binding for installable skills.

## Current Execution Line

- Objective: bind the docs and install prompts to the real repository `redcreen/openclaw-skills`, publish the first stable tag, and keep skill-level isolation intact
- Plan Link: release-facing install routing
- Runway: one checkpoint-sized execution line
- Progress: 4 / 4 tasks complete
- Stop Conditions:
  - install support moves away from GitHub tree URLs
  - a host-specific installer contract replaces the current copy-paste chat entry model
  - multi-version manifest maintenance needs automation beyond the current generator

## Execution Tasks

- [x] EL-1 bind the public repository to `redcreen/openclaw-skills`
- [x] EL-2 publish the first stable install ref as `v0.1.0`
- [x] EL-3 replace placeholder install URLs with real copy-paste prompts
- [x] EL-4 push the release binding to GitHub

## Development Log Capture

- Trigger Level: high
- Pending Capture: no
- Last Entry: `docs/devlog/2026-04-18-github-install-release-binding.md`

## Architecture Supervision
- Signal: `green`
- Signal Basis: install routing is now bound to a real repo and first stable tag instead of staying template-only
- Root Cause Hypothesis: template-only docs leave the last mile undone, so users still cannot install from a real URL
- Correct Layer: real repo binding, real tag, public install docs, and the manifest generator
- Automatic Review Trigger: review again when a second public release or a non-GitHub install flow appears
- Escalation Gate: continue automatically

## Current Escalation State
- Current Gate: continue automatically
- Reason: the current work is still converging within the agreed local-first health direction
- Next Review Trigger: a future slice adds release automation or a non-GitHub distribution path

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
- root, `health`, and per-skill READMEs now expose copy-paste GitHub install templates
- public repo created at `https://github.com/redcreen/openclaw-skills`
- install docs now point to real `redcreen/openclaw-skills` URLs
- first stable install tag prepared as `v0.1.0`

## In Progress

- decide whether to add a one-command release/install rehearsal flow
- decide whether to commit a generated release manifest alongside each tag

## Blockers / Open Decisions

- decide whether release notes should carry generated install manifests directly
- decide whether to automate README/tag updates for future releases

## Next 3 Actions
1. Run a clean install rehearsal using the `v0.1.0` GitHub URLs.
2. Decide whether to add a one-command release helper that emits the manifest as part of tagging.
3. Decide whether future releases should commit a generated install manifest file.
