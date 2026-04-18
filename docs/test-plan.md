[English](test-plan.md) | [中文](test-plan.zh-CN.md)

# Test Plan

## Scope

Verify workspace structure, documentation routing, suite-install behavior, and the full health V1 acceptance chain.

## Acceptance Cases

- Case: root index routes correctly
  - Setup: open `README.md`
  - Action: inspect the workspace rules and skill-set index
  - Expected Result: the reader can find the `health` skill set, its skills, install path, and usage notes from the root page

- Case: health skill-set docs are isolated
  - Setup: open `health/README.md`
  - Action: inspect the health landing page
  - Expected Result: the page explains only health skills and does not mix order behavior or install steps

- Case: the full `health` suite has a top-level install entry
  - Setup: inspect `health/`
  - Action: verify the suite entry files
  - Expected Result: `health/` contains `SKILL.md`, `agents/openai.yaml`, and `SKILLSET.json`, so the full family-doctor suite has one stable install target

- Case: each health skill is independently installable
  - Setup: inspect `health/health-archive/`, `health/private-doctor/`, `health-review/`, `doctor-brief/`, `health-reminders/`, and `health-storage-feishu/`
  - Action: verify the folder contents
  - Expected Result: each folder contains `SKILL.md`, `agents/openai.yaml`, and a README pair for install and usage

- Case: workspace docs explain the top-level boundary
  - Setup: open `docs/architecture.md`
  - Action: inspect the topology and boundary rules
  - Expected Result: the docs explicitly state top-level skill-set isolation and per-skill runtime independence

- Case: health storage default remains configurable
  - Setup: open health docs
  - Action: inspect install and configuration notes
  - Expected Result: the default path is `~/document/personal health` and the docs say the user chooses the path during installation

- Case: GitHub direct-install entry points are copy-paste ready
  - Setup: open the root README, `health/README.md`, and an individual skill README
  - Action: inspect the GitHub install examples
  - Expected Result: a user can copy the suite URL or a single-skill GitHub tree URL into OpenClaw chat, and the docs prefer a tag-based URL for published installs

- Case: reset and migration guidance exists
  - Setup: open `docs/reference/openclaw-skills/health-reset-playbook.md`
  - Action: inspect the reset flow
  - Expected Result: the playbook explains backup, suite reinstall, restore, and verification without making Feishu the required write path

## Manual Checks

- verify all repository links are relative
- verify bilingual public docs have corresponding English and Chinese pages
- verify the root README does not become a per-skill implementation dump

## Automated Coverage

Available now:

- `python3 scripts/validate_skill_boundaries.py`
  - detects missing required public skill files
  - detects runtime references across sibling skills or skill sets
- `python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.2.0 --domain health --format json`
  - generates suite and per-skill GitHub install URLs and copy-paste prompts
- `python3 scripts/accept_health_suite.py --repo redcreen/openclaw-skills --ref v0.2.0`
  - proves suite install, archive, doctor dialogue, review, brief, reminders, and bundle restore from CLI
