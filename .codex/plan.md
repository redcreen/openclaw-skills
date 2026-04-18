# Project Plan

## Current Phase

Release-facing install routing and install-rehearsal prep.

## Current Execution Line

- Objective: bind the new GitHub-install contract to a real published repo/tag and verify that a clean install can be driven from one copy-paste URL per skill
- Plan Link: release/install rehearsal
- Runway: one checkpoint-sized execution line
- Progress: 0 / 4 tasks complete
- Stop Conditions:
  - the workspace remains unpublished and cannot provide a real GitHub owner/repo
  - the host installer contract changes away from GitHub tree URLs
  - the release process needs credentials or network steps outside this workspace
- Validation:
  - generated install URLs resolve to one skill folder each
  - published install docs prefer tag-based URLs over `main`
  - a clean install rehearsal succeeds from a copy-paste prompt

## Execution Tasks

- [ ] EL-1 decide the real GitHub owner/repo and first stable release tag
- [ ] EL-2 generate release-pinned install prompts for all current skills
- [ ] EL-3 run one clean install rehearsal from a GitHub URL
- [ ] EL-4 decide whether to wrap release tagging and manifest generation into one helper

## Development Log Capture

- Trigger Level: high
- Auto-Capture When:
  - a repo-level structure replaces a looser folder convention
  - a new shared contract is introduced for multiple skills
  - an architecture or documentation retrofit changes how maintainers add future skill sets
  - a tradeoff about cross-skill reuse is made explicit
- Skip When:
  - the work is purely copy-editing
  - a file change only mirrors already agreed structure
  - no durable reasoning changed

## Architecture Supervision
- Signal: `green`
- Signal Basis: the install contract is now explicit enough to move from documentation-only to publish-and-rehearse work
- Problem Class: distribution drift and weak install-entry consistency
- Root Cause Hypothesis: users were expected to browse repo paths manually, which does not scale to reusable public skills
- Correct Layer: generated per-skill install URLs, tag-first publish guidance, and a release rehearsal
- Rejected Shortcut: hand-writing install examples in each README without a reusable generator
- Automatic Review Trigger: a real remote/tag exists or a non-GitHub distribution path is proposed
- Escalation Gate: continue automatically

## Escalation Model

- Continue Automatically: repo topology, docs, and skill skeleton work stays within the agreed isolation direction
- Raise But Continue: documentation or module naming drifts, but the repo can still converge without product-level choices
- Require User Decision: installation UX, distribution model, or shared-layer design would materially change how skills are shipped

## Slices
- Slice: large-workspace retrofit baseline
  - Objective: define the repo as a multi-module workspace with isolated skill sets and clear public-doc routing
  - Dependencies: maintainer direction on isolation and documentation boundaries
  - Risks: a flat layout causes future domains to leak into each other
  - Validation: root README, architecture, roadmap, and control surface describe the same shape
  - Exit Condition: contributors can tell where a new skill set or skill should live without guessing

- Slice: health skill-set baseline
  - Objective: make `health/` a standalone skill-set root with its own index and first two installable skill folders
  - Dependencies: large-workspace retrofit baseline
  - Risks: health stays as a monolithic agent design instead of a reusable skill set
  - Validation: `health/README*.md`, `health/health-archive`, and `health/private-doctor` exist with independent skill artifacts
  - Exit Condition: `health` is ready for implementation work instead of structural debate

- Slice: health-archive implementation
  - Objective: implement the first local-first health archive workflow
  - Dependencies: health skill-set baseline
  - Risks: record state remains ambiguous or storage semantics drift
  - Validation: the skill can classify an image, save raw evidence, append a local record, and report explicit status
  - Exit Condition: users can trust whether a health image was archived

- Slice: private-doctor behavior implementation
  - Objective: implement concise family-doctor interpretation, advice, and planning on top of local health records
  - Dependencies: health skill-set baseline and at least a partial storage contract
  - Risks: the skill collapses into either a recorder or a verbose essay generator
  - Validation: the skill produces a stable short reply contract with interpretation and next steps
  - Exit Condition: the health set includes a usable doctor-style interaction path

- Slice: private-doctor reply refinement
  - Objective: turn the doctor summary output into repeatable user-visible reply patterns
  - Dependencies: private-doctor behavior implementation
  - Risks: the skill still varies too much in tone or archive-status wording
  - Validation: example replies stay concise, structured, and honest about record status
  - Exit Condition: the private-doctor layer is stable enough to use as the main health-facing interaction path

- Slice: isolation guardrails
  - Objective: add lightweight checks or review rules for cross-skill-set references
  - Dependencies: at least one active skill set and one future module placeholder
  - Risks: isolation exists only in prose
  - Validation: maintainers have a documented review rule or automated check for forbidden runtime reuse
  - Exit Condition: future modules can be added without repeating the same architecture debate

- Slice: release/install rehearsal
  - Objective: make published skills installable from one copy-paste GitHub URL per skill
  - Dependencies: skill-folder docs, install manifest generator, and a real repo/tag decision
  - Risks: install guidance stays template-only and never becomes a verifiable public flow
  - Validation: a release-pinned GitHub URL can be generated and used for a clean install
  - Exit Condition: the workspace can publish real install prompts instead of placeholders
