[English](README.md) | [中文](README.zh-CN.md)

# Private Doctor

`private-doctor` is the interpretation and planning skill in the `health` set. It should sound like a concise family doctor that uses local health records, not like a passive recorder.

## What This Is

From a user point of view, `private-doctor` is the layer that keeps talking like a family doctor after the data exists.

Its job is not only to repeat numbers. Its job is to:

- build the baseline profile with you
- interpret recent records in context
- show what matters most right now
- give one short advice or next step

If `health-archive` answers “did it really get recorded?”, `private-doctor` answers “what does it mean now?”

## Why Install It

Many health assistants fail in one of three ways:

- they record but do not interpret
- they interpret with long exhausting replies
- they speak as if every session starts from zero

`private-doctor` is meant to close those gaps:

- replies stay short but still useful
- the tone stays closer to a family doctor than to a clerk
- the dialogue can build on the local health workspace over time

## When To Use It

Typical cases:

- building the health profile for the first time
- asking what recent weight, blood pressure, or exercise data means
- wanting a short practical suggestion
- wanting to know what to watch next
- continuing the conversation after a new health image or fact was archived

## What The Reply Should Feel Like

The intended reply should stay stable rather than swinging between one-line logging and long essays.

In most cases it should make these things visible:

- `Record Status`
- `Doctor View`
- `Advice`
- `Plan`

The point is not to produce a long lecture. The point is to help the user quickly understand:

- whether the data is worrying or not
- what deserves attention next
- what to do today or over the next few days

## How To Start The First Time

The best first session is one of these:

1. build the profile directly
2. ask for interpretation right after a new health record

Examples:

```text
Build my health profile: 44 years old, 178 cm, mainly trying to control weight and blood pressure.
This is today's blood-pressure image. Record it and tell me what it means.
My weight has been dropping over the last few days. Help me understand whether the trend looks reasonable.
```

## What It Does Not Replace

`private-doctor` is not an emergency doctor and not a prescription replacement layer.

It does not:

- replace a clinician's diagnosis
- casually tell you to stop, reduce, or change medication
- overreact to one single reading

It is best used for the long-term “interpret, remind, and plan” layer of health management.

## Recommended Pairing

If you install only `private-doctor`, it can still read existing local records and interpret them.

But if you want the full experience, install at least:

- `health-archive`
- `private-doctor`

That way a health image can be archived first and then immediately continue into family-doctor dialogue.

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

## Maintainer Runtime Pieces

- `SKILL.md`: doctor behavior and short reply contract
- `scripts/summarize_health_workspace.py`: deterministic summary of the local health workspace
- `scripts/assess_health_profile.py`: baseline onboarding assessment and first-phase planning
- `scripts/render_doctor_reply.py`: render a stable doctor-style reply from the summary JSON
- `scripts/validate_doctor_reply.py`: lightweight validation for reply structure and archive-status honesty
- `scripts/update_health_profile.py`: append long-lived profile facts into `profile.md`
- `references/doctor-workflow.md`: doctor-facing operating flow
- `references/onboarding-profile.md`: profile-building guide
- `references/reply-contract.md`: user-visible reply shape

## Usage Notes

- replies should stay short but complete
- every reply should make record status visible when new facts arrived
- the skill should interpret and advise instead of acting like a clerk
- if this skill did not witness a successful archive write, it must mark record status as not verified
- onboarding flows should use the baseline assessment script instead of asking profile questions without returning an initial view
- published install docs should prefer a tag instead of `main`
