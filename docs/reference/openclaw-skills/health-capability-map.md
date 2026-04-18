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
| One-command install for the full `health` suite | `health/` suite entry plus `SKILLSET.json` | Done | Stage 3 | one stable GitHub URL installs the suite entry, and hosts with suite-manifest support can expand it into nested skills |
| Proactive onboarding | `private-doctor` | Done | Stage 3 | a CLI scenario completes onboarding, writes `profile.md`, and returns the first-phase plan |
| Baseline risk assessment for blood pressure / lipid / glucose context | `private-doctor` | Done | Stage 3 | the initial doctor reply covers risk framing and immediate follow-up priorities |
| Automatic archive from images or health facts | `health-archive` | Done | Stage 3 | an image or fact is written with verified archive status |
| Continue family-doctor dialogue after image archive | `health-archive` + `private-doctor` | Done | Stage 3 | CLI proves archive -> doctor interpretation -> next-step reply |
| Ongoing family-doctor follow-up | `private-doctor` + `health-review` | Done | Stage 4 | multi-day records produce trend-based follow-up and watchpoints |
| Daily / weekly / monthly review outputs | `health-review` | Done | Stage 4 | local `reviews/` outputs are generated from archived records |
| Clinician-readable brief / stage report | `doctor-brief` | Done | Stage 4 | local `reports/` outputs are generated in a clinician-friendly format |
| Reminder mechanism | `health-reminders` | Done | Stage 5 | fixed reminders and lightweight fallback reminders both work |
| Backup and migration readiness before reset | reset/migration playbook + bundle export/restore | Done | Stage 5 | backup/export and restore preparation are documented and tested |
| Optional Feishu backup or mirror | `health-storage-feishu` | Done / optional | Stage 5 | it works as a backup bundle layer and leaves the door open for future mirror adapters without blocking the local-first path |
| No manual user QA for the core flow | CLI acceptance chain | Done | Stage 5 | install, archive, dialogue, review, brief, reminder, and restore basics all pass from CLI |

## Current Assessment

The intended health-agent V1 is now covered by the modular suite. Future work can still deepen optional Feishu adapters or improve the user experience, but the baseline replacement path no longer depends on the old monolithic health agent.
