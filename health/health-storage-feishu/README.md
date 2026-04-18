[English](README.md) | [中文](README.zh-CN.md)

# Health Storage Feishu

`health-storage-feishu` is the optional backup and migration layer in the `health` skill set. In the current version its main job is to export and restore portable bundles from the local health workspace before any future Feishu mirror path is enabled.

## What This Is

From a user point of view, it solves questions like:

- how do I back up my health workspace before resetting the old health agent
- how do I restore that workspace after reset
- where should a future Feishu mirror or backup adapter connect

## Why Install It

Its value becomes especially clear before reset or migration:

- export one portable bundle from the local workspace
- restore that bundle later into a fresh local workspace
- avoid making Feishu the primary storage requirement from day one

## When To Use It

- before resetting the old health agent
- when you want a portable local health-data bundle
- when you want to restore a bundle into the local workspace

## What You Should Expect Back

In most cases the result should show:

- export or restore status
- the bundle file path
- what the bundle contains
- which local health directory was used

## Install

- install target: `health/health-storage-feishu/`
- required artifact: `SKILL.md`
- default external data root: `~/Documents/personal health`
- installation rule: allow the user to choose the data path; remote Feishu writes stay disabled by default

## GitHub Direct Install

- stable install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/v0.2.1/health/health-storage-feishu`
- development install:
  - `Install skill: https://github.com/redcreen/openclaw-skills/tree/main/health/health-storage-feishu`

## Maintainer Runtime Pieces

- `SKILL.md`: backup and restore behavior plus reply contract
- `scripts/export_health_workspace_bundle.py`: exports portable local bundles
- `scripts/import_health_workspace_bundle.py`: restores local bundles

## Usage Notes

- the current version is about local bundle export and restore
- Feishu remains a future optional mirror or backup adapter rather than the main source of truth
- do not describe “bundle export succeeded” as “synced to Feishu”
