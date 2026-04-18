[English](health-reset-playbook.md) | [中文](health-reset-playbook.zh-CN.md)

# Health 重置 Playbook

这份 playbook 定义了如何安全地把旧 health agent 替换成 skill 化的 `health` 套件。

## 目标

- 在重置前保住现有健康数据
- 用一个稳定 GitHub 地址装回新的整套能力
- 重置后把 local-first 健康工作区恢复回来
- 用 CLI 先证明替换路径成立，而不是把基础验证甩给用户

## 重置旧 Agent 前

1. 先确认当前健康数据还分散在哪些地方：
   - 当前 local-first 工作区 `~/Documents/personal health`
   - 旧工作区 `~/.openclaw/workspace-health/`
   - 仍保存独有记录的 Feishu 表或文档
2. 先把当前 local-first 工作区导出成 bundle：

   ```bash
   python3 health/health-storage-feishu/scripts/export_health_workspace_bundle.py --data-root "~/Documents/personal health" --format zip
   ```

3. 如果旧工作区里还有没有回写到 local-first 工作区的笔记或报告，重置前先单独备份那份目录。
4. 如果 Feishu 里还有本地没有的独有记录，也要先导出或截图留存。当前 skill 集不依赖 Feishu，也不会假装能自动拉回所有旧 Feishu 数据。

## 安装新的替代套件

正式整套安装入口：

```text
安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health
```

如果你只想装单个能力，也可以单独安装 `health/health-archive/` 之类的子 skill，但重置替换场景通常应该直接装整套。

## 恢复本地工作区

把 bundle 恢复回新的本地健康目录：

```bash
python3 health/health-storage-feishu/scripts/import_health_workspace_bundle.py \
  --bundle-file /path/to/health-bundle.zip \
  --data-root "~/Documents/personal health" \
  --overwrite
```

## 验证清单

恢复后，至少确认：

- 目标目录下存在 `profile.md`
- 目标目录下存在 `records.md`
- 如果之前做过原图备份，`raw/` 还在
- 如果之前用过复盘、摘要、提醒，`reviews/`、`reports/`、`reminders/` 目录还在
- agent 可以基于恢复后的工作区继续做 summary、review 或 doctor brief

## CLI 验收

仓库级完整验收已经由下面的脚本承接：

```bash
python3 scripts/accept_health_suite.py --repo redcreen/openclaw-skills --ref v0.2.0
```

这条验收链路已经覆盖：

- 整套安装
- 单条归档和多条 session 归档
- 家庭医生建档、初评、回复渲染
- 复盘生成
- 医生摘要生成
- 提醒
- bundle 导出与恢复

## 边界说明

- 新套件是 local-first，Feishu 是可选项，不是恢复前提
- 这份 playbook 不会假装所有旧 Feishu 部署都能在没有用户级凭证的情况下自动导入
- 在确认所有独有数据都至少备份或导出一次之前，不要重置旧 agent
