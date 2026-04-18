[English](development-plan.md) | [中文](development-plan.zh-CN.md)

# 开发计划

## 这份计划的作用

这份计划把路线图进一步展开成工作区可执行的实施队列。

## 使用方式

- 用 `docs/roadmap.zh-CN.md` 看里程碑顺序
- 用这份文件看详细执行队列
- 用 `.codex/plan.md` 看当前执行线

## 当前所处位置

工作区现在已经在模块化 `health` skill 集里完成了你要的 health agent V1 收口。接下来再做的会是未来迭代，不再是“核心能力还没补齐”的状态。

## Health V1 收口目标

这次路线图收口时，需要同时满足以下目标：

1. 重置旧 health agent 后，可以用一条命令安装整套 `health` skill 集。
2. 安装完成后，agent 能像家庭医生一样主动建档、自动记录图片/事实，并继续对话解释和给建议。
3. 长期跟踪、阶段复盘、医生摘要和提醒能力都由 skill 集承接，而不是依赖旧 agent。
4. CLI 验收链路必须完整，不能把基本功能测试甩给用户人肉验证。
5. Feishu 只保留为可选备份/镜像适配器，不再作为主存储前提。

## Stage 1: 工作区与 local-first 基线

### 目标

把仓库定义成一个带根索引、长期文档和模块控制面的多 skill 集工作区，并建立 `health` 的 local-first 基线。

### 状态

已完成。

### 已完成工作

- 根 README 对改成工作区索引
- 补齐架构、路线图和测试计划
- 增加模块化 `.codex` 控制层
- 把健康数据基线收口到 `~/Documents/personal health`

## Stage 2: 归档与家庭医生基线

### 目标

交付 `health-archive` 与 `private-doctor` 的基线闭环，让健康数据可以 local-first 地记录和解释。

### 状态

已完成。

### 已完成工作

1. 创建 `health` landing README 对。
2. 创建 `health-archive` 与 `private-doctor` 标准 skill 目录。
3. 定义 `~/Documents/personal health` 的本地存储契约。
4. 实现归档、医生摘要、档案更新、回复渲染与基础校验脚本。
5. 公开 GitHub 安装入口并发布 `v0.1.0`。

## Stage 3: Health 整套安装与医生核心能力补齐

### 目标

补齐“整套安装 + 主动建档 + 三高初评 + 图片归档后继续医生对话”的核心能力，做到重置旧 health agent 后可以直接从 skill 集恢复。

### 状态

已完成。

### 已完成工作

1. 增加 `health/SKILL.md` 与 `health/SKILLSET.json`，让整套入口稳定存在，同时保留子 skill 的独立安装能力。
2. 增加 `archive_health_session.py`，支持用户一次发多条健康信息时的 session 归档。
3. 扩充 `private-doctor` 的建档和初评能力，覆盖主动建档、基础风险判断和第一阶段计划。
4. 增加 CLI 验收，证明“归档 -> 医生判断 -> 下一步建议”可以跑通。
5. 刷新发布和安装文档，让整套安装入口对外可用。

### 完成标准

- 一条命令可安装整套 `health` skill 集
- 重置旧 agent 后可直接恢复核心健康能力
- CLI 端到端测试能证明图片归档后可以继续做家庭医生式对话

## Stage 4: 长期跟踪复盘与医生摘要

### 目标

交付长期跟踪、阶段复盘和医生可读摘要能力，让 skill 集不只是“会记录 + 会解读”，而是能持续管理。

### 状态

已完成。

### 已完成工作

1. 增加 `health-review`，可生成日 / 周 / 月复盘。
2. 让复盘结果稳定写入本地 `reviews/`。
3. 增加 `doctor-brief`，生成医生速读摘要和阶段性就医资料。
4. 让摘要结果稳定写入本地 `reports/`。
5. 把 review 和 doctor brief 生成也纳入 CLI 验收链路。

### 完成标准

- `health-review` 与 `doctor-brief` 可用
- 本地 `reviews/` 与 `reports/` 目录不再只是约定
- 用户的长期跟踪和就医支持能力由 skill 集承接

## Stage 5: 提醒自动化迁移与 Health V1 收口

### 目标

交付提醒、重置/迁移准备和 health V1 最终验收，确保技能集真正能替代当前旧 health agent。

### 状态

已完成。

### 已完成工作

1. 增加 `health-reminders`，支持固定提醒规则和到点提醒判断。
2. 增加 `health-storage-feishu`，先承接 bundle 导出 / 恢复，作为备份和迁移层。
3. 增加重置 / 迁移 playbook，明确旧 agent 的替换路径。
4. 建立 CLI 完整验收链路，覆盖安装、归档、对话、复盘、摘要、提醒和 bundle 恢复。
5. 保持 Feishu 为可选项，而不是重新变成主存储前提。

### 完成标准

- 你可以先备份旧数据，再重置旧 health agent
- 新 agent 通过安装整套 `health` skill 集恢复完整能力
- 核心能力已经由 CLI 端到端验证过
