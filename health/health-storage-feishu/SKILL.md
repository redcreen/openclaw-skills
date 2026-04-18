---
name: health-storage-feishu
description: Export or restore the local health workspace for optional external backup or mirror storage. Use when the user wants a portable bundle before reset, a restore path after reset, or a future Feishu-facing export surface without making Feishu the required source of truth.
---

# Health Storage Feishu

## Overview

This skill is the optional backup and migration layer for the `health` skill set. In the current version it focuses on export and restore bundles from the local health workspace.

## Use This Skill When

- the user wants a portable backup before resetting the old health agent
- the user wants to restore the local health workspace after reset
- the user wants an external-storage export surface without making Feishu the required write path

## Working Contract

- default external data root: `~/Documents/personal health`
- local-first storage remains the source of truth
- export and restore bundles live under `exports/`
- Feishu API writes remain optional and disabled by default

## Scripted Backup Path

1. Export a bundle:

   ```bash
   python3 scripts/export_health_workspace_bundle.py --format zip
   ```

2. Restore a bundle:

   ```bash
   python3 scripts/import_health_workspace_bundle.py --bundle-file /tmp/health-bundle.zip --overwrite
   ```

## Reply Contract

Every backup or restore reply should show:

- `Bundle Status`
- `Source Or Target`
- `Saved To`
- `What Was Included`

Keep the reply factual and explicit.

## Non-Goals

- making Feishu the V1 primary storage path
- pretending a remote sync happened when only a local export bundle was created
