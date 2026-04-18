# OpenClaw Skills 工作区

这个仓库是一个面向 OpenClaw 的多 skill 工作区。它按顶层 skill 集来组织不同领域，例如 `health/`、`order/`，同时保证每个具体 skill 都可以单独安装、单独运行。

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
| [`health`](health/README.zh-CN.md) | 个人健康建档、归档、解读和规划 | [`health-archive`](health/health-archive/README.zh-CN.md)、[`private-doctor`](health/private-doctor/README.zh-CN.md) | 按 `health/<skill-name>/` 目录逐个安装 | 健康数据默认落到 `~/document/personal health`；安装时允许用户改路径；Feishu 默认关闭 |
| `order` | 预留给未来订单相关 skill 集 | 暂无 | 尚未开始 | 后续新增时必须和 `health` 完全隔离 |

## 安装方式

按单个 skill 安装，不按整个 skill 集整包安装。

1. 先选领域 skill 集，例如 `health/`。
2. 打开目标 skill 自己的 README。
3. 安装包含该 `SKILL.md` 的目录。
4. 只配置该 skill 需要的最小参数。

## GitHub 直装

发布后，推荐直接把单个 skill 的 GitHub 地址粘到 OpenClaw 对话框里，而不是让用户手动找目录。

- 正式安装建议固定到 tag:
  - `安装技能：https://github.com/<owner>/<repo>/tree/<tag>/health/health-archive`
- 开发安装可以指向 `main`:
  - `安装技能：https://github.com/<owner>/<repo>/tree/main/health/private-doctor`
- 维护者可用 `python3 scripts/generate_skill_install_manifest.py --repo <owner>/<repo> --ref <tag>` 批量生成每个 skill 的安装地址和可复制提示词。

## 文档入口

- English overview: [README.md](README.md)
- 文档首页: [docs/README.zh-CN.md](docs/README.zh-CN.md)
- GitHub 安装指引: [docs/reference/openclaw-skills/github-install.zh-CN.md](docs/reference/openclaw-skills/github-install.zh-CN.md)
- 架构说明: [docs/architecture.zh-CN.md](docs/architecture.zh-CN.md)
- 路线图: [docs/roadmap.zh-CN.md](docs/roadmap.zh-CN.md)
- 测试计划: [docs/test-plan.zh-CN.md](docs/test-plan.zh-CN.md)
