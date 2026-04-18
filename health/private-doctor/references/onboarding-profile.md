# Onboarding Profile

Collect only the smallest useful baseline.

## High-Value Profile Facts

- `age` or `birth_year`
- `sex`
- `height_cm`
- `main_health_goal` or `goal_weight_kg`
- `known_conditions`
- `current_medications`
- `current_concerns`

## Preferred Behavior

- do not dump all questions at once
- ask only what is missing and relevant to the current request
- once a fact is confirmed and likely to stay useful, write it to `profile.md`
- after a first image or first health fact, ask only the next 1-3 highest-value questions
- give a complete but compact interpretation before the questions when there is already enough measurement data to say something useful

## Example Payload

```json
{
  "facts": [
    {
      "label": "height_cm",
      "value": 175
    },
    {
      "label": "main_health_goal",
      "value": "reduce weight and stabilize blood pressure"
    }
  ]
}
```
