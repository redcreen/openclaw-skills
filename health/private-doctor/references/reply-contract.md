# Reply Contract

## Routine Reply

Keep routine replies short and stable:

- `Record Status`
- `Doctor View`
- `Advice`
- `Plan` only when useful

## Onboarding Reply

When building a profile:

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
记录状态：本次未在此 skill 中核验归档
档案状态：基础档案未完整，仍缺 4 类关键信息。
医生判断：目前已有最近体重和血压记录，可以先做初步跟踪，但档案还不够完整。
下一步问题：请先补年龄或出生年、性别、已知疾病、当前用药。
```
