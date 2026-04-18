[English](README.md) | [中文](README.zh-CN.md)

# OpenClaw Skills 工作区

这个仓库是一个面向 OpenClaw 的多 skill 工作区。它按顶层 skill 集来组织不同领域，例如 `health/`、`order/`，同时保证领域之间隔离、具体 skill 可独立运行。

## 工作区规则

- 一个顶层目录代表一个领域 skill 集
- 一个可安装 skill 对应一个独立目录
- 不允许跨兄弟 skill 目录做运行时导入、prompt 加载或资源加载
- 不允许把 `health` 和 `order` 这类不同领域的逻辑混在同一个 skill 集里
- 仓库级文档可以共享，但运行时复用必须显式抽成独立边界

## 仓库结构

```text
openclaw-skills/
  health/
    README.zh-CN.md
    SKILL.md
    SKILLSET.json
    health-archive/
      SKILL.md
    private-doctor/
      SKILL.md
  order/
    ...
  docs/
    README.zh-CN.md
    architecture.zh-CN.md
    roadmap.zh-CN.md
    test-plan.zh-CN.md
```

## Skill 集索引

| Skill 集 | 作用 | 已有 Skill | 安装路径 | 使用注意 |
| --- | --- | --- | --- | --- |
| [`health`](health/README.zh-CN.md) | 个人健康建档、归档、家庭医生对话、复盘、摘要、提醒和备份 | [`health`](health/README.zh-CN.md)、[`health-archive`](health/health-archive/README.zh-CN.md)、[`private-doctor`](health/private-doctor/README.zh-CN.md)、[`health-review`](health/health-review/README.zh-CN.md)、[`doctor-brief`](health/doctor-brief/README.zh-CN.md)、[`health-reminders`](health/health-reminders/README.zh-CN.md)、[`health-storage-feishu`](health/health-storage-feishu/README.zh-CN.md) | 可直接安装 `health/` 整套入口，或单装 `health/<skill-name>/` | 健康数据默认落到 `~/Documents/personal health`；安装时允许用户改路径；Feishu 默认关闭 |
| `order` | 预留给未来订单相关 skill 集 | 暂无 | 尚未开始 | 后续新增时必须和 `health` 完全隔离 |

## 安装方式

现在同时支持整套入口和单个 skill 两种安装方式。

1. 如果你要完整的家庭医生体验，直接安装 `health/`。
2. 如果你只要一个聚焦能力，就安装对应目录，例如 `health/health-archive/`。
3. 先看对应 README，确认行为和数据目录规则。
4. 只配置所选安装目标真正需要的最小参数。

## GitHub 直装

发布后，推荐直接把单个 skill 的 GitHub 地址粘到 OpenClaw 对话框里，而不是让用户手动找目录。

- 正式整套安装建议固定到 tag:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health`
- 单 skill 稳定安装也固定到同一 tag:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/private-doctor`
- 开发安装可以指向 `main`:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health`
- 维护者可用 `python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.2.0 --domain health` 批量生成安装地址和可复制提示词。

## 文档入口

- English overview: [README.md](README.md)
- 文档首页: [docs/README.zh-CN.md](docs/README.zh-CN.md)
- GitHub 安装指引: [docs/reference/openclaw-skills/github-install.zh-CN.md](docs/reference/openclaw-skills/github-install.zh-CN.md)
- 架构说明: [docs/architecture.zh-CN.md](docs/architecture.zh-CN.md)
- 路线图: [docs/roadmap.zh-CN.md](docs/roadmap.zh-CN.md)
- 测试计划: [docs/test-plan.zh-CN.md](docs/test-plan.zh-CN.md)
