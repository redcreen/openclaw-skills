# 2026-04-18 Private Doctor Local Summary Foundation

## Problem

The `private-doctor` skill still behaved like a thin prompt shell. That was not enough to support the intended family-doctor role:

- it needed a deterministic way to read recent health state
- it needed a deterministic way to write long-lived profile facts
- it needed to stay isolated from the `health-archive` skill folder at runtime

## Decision

Add doctor-local scripts inside `health/private-doctor/` instead of calling the sibling `health-archive` folder.

Implemented scripts:

- `scripts/summarize_health_workspace.py`
- `scripts/update_health_profile.py`

## Why This Boundary

Directly calling the sibling skill would violate the workspace isolation rule.

Duplicating only the minimum doctor-side logic is acceptable here because:

- the shared artifact is the external health workspace, not sibling runtime code
- the doctor layer mostly needs read access plus profile writes
- measurement archive truth still belongs to the archive layer

## Key Behavior Contract

- doctor replies are grounded in the summary script output
- long-lived facts can be appended to `profile.md`
- the doctor layer must not claim archive success it did not directly observe

## Validation Performed

- Python syntax check for both doctor scripts
- local smoke test against the existing temporary health workspace
- profile update test adding `height_cm` and `main_health_goal`
- summary output inspection confirming weight, blood pressure, profile gaps, and follow-up topics

## Next Step

Refine final user-visible doctor replies so they stay concise, useful, and honest about record status.
