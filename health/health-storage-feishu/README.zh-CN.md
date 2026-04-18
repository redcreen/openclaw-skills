[English](README.md) | [中文](README.zh-CN.md)

# Health Storage Feishu

`health-storage-feishu` 是 `health` skill 集里的可选备份 / 迁移层。当前版本重点不是强绑 Feishu API，而是先把本地健康工作区导出成可带走、可恢复的 bundle。

## 这是什么

从用户视角看，它解决的是：

- 重置旧 health agent 前，怎么先把现在的健康数据带走
- 重置后，怎么把本地健康工作区恢复回来
- 以后如果要接 Feishu 镜像 / 备份，应该从哪一层接

## 为什么要装它

如果你后面准备重置旧 health agent，这个 skill 的价值会很直接：

- 先做一份本地 bundle 备份
- 以后可恢复到新的本地工作区
- 不需要一开始就把 Feishu 当主存储

## 什么时候用

- 准备重置旧 health agent 前
- 想导出一份本地健康数据 bundle
- 想把 bundle 恢复回本地工作区

## 你会得到什么

通常会得到：

- 导出或恢复状态
- bundle 文件路径
- 包里包含了哪些内容
- 当前使用的是哪个本地健康目录

## 安装

- 安装目录: `health/health-storage-feishu/`
- 必需文件: `SKILL.md`
- 默认外部数据目录: `~/document/personal health`
- 安装要求: 必须允许用户自己选数据路径；Feishu 远端写入默认关闭

## GitHub 直装

- 正式安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-storage-feishu`
- 开发安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health/health-storage-feishu`

## 给维护者看的实现组成

- `SKILL.md`: 备份 / 恢复行为和回复契约
- `scripts/export_health_workspace_bundle.py`: 导出本地健康工作区 bundle
- `scripts/import_health_workspace_bundle.py`: 从 bundle 恢复本地健康工作区

## 使用注意

- 当前版本的重点是本地 bundle 导出 / 恢复
- Feishu 只保留为未来可选镜像 / 备份适配，不是主存储前提
- 不要把“导出 bundle 成功”误说成“已经同步到 Feishu”
