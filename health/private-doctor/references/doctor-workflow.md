# Doctor Workflow

## Working Modes

### 1. Onboarding

Use this mode when:

- the user asks to create or refresh a health profile
- the local profile is sparse
- profile-critical facts are missing for the advice they want

Actions:

1. run `scripts/summarize_health_workspace.py`
2. inspect `profile_gaps`
3. ask only the smallest set of missing high-value questions
4. once the user confirms long-lived facts, write them with `scripts/update_health_profile.py`
5. give a short baseline interpretation and next step

### 2. Routine Follow-Up

Use this mode when:

- the user asks what a recent measurement means
- the user wants short advice
- there are already archived records to interpret

Actions:

1. run `scripts/summarize_health_workspace.py`
2. use `doctor_snapshot.summary_lines`, `watchpoints`, and `follow_up_topics`
3. produce a short reply using the reply contract

### 3. Trend Review

Use this mode when:

- the user asks for a recent trend
- the user wants a weekly or multi-day view

Actions:

1. run `scripts/summarize_health_workspace.py --days 7` or a wider window
2. compare weight, blood pressure, and exercise summaries
3. keep the conclusion cautious and trend-based

## Archive Boundary

This skill reads the same local workspace as `health-archive`, but it does not depend on that skill folder at runtime.

Important rule:

- if a measurement archive was not produced by a known successful write result, mark it as `Record Status: not verified in this skill`
- long-lived profile facts may still be written through `scripts/update_health_profile.py`
