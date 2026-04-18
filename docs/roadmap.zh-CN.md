[English](roadmap.md) | [中文](roadmap.zh-CN.md)

# 路线图

| 阶段 | 状态 | 目标 | 完成标准 | 解锁能力 |
| --- | --- | --- | --- | --- |
| [Stage 1](reference/openclaw-skills/development-plan.zh-CN.md#stage-1-工作区与-local-first-基线) | done | 建立多 skill 集工作区和 `health` 的 local-first 基线 | 根文档、架构、控制面、`health` 落地目录和本地数据契约都已存在 | 可以围绕健康能力做模块化交付 |
| [Stage 2](reference/openclaw-skills/development-plan.zh-CN.md#stage-2-归档与家庭医生基线) | done | 交付 `health-archive` 与 `private-doctor` 的基础闭环 | 图片/事实归档、简洁医生式解读、GitHub 发布入口和本地工作区都已可用 | 有可信的健康归档与基础医生对话 |
| [Stage 3](reference/openclaw-skills/development-plan.zh-CN.md#stage-3-health-整套安装与医生核心能力补齐) | active | 补齐“整套安装 + 主动建档 + 三高初评 + 图片归档后对话”这一轮核心能力 | 一条命令可安装整套 `health` skill 集；`private-doctor` 完成建档、初评、第一阶段计划；CLI 端到端验证图片归档后能继续医生对话 | 重置旧 health agent 后可直接用 skill 集重建核心能力 |
| [Stage 4](reference/openclaw-skills/development-plan.zh-CN.md#stage-4-长期跟踪复盘与医生摘要) | planned | 交付长期跟踪、阶段复盘和医生可读摘要能力 | `health-review` 与 `doctor-brief` 可以把本地记录写成日/周/月复盘与医生速读摘要 | 从“会记录和判断”升级到“会长期跟踪和就医支持” |
| [Stage 5](reference/openclaw-skills/development-plan.zh-CN.md#stage-5-提醒自动化迁移与-health-v1-收口) | planned | 交付提醒、迁移/重置准备与 health V1 收口 | 提醒路径、重置前备份/迁移方案、CLI 完整验收链路都具备；Feishu 仍保持可选适配器而不是主路径 | 你要的 health agent V1 能力可以完全由 skill 集承接 |
