[English](README.md) | [中文](README.zh-CN.md)

# Health Reminders

`health-reminders` is the reminder-contract layer in the `health` skill set. It manages what should be reminded, when it should be reminded, and whether a reminder is due right now.

## What This Is

From a user point of view, it answers questions like:

- when should I measure weight or blood pressure
- when should I log medication context
- when should I review the day or the week
- what reminder should fire right now if a scheduler is connected later

It is not the chat layer itself. It is the local reminder rule layer behind that experience.

## Why Install It

Without a reminder layer, health follow-up often becomes:

- measure only when remembered
- log only when convenient
- realize a week later that the routine drifted

`health-reminders` turns “what should be reminded” into a saved, checkable, automation-friendly local contract.

## When To Use It

- when you want a recurring morning weight reminder
- when you want a blood-pressure recheck reminder
- when you want exercise or review reminders
- when you want the system to answer “what is due right now?”

## What You Should Expect Back

In most cases the output should show:

- the active reminder rules
- which reminder is due now
- why it is due
- what to do next

## How To Start The First Time

The easiest start is to set one or two fixed reminders.

Examples:

```text
Remind me every morning at 8:00 to measure weight.
Remind me every evening at 21:00 to review the day's health records.
```

## Recommended Pairing

Reminders become much more useful when they work together with:

- `health-archive`
- `private-doctor`
- `health-review`

That way the reminder can flow into recording, interpretation, and review instead of stopping at the reminder itself.

## Install

- install target: `health/health-reminders/`
- required artifact: `SKILL.md`
- default external data root: `~/Documents/personal health`
- installation rule: allow the user to choose the data path and keep Feishu disabled by default

## GitHub Direct Install

- stable install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.2.1/health/health-reminders`
- development install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-reminders`

## Maintainer Runtime Pieces

- `SKILL.md`: reminder rules and reply contract
- `scripts/health_reminders.py`: manages reminder rules and evaluates due reminders

## Usage Notes

- it handles reminder rules and due-checks, not a full transport or delivery system
- a real push channel can be added later, but the reminder contract should exist locally first
- outputs are written into `reminders/` by default
