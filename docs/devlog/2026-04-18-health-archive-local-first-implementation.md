# 2026-04-18 Health Archive Local-First Implementation

## Problem

The `health-archive` skill existed only as a structural placeholder. That did not solve the user's main trust problem:

- after sending an image, the user must know whether the record was really written
- the skill cannot rely on conversational wording such as "recorded" without a durable write result
- health evidence needs both a human-readable archive and a machine-checkable journal

## Decision

Implement a deterministic archive script at:

```text
health/health-archive/scripts/archive_health_record.py
```

The script accepts a normalized JSON payload and writes to the external health workspace.

## Storage Contract

Default data root:

```text
~/document/personal health
```

Managed files:

- `records.md` for append-only human-readable records
- `profile.md` for long-lived profile facts
- `archive-log.jsonl` for machine verification and deduplication
- `raw/YYYY/MM/DD/` for copied evidence files and sidecar metadata

## Key Tradeoffs

### Why a script instead of markdown-only instructions

The failure mode we are fixing is not missing guidance. It is missing deterministic write semantics. A script provides an auditable write result and a stable output contract.

### Why keep both `records.md` and `archive-log.jsonl`

The user explicitly asked for a Markdown record file. But Markdown alone is a weak verification surface. The JSONL log gives the skill a durable way to confirm whether a matching archive already exists.

### Why deduplicate by entry key

Repeated replay of the same payload should not keep appending duplicate records. The entry key is derived from the normalized payload and source hashes, so the same archive request reuses the existing result.

## Validation Performed

- Python syntax check via `python3 -m py_compile`
- local smoke test with a temporary data root
- duplicate replay test confirming `deduplicated: true`
- inspection of generated `records.md`, `profile.md`, `archive-log.jsonl`, and raw evidence files

## Next Step

Use this archive path as the write foundation for `private-doctor`, without letting the doctor layer claim writes it did not perform.
