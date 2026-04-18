# Private Doctor

`private-doctor` 是 `health` skill 集里的解读和规划 skill。它应该表现得像一个简洁的家庭医生，而不是一个被动记录员。

## 安装

- 安装目录: `health/private-doctor/`
- 必需文件: `SKILL.md`
- 默认外部数据目录: `~/document/personal health`
- 安装要求: 必须允许用户自己选数据路径，且 Feishu 默认关闭

## GitHub 直装

- 正式安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.1.0/health/private-doctor`
- 开发安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health/private-doctor`
- 如果维护者已经发布了 release，可直接把上面的地址粘到 OpenClaw 对话框里。

## 运行组成

- `SKILL.md`: 医生行为和短回复契约
- `scripts/summarize_health_workspace.py`: 确定性读取本地健康工作区并生成摘要
- `scripts/render_doctor_reply.py`: 把摘要 JSON 渲染成稳定的医生式回复
- `scripts/validate_doctor_reply.py`: 轻量校验回复结构和归档状态表述
- `scripts/update_health_profile.py`: 把长期档案事实追加写入 `profile.md`
- `references/doctor-workflow.md`: 家庭医生工作流
- `references/onboarding-profile.md`: 建档指引
- `references/reply-contract.md`: 用户可见回复结构

## 适用场景

- 用户需要建立或更新健康档案
- 用户想知道最近这组测量数据意味着什么
- 用户需要简短建议或后续计划

## 使用注意

- 回复要短，但不能缺关键结论
- 只要有新事实进入，就应当让“记录状态”可见
- 这个 skill 必须负责解读和建议，不能退化成办事员
- 如果这个 skill 没有亲自看到一次成功归档结果，就必须把记录状态写成 `not verified in this skill`
- 对外发布时优先使用 tag 地址，不要默认让用户安装 `main`
