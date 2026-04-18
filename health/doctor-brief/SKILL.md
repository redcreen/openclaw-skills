---
name: doctor-brief
description: Generate clinician-readable health briefs from the local health workspace. Use when the user wants a concise doctor-facing summary before a visit, a stage report, or a structured brief built from archived records and profile facts.
---

# Doctor Brief

## Overview

This skill generates clinician-facing briefs from the local health workspace. It is the visit-preparation layer of the `health` skill set.

## Use This Skill When

- the user wants a concise doctor-facing summary
- the user is preparing for an appointment
- the user wants recent trends, medication context, and symptom signals organized into one brief

## Working Contract

- default external data root: `~/Documents/personal health`
- read the same local health workspace used by the other `health` skills
- write clinician-ready outputs into `reports/`
- keep Feishu disabled by default

## Scripted Brief Path

1. Decide the brief window:
   - recent stage
   - custom period
2. Run:

   ```bash
   python3 skills/doctor-brief/scripts/generate_doctor_brief.py --days 30 --save
   ```

3. Use the script result as the source of truth for:
   - patient snapshot
   - recent trend summary
   - medication context
   - follow-up questions
   - saved brief path

## Reply Contract

Every user-visible brief reply should include:

- `Brief Window`
- `Main Concerns`
- `Clinician Snapshot`
- `Saved To`

Keep the brief structured, clinically readable, and explicit about what was generated and where it was saved.
Do not collapse a generated brief result into a one-line answer when a saved brief path is available.

## Non-Goals

- real-time archiving
- reminder scheduling
- pretending the brief replaces a clinician visit
