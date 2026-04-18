[English](health-capability-map.md) | [中文](health-capability-map.zh-CN.md)

# Health Capability Map

This document maps the original health-agent intent onto the new skill-set architecture so the roadmap can close against real capability parity instead of only structural progress.

## Goal

- align the original health-agent expectations with the modular skill set
- make current status explicit: done, partial, or planned
- show which roadmap stage closes each capability

## Capability Table

| Capability | Target Surface | Current State | Target Stage | Acceptance |
| --- | --- | --- | --- | --- |
| One-command install for the full `health` suite | `health` suite install entry, without turning `health/` into one fake skill | Planned | Stage 3 | one command installs the required health skills from one GitHub tag |
| Proactive onboarding | `private-doctor` | Partial | Stage 3 | a CLI scenario completes onboarding, writes `profile.md`, and returns the first-phase plan |
| Baseline risk assessment for blood pressure / lipid / glucose context | `private-doctor` | Partial | Stage 3 | the initial doctor reply covers risk framing and immediate follow-up priorities |
| Automatic archive from images or health facts | `health-archive` | Baseline done | Stage 3 | an image or fact is written with verified archive status |
| Continue family-doctor dialogue after image archive | `health-archive` + `private-doctor` | Partial | Stage 3 | CLI proves archive -> doctor interpretation -> next-step reply |
| Ongoing family-doctor follow-up | `private-doctor` + `health-review` | Partial | Stage 4 | multi-day records produce trend-based follow-up and watchpoints |
| Daily / weekly / monthly review outputs | `health-review` | Planned | Stage 4 | local `reviews/` outputs are generated from archived records |
| Clinician-readable brief / stage report | `doctor-brief` | Planned | Stage 4 | local `reports/` outputs are generated in a clinician-friendly format |
| Reminder mechanism | `health-reminders` or an equivalent scheduling contract | Planned | Stage 5 | fixed reminders and lightweight fallback reminders both work |
| Backup and migration readiness before reset | reset/migration playbook + optional `health-storage-feishu` | Planned | Stage 5 | backup/export and restore preparation are documented and tested |
| Optional Feishu backup or mirror | `health-storage-feishu` | Planned, optional | Stage 5 | it works as mirror or backup only and does not block the local-first path |
| No manual user QA for the core flow | CLI acceptance chain | Planned | Stage 5 | install, archive, dialogue, review, brief, and reminder basics all pass from CLI |

## Current Assessment

The suite already has the minimum loop of archive plus basic family-doctor dialogue, but it is still missing three closure layers:

1. full-suite installation and reset-ready recovery
2. longitudinal review and clinician brief outputs
3. reminders plus CLI-first full acceptance

The roadmap should therefore close only when the table above has reached `done` or `done / optional`.
