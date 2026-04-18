---
name: health-reminders
description: Manage and evaluate local-first health reminder rules. Use when the user wants recurring measurement, medication, exercise, or review reminders, and when an external scheduler needs a due-reminder check against the local health workspace.
---

# Health Reminders

## Overview

This skill manages reminder rules for the `health` skill set. It does not replace the chat skills; it gives them a local reminder contract and due-reminder evaluation path.

## Use This Skill When

- the user wants fixed health reminders
- the user wants medication or measurement reminders tracked locally
- an external scheduler or automation needs to know which reminders are due now

## Working Contract

- default external data root: `~/Documents/personal health`
- write reminder rules into `reminders/`
- evaluate due reminders against the local health workspace
- keep Feishu disabled by default

## Scripted Reminder Path

1. Upsert reminder rules:

   ```bash
   python3 skills/health-reminders/scripts/health_reminders.py upsert --payload-file /tmp/health-reminders.json
   ```

2. Check due reminders:

   ```bash
   python3 skills/health-reminders/scripts/health_reminders.py due --at 2026-04-18T08:00:00+08:00
   ```

3. Use the script result as the source of truth for:
   - active reminder rules
   - due reminders right now
   - saved reminder-plan path

## Reply Contract

Every reminder reply should make these things visible:

- `Reminder Status`
- `What Is Due`
- `Why It Is Due`
- `What To Do Next`

Keep the reminder output brief, explicit, and actionable.
Do not omit the due reason or the next action when a reminder is currently due.

## Non-Goals

- replacing a full external scheduler
- pretending a reminder was delivered by a channel when only the due-check ran
- making Feishu the required reminder transport
