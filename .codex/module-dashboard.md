# Module Dashboard

## Summary
- Overall: the repo remains a module-aware OpenClaw skill workspace, but the primary delivery target is now full health-agent capability closure through the `health` skill set
- Current Phase: `health V1 released`
- Active Module: `health`
- Main Risk: future post-release changes may drift from the released health-suite contract

## Modules
| Module | Status | Already Implemented | Remaining Steps | Completion Signal | Next Checkpoint |
| --- | --- | --- | --- | --- | --- |
| `health` | `done` | suite root plus umbrella install entry, `health-archive`, `private-doctor`, `health-review`, `doctor-brief`, `health-reminders`, `health-storage-feishu`, local-first workspace contract, reset playbook, CLI acceptance, and GitHub install/release docs | future optional experience or adapter improvements only | the full intended health-agent V1 is covered by modular skills and passes CLI-first acceptance | reopen only when a new post-V1 slice exists |
| `order` | `deferred` | module reserved in control surface and architecture docs | do not activate until health V1 closes | future-only | revisit after health V1 completion |
