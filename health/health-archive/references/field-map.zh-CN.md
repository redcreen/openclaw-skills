# Field Map

归档前尽量把提取出来的字段规范成稳定命名。

## 体重

- `weight_kg`
- `body_fat_pct`
- `body_water_pct`
- `muscle_pct`
- `bmi`
- `room_temp_c`

## 血压

- `systolic_mmhg`
- `diastolic_mmhg`
- `pulse_bpm`

## 运动

- `exercise_type`
- `duration_min`
- `distance_km`
- `steps`
- `calories_kcal`
- `average_pace_min_per_km`
- `average_heart_rate_bpm`

## 睡眠

- `sleep_duration_hr`
- `bed_time`
- `wake_time`
- `deep_sleep_hr`

## 症状和用药

尽量使用简洁、稳定的事实字段，例如：

- `symptom_name`
- `symptom_severity`
- `medication_name`
- `medication_dose`
- `medication_schedule`

如果某个事实暂时没有稳定字段，优先放进 `notes`，不要临时发明一次性 key。
