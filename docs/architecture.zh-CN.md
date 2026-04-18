[English](architecture.md) | [中文](architecture.zh-CN.md)

# 架构说明

## 系统形态

这个仓库是一个带模块边界的 OpenClaw skill 工作区。

- 每个顶层目录，例如 `health/`、`order/`，代表一个独立的 skill 集
- 顶层 skill 集根目录可以选择性提供 `SKILL.md` 或 `SKILLSET.json` 作为整套入口，但不能越出本领域边界
- 每个下一层 skill 目录，例如 `health/health-archive/`，代表一个可单独安装的 skill
- 每个 skill 自己拥有 `SKILL.md`、UI 元数据、prompt、references 和 assets

## 目录拓扑

```text
<repo root>/
  <skill-set>/
    README.md
    README.zh-CN.md
    SKILL.md              # 可选的整套入口
    SKILLSET.json         # 可选的整套 manifest
    <skill-name>/
      SKILL.md
      agents/openai.yaml
      README.md
      README.zh-CN.md
```

## 边界规则

- 一个 skill 集不能吸收另一个领域的业务规则
- 一个 skill 不能导入、调用或加载兄弟 skill 的运行时资源
- 一个领域 skill 集不能复用另一个领域 skill 集的运行时资源
- 仓库级文档可以共享
- 如果未来确实需要复用，必须显式抽成独立共享边界，而不是直接走兄弟目录捷径

## 模块清单

### `health`

- 作用: 个人健康建档、归档、解读和规划
- 整套入口: `health/`
- 当前 skill: `health-archive`、`private-doctor`、`health-review`、`doctor-brief`、`health-reminders`
- 可选适配器: `health-storage-feishu`
- 默认外部数据目录: `~/Documents/personal health`
- Feishu 策略: 默认关闭，未来只作为可选存储适配器

### `order`

- 作用: 预留给未来订单相关 skill
- 当前状态: 已规划，尚未搭建
- 规则: 不允许复用 `health` 的运行时逻辑、prompt 或资源

## 数据与运行时边界

- 用户数据必须存放在仓库之外
- skill 可以定义默认外部数据目录，但安装时必须允许用户覆盖
- `health` skill 集默认目录是 `~/Documents/personal health`
- skill 对“是否记录成功”的反馈必须来自真实写入结果，不能只凭推断

## Health 套件分发模型

- 运行时仍然保持在 `health/` 内部的多 skill 分层
- `health/` 可以同时提供 umbrella skill 和 suite manifest 作为安装入口
- 分发层需要同时支持：
  - 单 skill 安装
  - 一条命令安装整套 `health` skill 集
- 整套安装的本质可以是：
  - 同一仓库 / 同一 tag 下安装多个子 skill 目录，或
  - 在宿主只支持单目录安装时，直接安装 `health/` umbrella 入口
- 无论哪种分发方式，都不改变 `health` 内部运行时边界
- 重置旧 health agent 后，预期通过整套安装入口恢复健康能力

## 验证模型

- health V1 不能只靠用户人肉点测
- readiness 需要先通过 CLI 验收链路证明：
  - 整套安装
  - 图片 / 事实归档
  - 家庭医生对话
  - 长期复盘
  - 医生摘要
  - 提醒基础路径
- 用户测试应该只承担体验确认，不承担基础功能代测

## 文档模型

- 根目录 `README*` 是工作区总索引
- 每个 skill 集拥有自己的 landing README 对
- 每个 skill 拥有自己的 README 对，负责安装和使用说明
- `docs/` 负责共享工作区文档，例如架构、路线图、测试计划和开发计划

## 明确拒绝的捷径

- 把所有 health 能力继续塞回一个混合型大 agent 目录
- 从一个领域复制 skill 再临时改名给另一个领域使用
- 在 local-first 场景里把 Feishu 或其他外部系统当成唯一真实存储
