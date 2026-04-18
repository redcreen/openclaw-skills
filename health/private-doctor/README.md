# Private Doctor

`private-doctor` is the interpretation and planning skill in the `health` set. It should sound like a concise family doctor that uses local health records, not like a passive recorder.

## Install

- install target: `health/private-doctor/`
- required artifact: `SKILL.md`
- default external data root: `~/document/personal health`
- installation rule: allow the user to choose the data path and keep Feishu disabled by default

## GitHub Direct Install

- stable install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.1.0/health/private-doctor`
- development install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/private-doctor`
- once the repository is published, maintainers can paste that URL directly into the OpenClaw chat.

## Runtime Pieces

- `SKILL.md`: doctor behavior and short reply contract
- `scripts/summarize_health_workspace.py`: deterministic summary of the local health workspace
- `scripts/render_doctor_reply.py`: render a stable doctor-style reply from the summary JSON
- `scripts/validate_doctor_reply.py`: lightweight validation for reply structure and archive-status honesty
- `scripts/update_health_profile.py`: append long-lived profile facts into `profile.md`
- `references/doctor-workflow.md`: doctor-facing operating flow
- `references/onboarding-profile.md`: profile-building guide
- `references/reply-contract.md`: user-visible reply shape

## Use When

- the user wants to build or update a health profile
- the user asks what recent measurements mean
- the user wants short advice or a follow-up plan

## Usage Notes

- replies should stay short but complete
- every reply should make record status visible when new facts arrived
- the skill should interpret and advise instead of acting like a clerk
- if this skill did not witness a successful archive write, it must mark record status as not verified
- published install docs should prefer a tag instead of `main`
