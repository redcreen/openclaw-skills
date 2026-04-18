---
name: health-review
description: Generate daily, weekly, or monthly health reviews from the local health workspace. Use when the user wants trend-based follow-up, periodic summaries, or a short review grounded in archived weight, blood pressure, exercise, symptom, and medication records.
---

# Health Review

## Overview

This skill turns the local health workspace into review outputs. It is the longitudinal follow-up layer for the `health` skill set.

## Use This Skill When

- the user asks for a daily, weekly, or monthly health review
- the user wants trend-based follow-up rather than one-shot interpretation
- the user wants the recent records summarized into a short review file

## Working Contract

- default external data root: `~/document/personal health`
- read the same local health workspace used by `health-archive` and `private-doctor`
- write review outputs into `reviews/`
- keep Feishu disabled by default

## Scripted Review Path

1. Decide the review window:
   - `daily`
   - `weekly`
   - `monthly`
   - custom day range when needed
2. Run:

   ```bash
   python3 scripts/generate_health_review.py --mode weekly --save
   ```

3. Use the script result as the source of truth for:
   - review title
   - review window
   - trend summary
   - saved review path

## Reply Contract

Every user-visible review reply should include:

- `Review Window`
- `Main Takeaway`
- `What Changed`
- `Next Focus`

Keep the reply concise and grounded in archived records.

## Non-Goals

- real-time archiving
- clinician-facing brief generation
- pretending review conclusions are stronger than the available records support
