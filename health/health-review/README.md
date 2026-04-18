[English](README.md) | [中文](README.zh-CN.md)

# Health Review

`health-review` is the longitudinal review layer in the `health` skill set. It turns archived health records into daily, weekly, or stage-based reviews.

## What This Is

From a user point of view, `health-review` solves the problem of not wanting to look only at one reading at a time.

It is for moments like:

- you want to know how the week actually went
- you want to see whether things are improving or drifting
- you want a short review instead of manually reading back through chats

If `private-doctor` is the current family-doctor interpretation, `health-review` is the periodic follow-up summary.

## Why Install It

Its value is turning scattered records into trend conclusions:

- it looks beyond one isolated reading
- it helps you see the direction over several days or a week
- it makes later advice more continuous and grounded

## When To Use It

- when you want a short daily review
- when you want a weekly follow-up summary
- when you want a stage review
- when you want the local records turned into a compact review file

## What You Should Expect Back

In most cases the output should make these things visible:

- the review window
- the main change during that window
- what deserves attention
- what to focus on next

## How To Start The First Time

The easiest way to start is to ask for a weekly review.

Examples:

```text
Give me a review of the last week.
Summarize the last few days of weight, blood pressure, and exercise.
```

## Recommended Pairing

For reviews to mean anything, the local workspace should already have records from:

- `health-archive`
- `private-doctor`

## Install

- install target: `health/health-review/`
- required artifact: `SKILL.md`
- default external data root: `~/Documents/personal health`
- installation rule: allow the user to choose the data path and keep Feishu disabled by default

## GitHub Direct Install

- stable install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-review`
- development install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-review`

## Maintainer Runtime Pieces

- `SKILL.md`: review behavior and short reply contract
- `scripts/generate_health_review.py`: generates daily, weekly, and monthly reviews

## Usage Notes

- the review must be grounded in archived records rather than chat memory
- conclusions should stay trend-based and cautious
- review outputs are written into `reviews/` by default
