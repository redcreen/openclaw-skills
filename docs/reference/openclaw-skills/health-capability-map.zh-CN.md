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
| 一键安装整套 `health` skill 集 | `health` 整套安装入口，不把 `health/` 伪装成单个 skill | 规划中 | Stage 3 | 一条命令从 GitHub tag 安装整套 health skill |
| 主动建档 | `private-doctor` | 部分完成 | Stage 3 | CLI 场景可完成建档问答、写入 `profile.md`、输出第一阶段计划 |
| 三高相关风险初评 | `private-doctor` | 部分完成 | Stage 3 | 初评回复能覆盖血压 / 血脂 / 血糖背景与主要风险提示 |
| 图片 / 事实自动归档 | `health-archive` | 基线已完成 | Stage 3 | 图片或事实输入后，真实写入并返回明确状态 |
| 图片归档后继续做家庭医生对话 | `health-archive` + `private-doctor` | 部分完成 | Stage 3 | CLI 端到端验证：归档成功后继续输出医生判断与建议 |
| 家庭医生式持续跟踪 | `private-doctor` + `health-review` | 部分完成 | Stage 4 | 多日记录后可输出趋势结论与后续跟踪重点 |
| 日报 / 周报 / 月报 | `health-review` | 规划中 | Stage 4 | 本地 `reviews/` 目录生成稳定复盘结果 |
| 医生速读摘要 / 阶段报告 | `doctor-brief` | 规划中 | Stage 4 | 本地 `reports/` 目录生成医生可读摘要 |
| 提醒机制 | `health-reminders` 或等价调度契约 | 规划中 | Stage 5 | 固定提醒和轻量兜底提醒都可运行 |
| 重置前备份 / 迁移准备 | 重置/迁移 playbook + 可选 `health-storage-feishu` | 规划中 | Stage 5 | 重置旧 agent 前能完成备份和恢复准备 |
| Feishu 备份 / 镜像适配 | `health-storage-feishu` | 规划中，可选 | Stage 5 | 仅作为备份/镜像路径，不影响 local-first 主流程 |
| 不依赖用户人肉验收 | CLI 验收链路 | 规划中 | Stage 5 | 安装、归档、对话、复盘、摘要、提醒基础链路都能由 CLI 自测 |

## 当前判断

当前 skill 集已经有了“归档 + 基础家庭医生对话”的最小闭环，但距离你要的完整 health agent 能力还差三层：

1. 整套安装入口和重置后恢复路径
2. 长期跟踪复盘与医生摘要
3. 提醒机制与 CLI 完整验收

所以 roadmap 的真正收口点不是再补几个脚本，而是把上表全部收成 `done` 或 `done / optional`。
