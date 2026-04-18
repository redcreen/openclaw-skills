[English](README.md) | [中文](README.zh-CN.md)

# Health Archive

`health-archive` is the intake skill for local-first health records. It archives incoming measurements and health evidence into the user's external health data folder and returns explicit archive status.

## What This Is

From a user point of view, `health-archive` is the layer that answers the basic trust question:

- you sent a health image
- did it really get recorded
- what exactly was extracted
- where was it saved

If `private-doctor` is the family-doctor layer, `health-archive` is the trustworthy intake and record layer behind it.

## Why Install It

Its main value is not long-form analysis. Its main value is trustworthy recording:

- it tells you whether something was truly archived
- it backs up the raw evidence instead of only reading numbers from the image
- later doctor dialogue can depend on real local records instead of chat memory alone

If your first pain is “I send health images and still do not trust whether they were recorded,” this is the first skill to install.

## When To Use It

Typical cases:

- weight images
- blood-pressure images
- exercise screenshots
- sleep, symptom, or medication evidence
- any moment when you want to verify whether an item was actually written

## What You Should Expect Back

The intended reply should not stop at “recorded”.

It should at least make these things visible:

- `Record Status`
- the key facts that were extracted
- where they were saved
- one compact doctor interpretation

So the first job is “did it really get stored”, and only then “what does this roughly mean”.

## How To Start The First Time

The simplest way to start is to send one image naturally.

Examples:

```text
This is my weight image from this morning.
This is today's blood-pressure image.
This is my exercise screenshot for today.
```

## What It Does Not Replace

`health-archive` is about recording, not full doctor follow-up.

It does not replace:

- long-term trend interpretation
- full family-doctor advice
- weekly or monthly review
- clinician-facing briefs

Those are handled by `private-doctor` and the other installed health skills.

## Recommended Pairing

If you only want to solve “did the image really get recorded?”, this skill alone is enough to start.

If you want the full family-doctor experience, install at least:

- `health-archive`
- `private-doctor`

## Install

- install target: `health/health-archive/`
- required artifact: `SKILL.md`
- default external data root: `~/Documents/personal health`
- installation rule: let the user choose the data path; do not hardcode a personal path

## GitHub Direct Install

- stable install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.2.1/health/health-archive`
- development install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-archive`
- once the repository is published, maintainers can paste that URL directly into the OpenClaw chat.

## Maintainer Runtime Pieces

- `SKILL.md`: archive behavior and reply contract
- `scripts/archive_health_record.py`: deterministic local write path
- `scripts/archive_health_session.py`: archives multiple health entries in one session
- `references/archive-format.md`: storage contract and payload schema
- `references/field-map.md`: normalized field names

## Script Example

```bash
python3 skills/health-archive/scripts/archive_health_record.py --payload-file artifacts/health-archive-payload.json
```

## Usage Notes

- local files are the source of truth
- raw evidence should be backed up before claiming success
- the script writes `records.md`, `raw/YYYY/MM/DD/`, and `archive-log.jsonl`
- Feishu stays disabled by default
- uncertain health evidence should still be saved with an honest type such as `unknown-health`
- when the user sends multiple images or multiple facts together, the session-archive script is the right path
- published install docs should prefer a tag instead of `main`
