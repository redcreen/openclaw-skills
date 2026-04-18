[English](README.md) | [中文](README.zh-CN.md)

# Doctor Brief

`doctor-brief` 是 `health` skill 集里面向医生的摘要层。它把本地健康记录整理成医生更容易快速阅读的一页式材料。

## 这是什么

从用户视角看，`doctor-brief` 解决的是：

- 平时记录了很多，但去看医生时不好讲清楚
- 想把最近体重、血压、运动、症状、用药变化整理成重点
- 希望医生快速看懂最近这段时间发生了什么

它不是“每天都要用”的 skill，而是“就医前特别有价值”的 skill。

## 为什么要装它

它的价值是把零散记录变成医生可读摘要：

- 不用临时翻聊天
- 不用自己手工整理时间线
- 能把重点问题压缩成医生更容易消化的内容

## 什么时候用

- 线下就医前
- 想把最近一阶段情况整理给医生看
- 想做一次阶段性医生摘要

## 你会得到什么

通常会得到：

- 基本档案摘要
- 最近趋势重点
- 当前用药背景
- 近期症状或异常信号
- 建议向医生重点确认的问题

## 第一次怎么开始

最自然的方式是直接告诉它：

```text
帮我做一份最近 30 天的医生摘要
把最近体重、血压、用药和症状整理成给医生看的版本
```

## 推荐搭配

它最好和这些 skill 一起用：

- `health-archive`
- `private-doctor`
- `health-review`

这样医生摘要才有足够的本地记录和阶段复盘可用。

## 安装

- 安装目录: `health/doctor-brief/`
- 必需文件: `SKILL.md`
- 默认外部数据目录: `~/document/personal health`
- 安装要求: 必须允许用户自己选数据路径，且 Feishu 默认关闭

## GitHub 直装

- 正式安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.1.0/health/doctor-brief`
- 开发安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health/doctor-brief`

## 给维护者看的实现组成

- `SKILL.md`: 医生摘要行为和回复契约
- `scripts/generate_doctor_brief.py`: 生成医生可读摘要

## 使用注意

- 医生摘要必须基于本地记录，不靠聊天印象拼凑
- 目标是“医生快速看懂”，不是堆很多原始数据
- 摘要结果默认写入 `reports/`
