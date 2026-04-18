# Module Dashboard

## Summary
- Overall: the repo is being upgraded into a module-aware OpenClaw skill workspace where each top-level folder represents an isolated skill set
- Current Phase: `GitHub-first install routing` and release-prep
- Active Module: `health`
- Main Risk: future domains may still try to share runtime helpers or blur install/document boundaries

## Modules
| Module | Status | Already Implemented | Remaining Steps | Completion Signal | Next Checkpoint |
| --- | --- | --- | --- | --- | --- |
| `health` | `active` | skill-set root, landing README pair, `health-archive` archive path, `private-doctor` summary/profile/reply scripts, workflow refs, smoke-tested local read/write path, GitHub install templates | bind docs to a real repo/tag, run install rehearsal, decide whether more machine-readable profile storage is needed, decide on multi-image archive helper | archive, doctor, and install-template baseline complete | generate release-pinned install URLs and verify one clean install |
| `order` | `planned` | module reserved in control surface and architecture docs | create `order/` root, module README pair, first installable order skill | planned next | decide the first `order` skill and its isolation rules |
