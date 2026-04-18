# 开发计划

## 这份计划的作用

这份计划把路线图进一步展开成工作区可执行的实施队列。

## 使用方式

- 用 `docs/roadmap.zh-CN.md` 看里程碑顺序
- 用这份文件看详细执行队列
- 用 `.codex/plan.md` 看当前执行线

## 当前所处位置

工作区已经完成 `health` 的首轮功能和安装模板建设，当前进入 `Stage 5` 的发布与防漂移阶段。

## Stage 1: 工作区治理基线

### 目标

把仓库定义成一个带根索引、长期文档和模块控制面的多 skill 集工作区。

### 状态

已完成。

### 已完成工作

- 根 README 对改成工作区索引
- 补齐架构、路线图和测试计划
- 增加模块化 `.codex` 控制层

## Stage 2: Health Skill 集基线

### 目标

把 `health/` 建成第一个隔离的 skill 集根目录，并补出标准 skill 目录和公开文档。

### 状态

已完成。

### 已完成工作

1. 创建 `health` landing README 对。
2. 创建 `health-archive` 标准 skill 目录。
3. 创建 `private-doctor` 标准 skill 目录。
4. 在 skill 集文档中写清安装和存储预期。

## Stage 3: Health-Archive 功能交付

### 目标

交付 local-first 的健康归档能力，并明确返回记录成功状态。

### 状态

已完成。

### 已完成工作

1. 定义 `~/document/personal health` 的本地存储契约。
2. 增加归档格式和字段命名参考文档。
3. 实现 `scripts/archive_health_record.py`。
4. 把 skill 工作流收敛到以脚本结果作为唯一成功依据。
5. 用本地烟测验证了落盘和重复重放去重行为。

## Stage 4: Private-Doctor 功能交付

### 目标

交付一个简洁的家庭医生型 skill，能解释、建议、规划，而不是被动记录。

### 状态

已完成。

### 已完成工作

1. 增加 `scripts/summarize_health_workspace.py`。
2. 增加 `scripts/update_health_profile.py`。
3. 增加 `scripts/render_doctor_reply.py`。
4. 增加 `scripts/validate_doctor_reply.py`。
5. 增加家庭医生工作流、建档和回复契约参考文档。
6. 用同一份本地健康工作区验证了摘要、档案更新和医生回复渲染行为。

## Stage 5: 未来 Skill 集扩展与防漂移

### 目标

后续新增 skill 集时不混领域，也不重新陷入结构漂移。

### 状态

进行中。

### 已完成工作

1. 增加跨 skill 运行时引用的隔离检查 `scripts/validate_skill_boundaries.py`。
2. 增加 GitHub 直装参考文档。
3. 增加 `scripts/generate_skill_install_manifest.py`，用于批量生成每个 skill 的安装地址和提示词。
4. 把根 README、`health` landing 和单 skill README 全部接到 GitHub 直装模板上。
5. 绑定真实仓库 `redcreen/openclaw-skills`。
6. 确定第一个稳定安装 tag 为 `v0.1.0`。

### 执行队列

1. 跑一次从 GitHub 地址出发的安装验收。
2. 决定未来 release 是否自动刷新 README 中的 tag 地址。
3. 只有在第一个 order skill 明确后才创建 `order/` 模块。
4. 随着工作区扩展，继续补模块级验证和发布指引。
