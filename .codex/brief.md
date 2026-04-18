# Project Brief

## Delivery Tier
- Tier: `large`
- Why this tier: the repo is evolving into a multi-skill workspace with first-class skill sets such as `health` and `order`, each containing independently installable skills and separate documentation surfaces
- Last reviewed: 2026-04-18

## Outcome

Build and maintain a repository of OpenClaw skills where:

- each top-level skill-set folder is isolated from the others
- each individual skill remains independently installable and runnable
- the root README acts as an index for all skill sets and skills
- each skill set and each skill has its own focused README pair
- published skills can be installed from one copy-paste GitHub URL per skill

## Scope

- define the repository shape for multiple isolated skill sets
- keep `health` and future sets such as `order` separated at the folder, doc, and runtime boundary
- provide a durable documentation stack for install, usage, architecture, roadmap, and validation
- scaffold the first `health` skill set with reusable, user-installable skills
- make GitHub tree URLs the standard public install entry for each skill

## Non-Goals

- building a shared runtime layer by quietly reusing code from sibling skill folders
- mixing domain-specific health and order logic in one skill set
- making Feishu the primary storage path for health in V1
- using `.codex` files as a replacement for the repository's public docs

## Constraints

- each skill set owns its own skill folders and README surface
- each skill folder must include a `SKILL.md` and remain independently usable
- skills must not import, call, or load runtime assets from sibling skill folders or sibling skill sets
- repository docs must use repository-relative links
- health data defaults to `~/document/personal health`, but installation must allow the user to override the path
- Feishu support stays disabled by default and may return later only as an optional storage adapter

## Definition of Done

- the repo is classified and documented as a multi-skill, multi-skill-set workspace
- the root README pair works as an index with role, install path, and usage notes for each available skill
- `health/` exists as an isolated skill-set root with its own landing README pair
- `health/health-archive` and `health/private-doctor` exist as standard skill folders with `SKILL.md`, UI metadata, and per-skill README pairs
- durable docs explain the top-level skill-set boundary, roadmap, development plan, and validation policy
- maintainers can generate release-pinned GitHub install prompts for each installable skill
