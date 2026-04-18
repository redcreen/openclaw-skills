# Field Map

Use stable normalized field names when extracting values before archiving.

## Weight

- `weight_kg`
- `body_fat_pct`
- `body_water_pct`
- `muscle_pct`
- `bmi`
- `room_temp_c`

## Blood Pressure

- `systolic_mmhg`
- `diastolic_mmhg`
- `pulse_bpm`

## Exercise

- `exercise_type`
- `duration_min`
- `distance_km`
- `steps`
- `calories_kcal`
- `average_pace_min_per_km`
- `average_heart_rate_bpm`

## Sleep

- `sleep_duration_hr`
- `bed_time`
- `wake_time`
- `deep_sleep_hr`

## Symptoms And Medication

Prefer concise factual keys such as:

- `symptom_name`
- `symptom_severity`
- `medication_name`
- `medication_dose`
- `medication_schedule`

If a fact does not fit a stable field yet, keep it in `notes` instead of inventing a one-off key.
