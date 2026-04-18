# Doctor Workflow

## Working Modes

### 1. Onboarding

Use this mode when:

- the user asks to create or refresh a health profile
- the local profile is sparse
- profile-critical facts are missing for the advice they want
- the user sends a first health image or first health fact and the profile is still sparse

Actions:

1. run `skills/private-doctor/scripts/summarize_health_workspace.py`
2. inspect `profile_gaps`
3. if a fresh measurement already exists, give a short baseline interpretation first
4. ask only the smallest set of missing high-value questions
5. once the user confirms long-lived facts, write them with `skills/private-doctor/scripts/update_health_profile.py`
6. give a short first-phase next step

### 2. Routine Follow-Up

Use this mode when:

- the user asks what a recent measurement means
- the user wants short advice
- there are already archived records to interpret

Actions:

1. run `skills/private-doctor/scripts/summarize_health_workspace.py`
2. use `doctor_snapshot.summary_lines`, `watchpoints`, and `follow_up_topics`
3. produce a short reply using the reply contract

### 3. Trend Review

Use this mode when:

- the user asks for a recent trend
- the user wants a weekly or multi-day view

Actions:

1. run `skills/private-doctor/scripts/summarize_health_workspace.py --days 7` or a wider window
2. compare weight, blood pressure, and exercise summaries
3. keep the conclusion cautious and trend-based

## Archive Boundary

This skill reads the same local workspace as `health-archive`, but it does not depend on that skill folder at runtime.

Important rule:

- if a measurement archive was not produced by a known successful write result, mark it as `Record Status: not verified in this skill`
- long-lived profile facts may still be written through `skills/private-doctor/scripts/update_health_profile.py`
- if archive was verified and the user is clearly in a health flow, continue the doctor dialogue in the same turn instead of stopping at archive status
