# Health Skill Set

This folder contains installable skills for personal health workflows. The set is local-first and keeps health data outside the repository.

## Rules For This Skill Set

- keep all runtime behavior inside `health/`
- do not mix order or other non-health business logic into this set
- install individual skills, not the whole folder as one hidden monolith
- default external data root is `~/document/personal health`, but installation must let the user override it
- Feishu is disabled by default in V1

## Skills

| Skill | Role | Install Path | Use When | Notes |
| --- | --- | --- | --- | --- |
| [`health-archive`](health-archive/README.md) | Archive measurements, screenshots, and health facts into local records with explicit success status | `health/health-archive/` | the user sends weight, blood pressure, exercise, sleep, symptom, or other health evidence that should be recorded | first functional delivery target |
| [`private-doctor`](private-doctor/README.md) | Act like a concise family doctor that interprets, advises, and plans from local health records | `health/private-doctor/` | the user wants onboarding, explanation, trend review, advice, or follow-up planning | must not degrade into recorder-only behavior |

## GitHub Direct Install Templates

After publishing, prefer sending the exact GitHub tree URL for the chosen skill.

- `health-archive`
  - `Install skill: https://github.com/<owner>/<repo>/tree/<tag>/health/health-archive`
- `private-doctor`
  - `Install skill: https://github.com/<owner>/<repo>/tree/<tag>/health/private-doctor`
- maintainer batch generation:
  - `python3 scripts/generate_skill_install_manifest.py --repo <owner>/<repo> --ref <tag> --domain health`

## Data Root

The default external data root for this skill set is `~/document/personal health`.

Recommended structure:

```text
~/document/personal health/
  profile.md
  records.md
  raw/
  reviews/
  reports/
```
