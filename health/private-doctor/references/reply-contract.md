# Reply Contract

## Routine Reply

Keep routine replies short and stable:

- `Record Status`
- `Doctor View`
- `Advice`
- `Plan` only when useful

## Onboarding Reply

When building a profile:

- `Record Status` when a measurement or image was part of this turn
- `Profile Status`
- `Doctor View`
- `Next Questions`

## Style Rules

- use calm factual language
- do not overstate a single reading
- prefer one or two concrete next steps
- avoid long essays unless the user explicitly asks for depth

## Scripted Rendering

Prefer rendering the user-visible reply from the summary JSON:

```bash
python3 scripts/render_doctor_reply.py --summary-file /tmp/private-doctor-summary.json --language zh --mode routine
```

If the reply will be shown to a user, prefer validating it too:

```bash
python3 scripts/validate_doctor_reply.py --reply-file /tmp/private-doctor-reply.json
```

## Routine Reply Example

```text
记录状态：已核验，已入档
医生判断：最近血压高于理想值，但还不算急迫异常；最近体重记录还不足以下趋势结论。
建议：今天先按标准条件再测 1 次血压，继续同口径记录晨测。
下一步：先连续积累 3-5 天同口径记录，再看趋势更稳。
```

## Onboarding Reply Example

```text
记录状态：已核验，已入档
档案状态：基础档案还不完整，但已经可以开始跟踪。
医生判断：这次体重先记住了；单次数据还不能下趋势结论，但已经可以作为你的健康档案起点。
下一步问题：请先补年龄或出生年、身高、目前主要目标。
```
