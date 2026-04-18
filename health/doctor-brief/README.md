[English](README.md) | [中文](README.zh-CN.md)

# Doctor Brief

`doctor-brief` is the clinician-facing summary layer in the `health` skill set. It turns the local health workspace into a compact brief that is easier for a doctor to scan quickly.

## What This Is

From a user point of view, `doctor-brief` solves a common appointment problem:

- you have many scattered health records
- you do not want to explain the whole history from memory
- you want the key trends, medication context, and symptom signals organized clearly

It is not the skill you use every day. It is the skill that becomes especially valuable before a visit.

## Why Install It

Its value is turning scattered records into a doctor-readable summary:

- no last-minute chat digging
- no manual timeline cleanup
- a better chance that the clinician sees the key recent signals quickly

## When To Use It

- before an in-person or remote appointment
- when you want a recent stage summary for a clinician
- when you want to condense weight, blood pressure, medication, and symptom context into one brief

## What You Should Expect Back

In most cases the output should include:

- a compact profile snapshot
- recent trend highlights
- current medication context
- recent symptom or signal summary
- questions or follow-up points worth bringing to the clinician

## How To Start The First Time

The easiest way to start is to ask for a recent-stage doctor brief.

Examples:

```text
Create a doctor brief for the last 30 days.
Summarize recent weight, blood pressure, medication, and symptoms into a doctor-facing version.
```

## Recommended Pairing

It works best together with:

- `health-archive`
- `private-doctor`
- `health-review`

That way the brief has enough archived records and review context to work from.

## Install

- install target: `health/doctor-brief/`
- required artifact: `SKILL.md`
- default external data root: `~/Documents/personal health`
- installation rule: allow the user to choose the data path and keep Feishu disabled by default

## GitHub Direct Install

- stable install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.2.1/health/doctor-brief`
- development install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/doctor-brief`

## Maintainer Runtime Pieces

- `SKILL.md`: clinician-brief behavior and reply contract
- `scripts/generate_doctor_brief.py`: generates clinician-readable briefs

## Usage Notes

- the brief must be grounded in local records rather than chat memory
- the point is readability for a clinician, not dumping raw data
- outputs are written into `reports/` by default
