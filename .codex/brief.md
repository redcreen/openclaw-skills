# Project Brief

## Delivery Tier
- Tier: `large`
- Why this tier: the repo is not only a multi-skill workspace but also the delivery vehicle for a full health-agent replacement, with staged capability closure, release distribution, and CLI-first acceptance
- Last reviewed: 2026-04-18

## Outcome

Build and maintain an OpenClaw skill repository where:

- each top-level skill-set folder stays isolated from the others
- the `health` set closes the intended health-agent V1 capability as a modular family-doctor suite
- the full `health` suite can be installed from GitHub in one command after the old agent is reset
- after installation, the agent can archive health images and continue doctor-style dialogue on top of those records
- release readiness is proven by CLI acceptance, not by asking the user to do the foundational testing manually

## Scope

- keep the repository shape for multiple isolated skill sets
- finish `health` as the primary active module before expanding `order`
- deliver the `health` suite as a local-first family-doctor workflow:
  - archive
  - onboarding and baseline assessment
  - ongoing interpretation
  - review and reports
  - reminders
  - reset and migration readiness
- preserve GitHub-based distribution for both single-skill install and full-suite install

## Non-Goals

- turning `health/` into one fake monolithic skill
- making Feishu the primary storage path for health in V1
- mixing health and order runtime logic
- using `.codex` files as a replacement for the repository's public docs
- asking the user to manually verify the core install/archive/dialogue flow before CLI acceptance exists

## Constraints

- each skill set owns its own skill folders and README surface
- each skill folder must include a `SKILL.md` and remain independently usable
- suite install must install multiple skill folders together without collapsing runtime boundaries
- skills must not import, call, or load runtime assets from sibling skill folders or sibling skill sets
- repository docs must use repository-relative links
- health data defaults to `~/document/personal health`, but installation must allow the user to override the path
- Feishu support stays disabled by default and may return later only as an optional backup or mirror adapter
- medical advice must stay cautious and must not replace clinician diagnosis or prescription decisions

## Definition of Done

- the repo remains documented as a multi-skill, multi-skill-set workspace
- the `health` roadmap closes with a modular replacement for the intended health-agent V1
- one command can install the full `health` suite from a stable GitHub release
- the full `health` suite covers:
  - verified archive from health images or facts
  - proactive onboarding and baseline assessment
  - ongoing family-doctor dialogue
  - longitudinal review outputs
  - clinician-readable briefs
  - reminder capability
- reset or migration from the old health agent is documented and testable
- CLI acceptance proves install, archive, dialogue, review, brief, and reminder basics
