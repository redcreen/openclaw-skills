[English](health-capability-map.md) | [中文](health-capability-map.zh-CN.md)

# Health 能力映射

这份文档用于把“原有 health agent 想要承担的能力”映射到新的 skill 集实现上，避免 roadmap 做完后仍然不知道哪些能力已经补齐、哪些还没落地。

## 目标

- 对齐原 health agent 能力和 skill 集拆分
- 明确当前状态：已完成 / 部分完成 / 规划中
- 明确每项能力会在哪个阶段收口

## 能力表

| 能力 | 目标承接面 | 当前状态 | 目标阶段 | 验收方式 |
| --- | --- | --- | --- | --- |
| 一键安装整套 `health` skill 集 | `health/` 整套入口 + `SKILLSET.json` | 已完成 | Stage 3 | 一个稳定 GitHub URL 就能安装整套入口；支持 suite manifest 的宿主还能自动展开成多个子 skill |
| 主动建档 | `private-doctor` | 已完成 | Stage 3 | CLI 场景可完成建档问答、写入 `profile.md`、输出第一阶段计划 |
| 三高相关风险初评 | `private-doctor` | 已完成 | Stage 3 | 初评回复能覆盖血压 / 血脂 / 血糖背景与主要风险提示 |
| 图片 / 事实自动归档 | `health-archive` | 已完成 | Stage 3 | 图片或事实输入后，真实写入并返回明确状态 |
| 图片归档后继续做家庭医生对话 | `health-archive` + `private-doctor` | 已完成 | Stage 3 | CLI 端到端验证：归档成功后继续输出医生判断与建议 |
| 家庭医生式持续跟踪 | `private-doctor` + `health-review` | 已完成 | Stage 4 | 多日记录后可输出趋势结论与后续跟踪重点 |
| 日报 / 周报 / 月报 | `health-review` | 已完成 | Stage 4 | 本地 `reviews/` 目录生成稳定复盘结果 |
| 医生速读摘要 / 阶段报告 | `doctor-brief` | 已完成 | Stage 4 | 本地 `reports/` 目录生成医生可读摘要 |
| 提醒机制 | `health-reminders` | 已完成 | Stage 5 | 固定提醒和轻量兜底提醒都可运行 |
| 重置前备份 / 迁移准备 | 重置/迁移 playbook + bundle 导出 / 恢复 | 已完成 | Stage 5 | 重置旧 agent 前能完成备份和恢复准备，并已有文档与测试 |
| Feishu 备份 / 镜像适配 | `health-storage-feishu` | 已完成 / 可选 | Stage 5 | 当前先承接 bundle 备份层，并为未来镜像适配留口，不影响 local-first 主流程 |
| 不依赖用户人肉验收 | CLI 验收链路 | 已完成 | Stage 5 | 安装、归档、对话、复盘、摘要、提醒和恢复基础链路都能由 CLI 自测 |

## 当前判断

现在模块化 skill 集已经覆盖了你要的 health agent V1。后续当然还可以继续增强 Feishu 可选适配器或体验细节，但“完整替代旧大 health agent”的基线已经不再缺层。
