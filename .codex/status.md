# Project Status

## Delivery Tier
- Tier: `large`
- Why this tier: the repo now needs module-aware governance for isolated skill sets and per-skill distribution docs
- Last reviewed: 2026-04-18

## Current Phase

GitHub-first install routing and release-prep docs on top of the local-first health workspace.

## Active Slice

Copy-paste GitHub install manifests and public install docs for installable skills.

## Current Execution Line

- Objective: make every installable skill advertise a stable GitHub tree URL and OpenClaw-ready install prompt, while keeping tag-first release guidance and skill-level isolation intact
- Plan Link: release-facing install routing
- Runway: one checkpoint-sized execution line
- Progress: 4 / 4 tasks complete
- Stop Conditions:
  - the workspace gains a real GitHub remote and needs release-pinned install manifests
  - install support moves away from GitHub tree URLs
  - a host-specific installer contract replaces the current copy-paste chat entry model

## Execution Tasks

- [x] EL-1 define the GitHub URL shape to use for per-skill install entry points
- [x] EL-2 add a deterministic manifest generator for installable skills
- [x] EL-3 update root, skill-set, and per-skill docs with copy-paste install patterns
- [x] EL-4 add reference and validation coverage for the new install-routing contract

## Development Log Capture

- Trigger Level: high
- Pending Capture: no
- Last Entry: `docs/devlog/2026-04-18-github-install-routing.md`

## Architecture Supervision
- Signal: `green`
- Signal Basis: install routing now converges on one per-skill GitHub URL contract instead of leaving distribution to ad hoc README guidance
- Root Cause Hypothesis: asking users to browse the repo manually weakens install consistency and makes skill-level isolation easy to violate
- Correct Layer: public install docs, a deterministic manifest generator, and tag-first release guidance
- Automatic Review Trigger: review again when the workspace gets a real GitHub remote or a host-native installer flow
- Escalation Gate: continue automatically

## Current Escalation State
- Current Gate: continue automatically
- Reason: the current work is still converging within the agreed local-first health direction
- Next Review Trigger: a future slice binds the docs to a real GitHub repo, release tag, or host install flow

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

## In Progress

- decide the real GitHub owner/repo and first release tag
- decide whether to add a one-command release/install rehearsal flow

## Blockers / Open Decisions

- this workspace still has no bound GitHub remote, so public install URLs remain template-driven
- decide whether release notes should carry generated install manifests directly

## Next 3 Actions
1. Bind the install docs to a real GitHub owner/repo and release tag.
2. Run a clean install rehearsal using the generated per-skill GitHub URLs.
3. Decide whether to add a one-command release helper that emits the manifest as part of tagging.
