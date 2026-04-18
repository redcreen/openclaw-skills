[English](README.md) | [中文](README.zh-CN.md)

# Private Doctor

`private-doctor` 是 `health` skill 集里的解读和规划 skill。它应该表现得像一个简洁的家庭医生，而不是一个被动记录员。

## 这是什么

从用户视角看，`private-doctor` 是“会继续和你说人话的那一层”。

它的工作不是只告诉你数值是多少，而是：

- 帮你逐步建档
- 结合最近记录做判断
- 告诉你什么值得关注
- 给一个短建议或下一步

如果 `health-archive` 解决的是“有没有记住”，`private-doctor` 解决的就是“记住以后，这意味着什么”。

## 为什么要装它

很多健康助手的问题不是不会识别数字，而是：

- 只会记，不会解释
- 解释太长，读起来累
- 每次都像第一次聊天，没有长期上下文

`private-doctor` 的目标就是把这些问题收掉：

- 回答要短，但不能空
- 要像家庭医生，而不是像录入员
- 要能基于本地档案持续对话

## 什么时候用

这些场景都适合：

- 第一次建立健康档案
- 想知道最近这组体重 / 血压 / 运动意味着什么
- 想要一个短建议
- 想知道接下来应该重点盯什么
- 发完图片 / 数据后，希望它继续像医生一样接着说

## 你会看到什么样的回复

理想中的回复应该很稳定，不应该忽长忽短。

通常会有这几部分：

- `记录状态`
- `医生判断`
- `建议`
- `下一步`

重点不是讲一大段，而是帮你快速理解：

- 这组数据算不算异常
- 现在更应该观察什么
- 今天 / 这几天下一步做什么

## 第一次怎么开始

第一次最适合做这两件事中的一件：

1. 直接建档
2. 基于刚记录的一条健康数据继续问它

例如：

```text
帮我建立健康档案：44岁，178cm，最近主要想控体重和血压
这是我今天的血压图，记录后告诉我这意味着什么
最近这几天体重一直在降，帮我看看趋势是不是正常
```

## 它不会替你做什么

`private-doctor` 不是急诊医生，也不是处方替代品。

它不会：

- 替代线下医生做诊断
- 轻率指导你停药、减药、换药
- 对单次波动做夸张判断

它更适合做长期管理里的“解释、提醒、规划”。

## 推荐搭配

如果只装 `private-doctor`，它可以读取已有本地记录并做解读。

但如果你想要完整体验，推荐至少搭配：

- `health-archive`
- `private-doctor`

这样你发图后，它可以先归档，再继续做家庭医生式对话。

## 安装

- 安装目录: `health/private-doctor/`
- 必需文件: `SKILL.md`
- 默认外部数据目录: `~/document/personal health`
- 安装要求: 必须允许用户自己选数据路径，且 Feishu 默认关闭

## GitHub 直装

- 正式安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/private-doctor`
- 开发安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health/private-doctor`
- 如果维护者已经发布了 release，可直接把上面的地址粘到 OpenClaw 对话框里。

## 给维护者看的实现组成

- `SKILL.md`: 医生行为和短回复契约
- `scripts/summarize_health_workspace.py`: 确定性读取本地健康工作区并生成摘要
- `scripts/assess_health_profile.py`: 做主动建档后的基础风险初评和第一阶段计划
- `scripts/render_doctor_reply.py`: 把摘要 JSON 渲染成稳定的医生式回复
- `scripts/validate_doctor_reply.py`: 轻量校验回复结构和归档状态表述
- `scripts/update_health_profile.py`: 把长期档案事实追加写入 `profile.md`
- `references/doctor-workflow.md`: 家庭医生工作流
- `references/onboarding-profile.md`: 建档指引
- `references/reply-contract.md`: 用户可见回复结构

## 使用注意

- 回复要短，但不能缺关键结论
- 只要有新事实进入，就应当让“记录状态”可见
- 这个 skill 必须负责解读和建议，不能退化成办事员
- 如果这个 skill 没有亲自看到一次成功归档结果，就必须把记录状态写成 `not verified in this skill`
- 建档场景优先走 `assess_health_profile.py`，不要只给缺口，不给初步判断
- 对外发布时优先使用 tag 地址，不要默认让用户安装 `main`
