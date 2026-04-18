[English](test-plan.md) | [中文](test-plan.zh-CN.md)

# 测试计划

## 范围

验证工作区结构、文档路由、整套安装行为，以及 health V1 的完整 CLI 验收链路。

## 验收用例

- Case: 根索引能正确路由
  - Setup: 打开 `README.zh-CN.md`
  - Action: 检查工作区规则和 skill 集索引
  - Expected Result: 读者能从根页面找到 `health` skill 集、其中的 skill、安装路径和使用注意

- Case: `health` skill 集文档保持独立
  - Setup: 打开 `health/README.zh-CN.md`
  - Action: 检查 health landing 页面
  - Expected Result: 页面只说明 health 相关 skill，不混入 order 领域的行为或安装步骤

- Case: `health` 整套有顶层安装入口
  - Setup: 查看 `health/`
  - Action: 检查整套入口文件
  - Expected Result: `health/` 包含 `SKILL.md`、`agents/openai.yaml` 和 `SKILLSET.json`，因此整套家庭医生能力有一个稳定安装目标

- Case: 每个 health skill 都可独立安装
  - Setup: 查看 `health/health-archive/`、`health/private-doctor/`、`health-review/`、`doctor-brief/`、`health-reminders/`、`health-storage-feishu/`
  - Action: 检查目录内容
  - Expected Result: 每个目录都包含 `SKILL.md`、`agents/openai.yaml` 和一对 README

- Case: 工作区文档明确说明顶层边界
  - Setup: 打开 `docs/architecture.zh-CN.md`
  - Action: 检查目录拓扑和边界规则
  - Expected Result: 文档明确说明顶层 skill 集隔离和单 skill 运行时独立

- Case: 健康数据默认路径允许覆盖
  - Setup: 打开 health 文档
  - Action: 检查安装与配置说明
  - Expected Result: 默认路径是 `~/Documents/personal health`，并且安装时允许用户改路径

- Case: GitHub 直装入口清晰可复制
  - Setup: 打开根 README、`health/README.zh-CN.md` 和单 skill README
  - Action: 检查 GitHub 直装示例
  - Expected Result: 用户能直接复制整套或单个 skill 的 GitHub tree 地址到 OpenClaw 对话框；文档优先推荐 tag 地址

- Case: 重置与迁移指引存在
  - Setup: 打开 `docs/reference/openclaw-skills/health-reset-playbook.zh-CN.md`
  - Action: 检查重置流程
  - Expected Result: playbook 说明了备份、整套重装、恢复和验证流程，并且没有把 Feishu 写成唯一前提

## 手工检查

- 检查仓库文档链接是否都使用相对路径
- 检查公开文档是否具备中英文对应页面
- 检查根 README 没有膨胀成单个 skill 的实现细节页

## 自动化覆盖

当前已具备：

- `python3 scripts/validate_skill_boundaries.py`
  - 检查公开 skill 是否缺少必要文件
  - 检查兄弟 skill 或不同 skill 集之间是否出现运行时引用
- `python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.2.0 --domain health --format json`
  - 生成整套与单个 skill 的 GitHub 安装地址和可复制提示词
- `python3 scripts/accept_health_suite.py --repo redcreen/openclaw-skills --ref v0.2.0`
  - 通过 CLI 验证整套安装、归档、医生对话、复盘、摘要、提醒和 bundle 恢复
