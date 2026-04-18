[English](health-reset-playbook.md) | [中文](health-reset-playbook.zh-CN.md)

# Health Reset Playbook

This playbook defines the safe path for replacing the old health agent with the skill-based `health` suite.

## Goal

- preserve existing health data before reset
- reinstall the new suite from one stable GitHub URL
- restore the local-first health workspace after reset
- verify the replacement path without asking the user to do foundation-level QA manually

## Before You Reset The Old Agent

1. Identify where the current health truth still lives:
   - current local health workspace under `~/Documents/personal health`
   - legacy workspace files under `~/.openclaw/workspace-health/`
   - optional Feishu tables or documents that still hold unique records
2. Export a portable bundle from the current local-first workspace:

   ```bash
   python3 health/health-storage-feishu/scripts/export_health_workspace_bundle.py --data-root "~/Documents/personal health" --format zip
   ```

3. If the legacy workspace still contains notes or reports that are not yet reflected in the local-first workspace, archive that legacy directory separately before reset.
4. If Feishu still contains unique records that do not exist locally, export or snapshot those records before reset. The current suite does not require Feishu and does not pretend to pull legacy Feishu records automatically.

## Install The Replacement Suite

Use the stable suite entry:

```text
Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health
```

If you only want one focused workflow, you can still install a single nested skill such as `health/health-archive/`, but the reset path should normally use the full suite.

## Restore The Local Workspace

Restore the bundle into the new local health root:

```bash
python3 health/health-storage-feishu/scripts/import_health_workspace_bundle.py \
  --bundle-file /path/to/health-bundle.zip \
  --data-root "~/Documents/personal health" \
  --overwrite
```

## Verification Checklist

After restore, confirm:

- `profile.md` exists under the target data root
- `records.md` exists under the target data root
- `raw/` contains archived source evidence if source files were previously backed up
- `reviews/`, `reports/`, or `reminders/` exist when those workflows were already used
- the suite can summarize the restored workspace and generate a fresh review or brief if requested

## CLI Validation

Repository-level acceptance is already covered by:

```bash
python3 scripts/accept_health_suite.py --repo redcreen/openclaw-skills --ref v0.2.0
```

That acceptance chain proves:

- suite install
- archive and archive-session writes
- doctor onboarding and reply rendering
- review generation
- clinician brief generation
- reminders
- bundle export and restore

## Boundaries

- the new suite is local-first; Feishu is optional, not required
- the playbook does not claim that every legacy Feishu deployment can be auto-imported without user-specific credentials
- do not reset the old agent until every unique data source has been copied or exported once
