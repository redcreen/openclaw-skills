# Archive Format

## Data Root

Default external data root:

```text
~/document/personal health
```

Expected layout:

```text
~/document/personal health/
  profile.md
  records.md
  archive-log.jsonl
  raw/YYYY/MM/DD/
```

`records.md` is the human-readable append-only log.
`archive-log.jsonl` is the machine-readable archive journal used for verification and deduplication.

## Raw Evidence Naming

Raw files are stored under:

```text
raw/YYYY/MM/DD/<timestamp>_<role>[_NN].<ext>
```

Examples:

- `raw/2026/04/18/20260418T073200+0800_weight.jpg`
- `raw/2026/04/18/20260418T073200+0800_blood-pressure.jpg`
- `raw/2026/04/18/20260418T073200+0800_weight_02.jpg`

Each saved raw file also gets a sidecar metadata file:

```text
<saved-file>.<ext>.meta.json
```

Example:

- `20260418T073200+0800_weight.jpg.meta.json`

## Payload Shape

Minimal payload:

```json
{
  "entry_type": "weight",
  "recorded_on": "2026-04-18",
  "fields": {
    "weight_kg": 82.45,
    "room_temp_c": 27
  },
  "sources": [
    {
      "path": "/absolute/path/to/weight.jpg",
      "role": "weight"
    }
  ]
}
```

Supported optional keys:

- `recorded_at`
- `notes`
- `doctor_note`
- `profile_updates`
- `data_root`

## Output Contract

The archive script prints JSON to stdout.

Important fields:

- `status`
- `entry_id`
- `entry_key`
- `record_path`
- `raw_files`
- `profile_path`
- `deduplicated`

Treat that JSON as the only reliable write result.
