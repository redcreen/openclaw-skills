# Health Skill 集

这个目录存放个人健康相关的可安装 skill。整个 skill 集采用 local-first 方案，健康数据放在仓库之外。

## 本 Skill 集规则

- 所有运行时行为都收敛在 `health/` 里
- 不允许把 order 或其他非健康领域逻辑混进这个 skill 集
- 按单个 skill 安装，不把整个目录伪装成一个大一统 agent
- 默认外部数据目录是 `~/document/personal health`，但安装时必须允许用户修改
- V1 默认关闭 Feishu

## Skill 列表

| Skill | 作用 | 安装路径 | 适用场景 | 备注 |
| --- | --- | --- | --- | --- |
| [`health-archive`](health-archive/README.zh-CN.md) | 把测量数据、截图和健康事实归档到本地记录，并明确回报是否成功 | `health/health-archive/` | 用户发来体重、血压、运动、睡眠、症状等需要记录的健康信息 | 第一优先交付 |
| [`private-doctor`](private-doctor/README.zh-CN.md) | 像简洁的家庭医生一样基于本地健康记录做解读、建议和规划 | `health/private-doctor/` | 用户需要建档、解读、趋势复盘、建议或后续规划 | 不允许退化成只会记账的记录员 |

## GitHub 直装模板

发布后，推荐把具体 skill 的 GitHub tree 地址直接发给用户。

- `health-archive`
  - `安装技能：https://github.com/<owner>/<repo>/tree/<tag>/health/health-archive`
- `private-doctor`
  - `安装技能：https://github.com/<owner>/<repo>/tree/<tag>/health/private-doctor`
- 维护者批量生成:
  - `python3 scripts/generate_skill_install_manifest.py --repo <owner>/<repo> --ref <tag> --domain health`

## 数据根目录

这个 skill 集的默认外部数据目录是 `~/document/personal health`。

建议结构：

```text
~/document/personal health/
  profile.md
  records.md
  raw/
  reviews/
  reports/
```
