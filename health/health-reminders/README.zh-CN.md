[English](README.md) | [中文](README.zh-CN.md)

# Health Reminders

`health-reminders` 是 `health` skill 集里的提醒契约层。它负责管理“什么时候该提醒什么”，并判断当前有没有到点的提醒。

## 这是什么

从用户视角看，它解决的是：

- 什么时候该测体重 / 血压
- 什么时候该记用药
- 什么时候该复盘
- 后面如果接定时器，应该提醒什么

它不是聊天本身，而是提醒能力背后的规则层。

## 为什么要装它

如果没有提醒层，健康管理很容易变成：

- 想起来才测
- 有空才记
- 一周过去了才发现没跟上

`health-reminders` 的作用就是把“该提醒什么”变成可保存、可检查、可自动化接出的本地规则。

## 什么时候用

- 想设体重晨测提醒
- 想设血压复测提醒
- 想设运动或复盘提醒
- 想让系统判断“现在有什么提醒到点了”

## 你会得到什么

通常会得到：

- 当前有哪些提醒规则
- 现在有没有到点的提醒
- 为什么这条提醒会触发
- 接下来应该做什么

## 第一次怎么开始

最简单的方式是先设 1-2 条固定提醒。

例如：

```text
每天早上 8 点提醒我测体重
每天晚上 9 点提醒我复盘当天健康记录
```

## 推荐搭配

提醒要真正有意义，最好前面已经装了：

- `health-archive`
- `private-doctor`
- `health-review`

这样提醒触发后，后面的记录、解读和复盘才能接得上。

## 安装

- 安装目录: `health/health-reminders/`
- 必需文件: `SKILL.md`
- 默认外部数据目录: `~/document/personal health`
- 安装要求: 必须允许用户自己选数据路径，且 Feishu 默认关闭

## GitHub 直装

- 正式安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-reminders`
- 开发安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health/health-reminders`

## 给维护者看的实现组成

- `SKILL.md`: 提醒规则和回复契约
- `scripts/health_reminders.py`: 管理提醒规则并判断当前到点提醒

## 使用注意

- 它解决的是“提醒规则”和“到点判断”，不是替代完整调度系统
- 真正的推送渠道后面可以再接，但 reminder 规则必须先落到本地
- 结果默认写入 `reminders/`
