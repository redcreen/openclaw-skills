# Health Archive

`health-archive` 是 local-first 健康记录体系里的接收和归档 skill。它负责把收到的测量数据和健康证据写进用户的外部健康目录，并明确返回归档状态。

## 安装

- 安装目录: `health/health-archive/`
- 必需文件: `SKILL.md`
- 默认外部数据目录: `~/document/personal health`
- 安装要求: 必须让用户自己选择数据路径，不能写死个人路径

## GitHub 直装

- 正式安装:
  - `安装技能：https://github.com/<owner>/<repo>/tree/<tag>/health/health-archive`
- 开发安装:
  - `安装技能：https://github.com/<owner>/<repo>/tree/main/health/health-archive`
- 如果维护者已经发布了 release，可直接把上面的地址粘到 OpenClaw 对话框里。

## 运行组成

- `SKILL.md`: 归档流程和回复契约
- `scripts/archive_health_record.py`: 确定性的本地落盘脚本
- `references/archive-format.zh-CN.md`: 存储契约和 payload 结构
- `references/field-map.zh-CN.md`: 标准字段命名

## 适用场景

- 用户发来体重或血压图片
- 用户发来运动截图，希望直接入档
- 用户想确认某条健康信息是否真的已经记录成功

## 脚本示例

```bash
python3 scripts/archive_health_record.py --payload-file /tmp/health-archive-payload.json
```

## 使用注意

- 本地文件才是真实存储
- 必须先备份原始证据，再宣称记录成功
- 脚本会写入 `records.md`、`raw/YYYY/MM/DD/` 和 `archive-log.jsonl`
- Feishu 默认关闭
- 类型不够确定时，也应当诚实地以 `unknown-health` 这类类型保存，而不是假装识别完全正确
- 对外发布时优先使用 tag 地址，不要默认让用户安装 `main`
