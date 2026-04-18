# Health Archive

`health-archive` is the intake skill for local-first health records. It archives incoming measurements and health evidence into the user's external health data folder and returns explicit archive status.

## Install

- install target: `health/health-archive/`
- required artifact: `SKILL.md`
- default external data root: `~/document/personal health`
- installation rule: let the user choose the data path; do not hardcode a personal path

## GitHub Direct Install

- stable install:
  - `Install skill: https://github.com/<owner>/<repo>/tree/<tag>/health/health-archive`
- development install:
  - `Install skill: https://github.com/<owner>/<repo>/tree/main/health/health-archive`
- once the repository is published, maintainers can paste that URL directly into the OpenClaw chat.

## Runtime Pieces

- `SKILL.md`: archive behavior and reply contract
- `scripts/archive_health_record.py`: deterministic local write path
- `references/archive-format.md`: storage contract and payload schema
- `references/field-map.md`: normalized field names

## Use When

- the user sends a weight or blood pressure photo
- the user sends an exercise screenshot and expects it to be recorded
- the user wants to know whether an item was really archived

## Script Example

```bash
python3 scripts/archive_health_record.py --payload-file /tmp/health-archive-payload.json
```

## Usage Notes

- local files are the source of truth
- raw evidence should be backed up before claiming success
- the script writes `records.md`, `raw/YYYY/MM/DD/`, and `archive-log.jsonl`
- Feishu stays disabled by default
- uncertain health evidence should still be saved with an honest type such as `unknown-health`
- published install docs should prefer a tag instead of `main`
