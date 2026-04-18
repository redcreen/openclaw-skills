[English](README.md) | [中文](README.zh-CN.md)

# Health Archive

`health-archive` 是 local-first 健康记录体系里的接收和归档 skill。它负责把收到的测量数据和健康证据写进用户的外部健康目录，并明确返回归档状态。

## 这是什么

从用户视角看，`health-archive` 是“发图片以后到底有没有真的记住”的那一层。

它主要解决的是：

- 你发了体重图、血压图、运动图
- 你不想只听到一句模糊的“记了”
- 你需要它明确告诉你：有没有写入、写到了哪里、识别到了什么

如果 `private-doctor` 更像家庭医生，`health-archive` 就像家庭医生背后的记录台账系统。

## 为什么要装它

它最直接的价值不是“分析”，而是“可信记录”：

- 明确告诉你有没有真的记录成功
- 原图会备份，不只是识别一下数字就算完
- 后面的医生判断能基于真实落盘的数据，而不是基于聊天记忆

如果你最在意的是“我发的图片到底有没有被记下来”，这个 skill 就是第一优先级。

## 什么时候用

这些场景都适合：

- 发体重图
- 发血压图
- 发运动截图
- 发睡眠、症状、用药相关图片或明确事实
- 想确认“这一条有没有真的入档”

## 你会得到什么结果

理想中的回复不应该只是“已记录”，而应该至少包含：

- `记录状态`
- `识别到的关键数据`
- `保存位置`
- `一行简短判断`

也就是说，它首先要解决“有没有记住”，然后才是“这组数据大概怎么看”。

## 第一次怎么开始

最简单的开始方式就是直接发一张图，并明确告诉它要记录。

例如：

```text
这是我今天早上的体重图，帮我记一下
这是今天的血压图，记录后告诉我有没有成功写入
这是我今天的运动截图，帮我入档
```

## 它不会替你做什么

`health-archive` 的重点是记录，不是长期解释和规划。

它不会替代：

- 长期趋势分析
- 完整家庭医生式建议
- 周 / 月复盘
- 医生摘要

这些能力更多由 `private-doctor` 和其他已安装的 health skill 承接。

## 推荐搭配

如果你只想先解决“发图后到底有没有被记住”，只装它也可以。

如果你想要完整体验，推荐至少搭配：

- `health-archive`
- `private-doctor`

## 安装

- 安装目录: `health/health-archive/`
- 必需文件: `SKILL.md`
- 默认外部数据目录: `~/Documents/personal health`
- 安装要求: 必须让用户自己选择数据路径，不能写死个人路径

## GitHub 直装

- 正式安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.0/health/health-archive`
- 开发安装:
  - `安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health/health-archive`
- 如果维护者已经发布了 release，可直接把上面的地址粘到 OpenClaw 对话框里。

## 给维护者看的实现组成

- `SKILL.md`: 归档流程和回复契约
- `scripts/archive_health_record.py`: 确定性的本地落盘脚本
- `scripts/archive_health_session.py`: 一次归档多条健康记录
- `references/archive-format.zh-CN.md`: 存储契约和 payload 结构
- `references/field-map.zh-CN.md`: 标准字段命名

## 脚本示例

```bash
python3 scripts/archive_health_record.py --payload-file ./health-archive-payload.json
```

## 使用注意

- 本地文件才是真实存储
- 必须先备份原始证据，再宣称记录成功
- 脚本会写入 `records.md`、`raw/YYYY/MM/DD/` 和 `archive-log.jsonl`
- Feishu 默认关闭
- 类型不够确定时，也应当诚实地以 `unknown-health` 这类类型保存，而不是假装识别完全正确
- 一次收到多张图或多条数据时，可以走 session 归档脚本而不是硬拆多轮
- 对外发布时优先使用 tag 地址，不要默认让用户安装 `main`
