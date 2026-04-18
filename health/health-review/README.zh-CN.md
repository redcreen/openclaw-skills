[English](README.md) | [中文](README.zh-CN.md)

# Health Review

`health-review` 是 `health` skill 集里的长期复盘层。它把已经入档的健康记录整理成日复盘、周总结或阶段性回顾。

## 这是什么

从用户视角看，`health-review` 解决的是：

- 你不只想看单次数据
- 你想知道这一周 / 这一阶段到底是变好了还是跑偏了
- 你想要简短复盘，而不是自己翻聊天记录

如果 `private-doctor` 更像“当下的家庭医生判断”，`health-review` 更像“隔一段时间帮你做阶段复盘”。

## 为什么要装它

它的价值在于把零散记录变成趋势结论：

- 不只看单次波动
- 帮你看最近几天或一周的方向
- 让后续建议更有连续性

## 什么时候用

- 想看今天的简短回顾
- 想看最近一周有没有跑偏
- 想做阶段性复盘
- 想把本地记录整理成一份简短 review

## 你会得到什么

通常会得到：

- 复盘周期
- 这段时间的核心变化
- 需要重点留意的地方
- 下一阶段最该抓什么

## 第一次怎么开始

最简单的方式是直接要求它做一份周总结。

例如：

```text
帮我做最近一周的健康复盘
把这几天的体重、血压和运动做个小结
```

## 推荐搭配

要想 review 有意义，前面最好已经装了：

- `health-archive`
- `private-doctor`

这样本地工作区里已经有可复盘的记录。

## 安装

- 安装目录: `health/health-review/`
- 必需文件: `SKILL.md`
- 默认外部数据目录: `~/document/personal health`
- 安装要求: 必须允许用户自己选数据路径，且 Feishu 默认关闭

## GitHub 直装

- 正式安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-review`
- 开发安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health/health-review`

## 给维护者看的实现组成

- `SKILL.md`: 复盘行为和短回复契约
- `scripts/generate_health_review.py`: 生成日 / 周 / 月 review

## 使用注意

- review 必须基于已归档记录，而不是凭聊天印象总结
- 结论要以趋势为主，不夸大单次异常
- 复盘结果默认写入 `reviews/`
