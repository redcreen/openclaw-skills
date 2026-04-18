# Archive Format

## 数据根目录

默认外部数据目录：

```text
~/Documents/personal health
```

预期结构：

```text
~/Documents/personal health/
  profile.md
  records.md
  archive-log.jsonl
  raw/YYYY/MM/DD/
```

`records.md` 是给人看的追加式主记录。
`archive-log.jsonl` 是给程序核验和去重用的机器日志。

## 原始证据命名

原图保存在：

```text
raw/YYYY/MM/DD/<timestamp>_<role>[_NN].<ext>
```

示例：

- `raw/2026/04/18/20260418T073200+0800_weight.jpg`
- `raw/2026/04/18/20260418T073200+0800_blood-pressure.jpg`
- `raw/2026/04/18/20260418T073200+0800_weight_02.jpg`

每个原图还会生成一个 sidecar 元数据文件：

```text
<saved-file>.<ext>.meta.json
```

示例：

- `20260418T073200+0800_weight.jpg.meta.json`

## Payload 结构

最小 payload：

```json
{
  "entry_type": "weight",
  "recorded_on": "2026-04-18",
  "fields": {
    "weight_kg": 82.45,
    "room_temp_c": 27
  },
  "sources": [
    {
      "path": "/absolute/path/to/weight.jpg",
      "role": "weight"
    }
  ]
}
```

支持的可选字段：

- `recorded_at`
- `notes`
- `doctor_note`
- `profile_updates`
- `data_root`

## 输出契约

归档脚本会把 JSON 结果打印到 stdout。

关键字段：

- `status`
- `entry_id`
- `entry_key`
- `record_path`
- `raw_files`
- `profile_path`
- `deduplicated`

用户可见的“是否记录成功”，只能以这份 JSON 结果为准。
