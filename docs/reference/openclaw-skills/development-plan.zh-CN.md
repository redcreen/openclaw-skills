[English](development-plan.md) | [中文](development-plan.zh-CN.md)

# 开发计划

## 这份计划的作用

这份计划把路线图进一步展开成工作区可执行的实施队列。

## 使用方式

- 用 `docs/roadmap.zh-CN.md` 看里程碑顺序
- 用这份文件看详细执行队列
- 用 `.codex/plan.md` 看当前执行线

## 当前所处位置

工作区已经完成 `health` 的基线交付，但还没有完成你真正想要的 health agent 能力闭环。下一步要做的是把现有 skill 集补成一个“可重置、可整套安装、可持续当家庭医生使用”的完整方案。

## Health V1 收口目标

这次路线图收口时，需要同时满足以下目标：

1. 重置旧 health agent 后，可以用一条命令安装整套 `health` skill 集。
2. 安装完成后，agent 能像家庭医生一样主动建档、自动记录图片/事实，并继续对话解释和给建议。
3. 长期跟踪、阶段复盘、医生摘要和提醒能力都由 skill 集承接，而不是依赖旧 agent。
4. CLI 验收链路必须完整，不能把基本功能测试甩给用户人肉验证。
5. Feishu 只保留为可选备份/镜像适配器，不再作为主存储前提。

## Stage 1: 工作区与 local-first 基线

### 目标

把仓库定义成一个带根索引、长期文档和模块控制面的多 skill 集工作区，并建立 `health` 的 local-first 基线。

### 状态

已完成。

### 已完成工作

- 根 README 对改成工作区索引
- 补齐架构、路线图和测试计划
- 增加模块化 `.codex` 控制层
- 把健康数据基线收口到 `~/document/personal health`

## Stage 2: 归档与家庭医生基线

### 目标

交付 `health-archive` 与 `private-doctor` 的基线闭环，让健康数据可以 local-first 地记录和解释。

### 状态

已完成。

### 已完成工作

1. 创建 `health` landing README 对。
2. 创建 `health-archive` 与 `private-doctor` 标准 skill 目录。
3. 定义 `~/document/personal health` 的本地存储契约。
4. 实现归档、医生摘要、档案更新、回复渲染与基础校验脚本。
5. 公开 GitHub 安装入口并发布 `v0.1.0`。

## Stage 3: Health 整套安装与医生核心能力补齐

### 目标

补齐“整套安装 + 主动建档 + 三高初评 + 图片归档后继续医生对话”的核心能力，做到重置旧 health agent 后可以直接从 skill 集恢复。

### 状态

进行中。

### 已有基础

1. `health-archive` 已具备 local-first 归档能力。
2. `private-doctor` 已具备基础建档、解读与回复渲染能力。
3. 仓库已经公开发布，并有 tag 安装入口。

### 执行队列

1. 明确 `health` 整套安装分发模型：
   - 目标是一条命令安装多个 health skill
   - 不是把 `health/` 伪装成一个带 `SKILL.md` 的大一统 skill
2. 交付 `health` 整套安装入口：
   - 生成 bundle manifest 或安装脚本
   - 文档化一键安装方式
3. 扩充 `private-doctor` 的基础档案 schema：
   - 基本信息
   - 当前目标
   - 三高背景
   - 当前用药
   - 生活方式
   - 当前主要困扰
4. 补齐医生核心能力：
   - 主动建档问答
   - 基础风险初评
   - 第一阶段行动建议
   - 后续跟踪重点
5. 把“图片归档后继续医生对话”变成 CLI 可验证链路：
   - 图片/事实 -> 归档成功
   - 读取本地工作区 -> 输出医生判断
   - 不依赖用户手工测试
6. 决定 archive 是否需要多图片单次会话助手，以适应用户一次发多张图的真实场景。

### 完成标准

- 一条命令可安装整套 `health` skill 集
- 重置旧 agent 后可直接恢复核心健康能力
- CLI 端到端测试能证明图片归档后可以继续做家庭医生式对话

## Stage 4: 长期跟踪复盘与医生摘要

### 目标

交付长期跟踪、阶段复盘和医生可读摘要能力，让 skill 集不只是“会记录 + 会解读”，而是能持续管理。

### 状态

计划中。

### 执行队列

1. 新增 `health-review` skill：
   - 日复盘
   - 周总结
   - 月度 / 阶段性复盘
2. 让复盘产物落到本地工作区：
   - `reviews/`
   - 可追溯的 review 元数据
3. 新增 `doctor-brief` skill：
   - 医生速读摘要
   - 阶段性就医资料
4. 让医生摘要落到本地工作区：
   - `reports/`
   - 统一输出格式
5. 增加 CLI 验收：
   - 从本地记录生成 review
   - 从本地记录生成 doctor brief

### 完成标准

- `health-review` 与 `doctor-brief` 可用
- 本地 `reviews/` 与 `reports/` 目录不再只是约定
- 用户的长期跟踪和就医支持能力由 skill 集承接

## Stage 5: 提醒自动化迁移与 Health V1 收口

### 目标

交付提醒、重置/迁移准备和 health V1 最终验收，确保技能集真正能替代当前旧 health agent。

### 状态

计划中。

### 执行队列

1. 新增 `health-reminders` 能力或等价调度契约：
   - 固定提醒
   - 轻量兜底提醒
   - 不把所有定时逻辑硬塞进主 skill
2. 补齐迁移/重置方案：
   - 重置旧 health agent 前的备份流程
   - Feishu 数据备份或导出
   - 重置后如何恢复到本地工作区
3. 评估并决定可选的 `health-storage-feishu` 适配器：
   - 仅作为镜像/备份
   - 不作为主存储前提
4. 建立 CLI 完整验收链路：
   - 整套安装
   - 图片归档
   - 家庭医生对话
   - 复盘
   - 医生摘要
   - 提醒基础路径
5. 以 CLI 验收结果作为 release gate，不把基本功能测试甩给用户。

### 完成标准

- 你可以先备份旧数据，再重置旧 health agent
- 新 agent 通过安装整套 `health` skill 集恢复完整能力
- 核心能力已经由 CLI 端到端验证过
