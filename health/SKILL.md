---
name: health
description: Installable umbrella skill for the full local-first health suite. Use when the user wants one entry point that can archive health images or facts, build a health profile, continue family-doctor dialogue, generate reviews and clinician briefs, manage reminders, and back up or restore the health workspace.
---

# Health Suite

## Overview

This skill is the suite-level entry for the `health/` module. It gives the agent one install target for the full family-doctor workflow while keeping the underlying runtime split across focused health skills inside the same folder.

## Use This Skill When

- the user installs the full `health` capability from one GitHub URL
- the user wants one health entry point instead of picking sub-skills manually
- the user sends health images or facts and expects archive plus doctor-style dialogue in the same flow
- the user later wants reviews, clinician briefs, reminders, or backup without reinstalling more skills

## Working Contract

- default external data root: `~/document/personal health`
- local files remain the source of truth
- runtime behavior stays inside `health/`
- do not mix order or other non-health domain logic into this suite
- Feishu remains optional and disabled by default

## Internal Routing

Route tasks to the bundled health sub-skills without exposing unnecessary engineering detail to the user:

- archive incoming images or facts with `health-archive/`
- interpret, advise, and maintain long-lived profile context with `private-doctor/`
- generate daily, weekly, or monthly follow-up with `health-review/`
- generate clinician-readable summaries with `doctor-brief/`
- manage recurring reminders and due checks with `health-reminders/`
- export or restore backup bundles with `health-storage-feishu/`

The suite entry may call scripts from these bundled folders because they ship together under the same installed `health/` tree. It must not reach outside the `health/` module boundary.

## Default Reply Shape

When new health evidence arrives, keep the user-visible structure short and stable:

- `Record Status`
- `Doctor View`
- `Advice`
- `Plan` when a follow-up step matters

When the request is about reviews, briefs, reminders, or backup, keep the reply factual and explicit about what was written and where.

## Non-Goals

- emergency triage
- replacing clinician diagnosis or prescription decisions
- pretending a remote sync happened when only local archive or export succeeded
