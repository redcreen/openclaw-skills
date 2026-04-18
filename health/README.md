[English](README.md) | [中文](README.zh-CN.md)

# Health Skill Set

This folder contains installable skills for personal health workflows. The set is local-first and keeps health data outside the repository.

## What This Suite Is

From a user point of view, `health` is not just a bundle of scripts. It is the beginning of a family-doctor workflow that should take over day-to-day health intake and follow-up dialogue.

In practical terms:

- you send weight, blood-pressure, exercise, symptom, or medication images and facts
- it records them and tells you whether they were really written
- then it continues like a family doctor: interpretation, reminders, advice, and next steps

The target is not a passive recorder. The target is a long-term health companion that keeps your health context alive across time.

## Why Install It

This suite is meant for users who currently feel one or more of these pains:

- you send a health image but do not know whether it was actually recorded
- health data stays scattered across chats and becomes hard to review
- you want trend-based follow-up, not one-shot answers
- you want weight, blood pressure, exercise, sleep, symptoms, and medication context on one health timeline
- you want reviews, clinician briefs, and reminders later without rebuilding everything from scratch

## Who It Is For

- people managing weight, blood pressure, lipid risk, or glucose risk over time
- people actively changing diet, exercise, sleep, or medication habits and wanting follow-up
- people who want recording, interpretation, advice, and review in one connected workflow

## Who It Is Not For

- emergency or urgent triage
- replacing a clinician's diagnosis or prescription decisions
- highly specialized first-version medical scenarios outside the current scope

## How You Will Use It

The intended user flow is:

1. install the `health` capability
2. build a baseline profile with goals, background, and medication context
3. send daily health images or facts
4. let the suite record first, then continue the doctor-style dialogue on top of those records
5. later add weekly reviews, stage summaries, clinician briefs, and reminders

## What You Can Do Right After Installing Today

The current baseline already supports:

- local-first archive with explicit record status
- concise family-doctor interpretation on top of the local health workspace
- ongoing profile building instead of restarting from zero every time

The roadmap has already locked the next layers:

- one-command install for the full `health` suite
- more complete proactive onboarding and baseline three-high assessment
- daily, weekly, and monthly reviews
- clinician-readable briefs
- reminder capability
- CLI-first full-suite acceptance

## How To Start The First Time

The most natural first session is:

1. tell it your age, height, current goals, three-high background, and medication context
2. or just send the first weight or blood-pressure image
3. ask it to record the item and tell you what it means

Typical examples:

```text
This is my weight image from this morning. Record it and tell me the recent trend.
This is today's blood pressure image. Record it and tell me what I should watch today.
Build my health profile: 44 years old, 178 cm, mainly trying to control weight and blood pressure.
```

## What Daily Dialogue Should Feel Like

The desired interaction is not:

- you send an image
- it replies only with “recorded”

It should instead do three things:

- clearly show record status
- give the doctor view
- give one short advice or next step

That means the user-facing shape should stay close to:

- `Record Status`
- `Doctor View`
- `Advice / Plan`

## Recommended Install Shape Right Now

If you want to start today:

- install at least:
  - `health-archive`
  - `private-doctor`

If your first problem is simply “did the image really get recorded?”:

- start with `health-archive`

If you want the family-doctor experience:

- start with `health-archive + private-doctor`

The roadmap does not turn `health/` into one fake monolithic skill. Instead, it aims to provide a one-command flow that installs the full `health` suite together.

## Rules For This Skill Set

- keep all runtime behavior inside `health/`
- do not mix order or other non-health business logic into this set
- install individual skills, not the whole folder as one hidden monolith
- default external data root is `~/document/personal health`, but installation must let the user override it
- Feishu is disabled by default in V1

## Skills

| Skill | Role | Install Path | Use When | Notes |
| --- | --- | --- | --- | --- |
| [`health-archive`](health-archive/README.md) | Archive measurements, screenshots, and health facts into local records with explicit success status | `health/health-archive/` | the user sends weight, blood pressure, exercise, sleep, symptom, or other health evidence that should be recorded | first functional delivery target |
| [`private-doctor`](private-doctor/README.md) | Act like a concise family doctor that interprets, advises, and plans from local health records | `health/private-doctor/` | the user wants onboarding, explanation, trend review, advice, or follow-up planning | must not degrade into recorder-only behavior |
| [`health-review`](health-review/README.md) | Generate daily, weekly, and monthly reviews plus trend summaries | `health/health-review/` | the user wants periodic follow-up instead of only one-shot interpretation | writes into `reviews/` |
| [`doctor-brief`](doctor-brief/README.md) | Generate clinician-readable briefs and stage summaries | `health/doctor-brief/` | the user wants a doctor-facing summary before a visit | writes into `reports/` |
| [`health-reminders`](health-reminders/README.md) | Manage recurring reminder rules and due-reminder checks | `health/health-reminders/` | the user wants measurement, medication, exercise, or review reminders | writes into `reminders/` |
| [`health-storage-feishu`](health-storage-feishu/README.md) | Export and restore portable health-workspace bundles for optional backup or mirror workflows | `health/health-storage-feishu/` | the user wants backup or restore readiness before reset | current focus is local bundle export and restore |

## Health Suite Install Target

- the roadmap does not turn `health/` into one fake monolithic skill
- the target is a one-command install flow that installs multiple health skills together
- the default suite target includes:
  - `health-archive`
  - `private-doctor`
  - `health-review`
  - `doctor-brief`
  - `health-reminders`
  - `health-storage-feishu`
- Feishu-related storage stays optional and does not block health V1
- see the detailed closure table here:
  - [Health capability map](../docs/reference/openclaw-skills/health-capability-map.md)

## Data and Privacy

- the default data root is `~/document/personal health`
- health data lives locally by default and does not require Feishu to work
- Feishu is not the V1 source of truth; it stays a future optional backup or mirror path
- this is why backup-before-reset and restore-after-reset are explicitly part of the roadmap

## GitHub Direct Install Templates

After publishing, you can send either the full-suite install URL or the exact single-skill URL.

- full `health` suite install
  - `Install skill suite: https://github.com/redcreen/openclaw-skills/tree/main/health`

- `health-archive`
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-archive`
- `private-doctor`
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/private-doctor`
- `health-review`
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-review`
- `doctor-brief`
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/doctor-brief`
- `health-reminders`
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-reminders`
- `health-storage-feishu`
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-storage-feishu`
- maintainer batch generation:
  - `python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref main --domain health`

## Data Root

The default external data root for this skill set is `~/document/personal health`.

Recommended structure:

```text
~/document/personal health/
  profile.md
  records.md
  raw/
  reviews/
  reports/
```
