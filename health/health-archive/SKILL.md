---
name: health-archive
description: Archive personal health images and measurements into a local health workspace. Use when the user sends weight, blood pressure, exercise, sleep, symptom, or other health evidence that should be identified, backed up, and recorded with explicit success or failure status.
---

# Health Archive

## Overview

This skill turns incoming health evidence into explicit local records. It is the storage-first intake layer for the `health` skill set.

## Use This Skill When

- the user sends a health-related image or screenshot
- the user provides weight, blood pressure, pulse, exercise, sleep, symptom, or medication facts that should be archived
- the user asks whether something was truly recorded
- the user sends a likely health image without telling you how to categorize it

## Storage Contract

- default external data root: `~/Documents/personal health`
- allow the user to override the path during installation
- store user data outside the repository
- use local files as the source of truth
- keep Feishu disabled unless a future optional adapter is explicitly enabled

Recommended files and folders:

```text
~/Documents/personal health/
  profile.md
  records.md
  archive-log.jsonl
  raw/YYYY/MM/DD/
```

Read [references/archive-format.md](references/archive-format.md) before writing archive payloads.
Read [references/field-map.md](references/field-map.md) when normalizing extracted fields.

## Scripted Archive Path

1. Decide whether the input contains archive-worthy health information.
2. Identify the evidence type.
3. Extract the key fields that are clear enough to record.
4. Build a JSON payload for `scripts/archive_health_record.py`.
5. Run:

   ```bash
   python3 scripts/archive_health_record.py --payload-file ./health-archive-payload.json
   ```

6. Use the script result as the only source of truth for user-visible status.

When a single user message contains multiple archive-worthy items, use:

```bash
python3 scripts/archive_health_session.py --payload-file ./health-archive-session.json
```

## Payload Minimum

Every archive payload should include:

- `entry_type`
- `recorded_on`
- `fields`
- `sources` when files are present

Optional fields:

- `recorded_at`
- `notes`
- `doctor_note`
- `profile_updates`
- `data_root`

## Evidence Types

- `weight`
- `blood-pressure`
- `exercise-walk`
- `exercise-run`
- `exercise-swim`
- `sleep`
- `symptom`
- `medication`
- `unknown-health`

If the evidence is clearly health-related but the subtype is uncertain, archive it as `unknown-health` instead of pretending the classification is certain.

## Reply Contract

Every archive reply must include:

- `Status`: `archived`, `partially archived`, or `not archived`
- `Recorded`: the normalized facts that were written
- `Saved To`: the local file path or logical location that was updated
- `Doctor Note`: one short interpretation line when the data supports it

Never say something was archived unless `scripts/archive_health_record.py` returned success.

If archive succeeds and the current interaction is clearly a health-management conversation, do not stop at storage acknowledgment alone. Continue with one short doctor-facing interpretation or hand the turn forward to the family-doctor layer in the same reply.

## Follow-Up Rules

Ask a follow-up only when one of these blocks correct archiving:

- the date is unclear
- the reading is not legible enough
- the same day has multiple conflicting groups and the new evidence cannot be placed safely
- the user explicitly asks not to store the item

Otherwise, archive first and keep the reply short.

If the user looks like a first-time or non-expert user:

- default to helping, not teaching prompt syntax
- after successful archive, continue with one short interpretation
- let the doctor layer ask only the next highest-value onboarding questions when needed

## Non-Goals

- long-form coaching
- pretending local archive success based on recognition alone
- making Feishu or another external system the required write path
