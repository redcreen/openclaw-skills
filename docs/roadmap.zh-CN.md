# 路线图

| 阶段 | 状态 | 目标 | 完成标准 | 解锁能力 |
| --- | --- | --- | --- | --- |
| [Stage 1](reference/openclaw-skills/development-plan.zh-CN.md#stage-1-工作区治理基线) | done | 把仓库明确成一个多 skill 集工作区，并写清隔离与索引规则 | 根文档、架构和控制面都对齐到顶层模块边界 | 后续模块可以按统一规则扩展 |
| [Stage 2](reference/openclaw-skills/development-plan.zh-CN.md#stage-2-health-skill-集基线) | done | 把 `health/` 建成第一个隔离的 skill 集，并补出独立 skill 目录和 README 面 | `health` landing 文档和首批 skill 骨架已存在 | 可以开始做功能实现 |
| [Stage 3](reference/openclaw-skills/development-plan.zh-CN.md#stage-3-health-archive-功能交付) | done | 把 `health-archive` 交付成一个 local-first 的归档 skill，并明确成功状态 | 原图备份、标准记录写入、状态回报端到端可用 | 可信的健康数据接收链路 |
| [Stage 4](reference/openclaw-skills/development-plan.zh-CN.md#stage-4-private-doctor-功能交付) | done | 把 `private-doctor` 交付成一个基于本地健康档案的简洁家庭医生 skill | 解读、建议、后续规划的行为稳定可用 | 可持续的家庭医生工作流 |
| [Stage 5](reference/openclaw-skills/development-plan.zh-CN.md#stage-5-未来-skill-集扩展与防漂移) | active | 后续新增 `order/` 等 skill 集时不再重开结构讨论，并让每个 skill 都具备 GitHub 直装入口 | 新模块都遵守同一套安装、文档、隔离和发布契约 | 可重复扩展多领域 skill 集 |
