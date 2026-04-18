[English](README.md) | [中文](README.zh-CN.md)

# Health Skill 集

这个目录存放个人健康相关的可安装 skill。整个 skill 集采用 local-first 方案，健康数据放在仓库之外。

## 这套东西是什么

从用户视角看，`health` 不是“几个脚本的集合”，而是一套准备接管健康日常记录和家庭医生对话的能力。

你可以把它理解成：

- 你发体重、血压、运动、症状、用药相关图片或事实
- 它先帮你记录，并明确告诉你有没有真的写入
- 然后继续像家庭医生一样解释、提醒、给建议、做后续规划

目标不是做一个只会“记账”的记录员，而是做一个长期跟踪你健康变化的家庭医生型 agent。

## 为什么值得装

如果你现在的健康管理里有这些痛点，这套东西就是为你准备的：

- 发了图片，但不知道到底有没有记住
- 健康数据散在聊天里，后面很难回看
- 想有人持续帮你看趋势，而不是只回答一次问题
- 想把体重、血压、运动、作息、用药放到同一条健康主线上
- 后面还想要周总结、医生摘要、提醒，而不是每次从头说

## 适合谁

- 需要长期管理体重、血压、血脂、血糖风险的人
- 已经在调整饮食、运动、作息、用药，希望持续跟踪的人
- 想把“记录、解释、建议、复盘”连成一体的人

## 不适合谁

- 急诊、急危重症判断
- 想用它替代线下医生诊断或处方
- 需要非常专科化的第一版未覆盖场景

## 你会怎么用

典型使用路径是这样的：

1. 优先直接安装 `health/` 这一个整套入口
2. 安装后，像和真人家庭医生说话一样直接发健康相关图片或一句话
3. 日常继续发体重、血压、运动、症状、用药相关图片或事实
4. 它先记录，再继续和你解释“这意味着什么、接下来怎么做”
5. 后面逐步看周趋势、阶段总结、医生摘要

## 今天装完以后，你能做什么

当前 baseline 已经支持：

- 通过 `health/` 作为整套入口，一次装下完整 `health` 能力
- 发图片或事实后，做 local-first 归档，并明确告诉你是否记录成功
- 基于本地健康记录，做简洁的家庭医生式解读和建议
- 持续补全基础档案，而不是每次重新开始
- 日 / 周 / 月复盘
- 医生速读摘要
- 固定提醒和当前到点提醒判断
- 重置 / 迁移前的 bundle 导出与恢复

剩下的 roadmap 重点主要是发布收口、迁移 playbook 和未来可选适配器，而不是核心健康流程缺失。

## 第一次安装后怎么开始

第一次使用不应该要求你先学会怎么引导它。

正常路径应该只有一件事：

1. 先安装整套入口：
   `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health`
2. 安装完成后，直接自然地发健康图片或说一句健康相关的话就行。

它应该自己判断当前是在做：

- 第一次建档
- 日常记录
- 趋势解读
- 风险提醒

如果基础档案不够，它应该在回复里主动补问 1-3 个最重要的问题，而不是要求你先学会“怎么 prompt 它”。

例如：

```text
这是我今天早上的体重图
这是我今天的血压图
我最近想减重和控血压
我这两天有点头晕
```

## 日常会话应该长什么样

理想中的对话不是：

- 你发图
- 它只回一句“已记录”

而应该是：

- 先明确告诉你有没有真的写入
- 再告诉你这组数据怎么看
- 最后给一个短建议或下一步

也就是：

- `记录状态`
- `医生判断`
- `建议 / 下一步`

## 当前推荐安装方式

如果你今天就要开始用：

- 默认直接安装 `health/` 整套入口

如果你只想先解决“发图后到底有没有记住”：

- 先装 `health-archive`

如果你想要家庭医生式体验：

- 可以单独装 `health-archive + private-doctor`

现在同时支持两种方式：

- 直接安装 `health/`，把它当成整套家庭医生能力入口
- 直接安装某个子 skill，只拿自己需要的那一层能力

内部运行时仍然保持模块化；`health/` 只是整套分发入口，不是回到过去那种混在一起的大 agent。

## 本 Skill 集规则

- 所有运行时行为都收敛在 `health/` 里
- 不允许把 order 或其他非健康领域逻辑混进这个 skill 集
- 允许直接安装整套入口 `health/`，也允许单独安装某个子 skill
- 默认外部数据目录是 `~/Documents/personal health`，但安装时必须允许用户修改
- V1 默认关闭 Feishu

## Skill 列表

| Skill | 作用 | 安装路径 | 适用场景 | 备注 |
| --- | --- | --- | --- | --- |
| [`health-archive`](health-archive/README.zh-CN.md) | 把测量数据、截图和健康事实归档到本地记录，并明确回报是否成功 | `health/health-archive/` | 用户发来体重、血压、运动、睡眠、症状等需要记录的健康信息 | 第一优先交付 |
| [`private-doctor`](private-doctor/README.zh-CN.md) | 像简洁的家庭医生一样基于本地健康记录做解读、建议和规划 | `health/private-doctor/` | 用户需要建档、解读、趋势复盘、建议或后续规划 | 不允许退化成只会记账的记录员 |
| [`health-review`](health-review/README.zh-CN.md) | 生成日 / 周 / 月复盘和趋势总结 | `health/health-review/` | 用户需要看最近一段时间的变化和下一阶段重点 | 写入 `reviews/` |
| [`doctor-brief`](doctor-brief/README.zh-CN.md) | 生成医生速读摘要和阶段性就医材料 | `health/doctor-brief/` | 用户就医前需要一份医生更容易快速阅读的摘要 | 写入 `reports/` |
| [`health-reminders`](health-reminders/README.zh-CN.md) | 管理固定提醒和当前到点提醒判断 | `health/health-reminders/` | 用户需要晨测、复盘、运动或用药提醒 | 写入 `reminders/` |
| [`health-storage-feishu`](health-storage-feishu/README.zh-CN.md) | 导出 / 恢复本地健康工作区 bundle，作为可选备份 / 镜像层 | `health/health-storage-feishu/` | 用户准备重置旧 agent 或需要先做可带走的健康数据备份 | 当前重点是本地 bundle，不强绑 Feishu API |

## Health 整套安装入口

- `health/` 现在就是整套安装入口
- 目录里同时提供 umbrella `SKILL.md` 和 `SKILLSET.json`
- 如果宿主支持 suite manifest，它可以展开成多个已安装 skill
- 如果宿主只支持安装单个 skill 目录，也可以直接安装 `health/` 使用 umbrella skill
- 内部运行时仍然保持在 `health/` 模块内部分层
- 默认整套能力至少包含：
  - `health-archive`
  - `private-doctor`
  - `health-review`
  - `doctor-brief`
  - `health-reminders`
  - `health-storage-feishu`
- Feishu 相关适配器保持可选，不作为 health V1 的主路径
- 详细能力收口表见：
  - [Health 能力映射](../docs/reference/openclaw-skills/health-capability-map.zh-CN.md)

## 数据和隐私

- 默认数据目录是 `~/Documents/personal health`
- 你的健康数据默认放在本地，不依赖 Feishu 才能工作
- Feishu 在 V1 里不是主存储，只保留为未来可选备份 / 镜像路径
- 这也是为什么 roadmap 里把“重置前备份”和“重置后恢复”单独列成一阶段

## GitHub 直装模板

发布后，可以直接发整套安装地址，也可以发单个 skill 地址。

- `health` 整套安装
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health`
  - 开发安装: `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health`

- `health-archive`
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-archive`
- `private-doctor`
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/private-doctor`
- `health-review`
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-review`
- `doctor-brief`
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/doctor-brief`
- `health-reminders`
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-reminders`
- `health-storage-feishu`
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-storage-feishu`
- 维护者批量生成:
  - `python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.2.0 --domain health`

## 数据根目录

这个 skill 集的默认外部数据目录是 `~/Documents/personal health`。

建议结构：

```text
~/Documents/personal health/
  profile.md
  records.md
  raw/
  reviews/
  reports/
```
