# 2026-04-18 GitHub 安装入口整改

## 背景

工作区已经有了按 skill 隔离的结构和 README，但对外安装入口还停留在“让用户自己去仓库里找目录”。这不适合做可复用 skill，也容易让用户误装整个 skill 集目录。

## 问题

- 安装路径只写在 README 里，不够直接
- 还没有标准的“复制到 OpenClaw 对话框”的安装格式
- 仓库没有真实 remote 时，维护者也缺一个统一方法来批量生成安装地址

## 决策

采用 `GitHub tree URL + 单条安装提示词` 作为标准公开安装入口：

- 中文：`安装技能：https://github.com/<owner>/<repo>/tree/<ref>/<skill-path>`
- English: `Install skill: https://github.com/<owner>/<repo>/tree/<ref>/<skill-path>`

对外正式发布优先使用 tag，不默认推荐 `main`。

## 实施

1. 新增 `scripts/generate_skill_install_manifest.py`，从仓库结构自动发现可安装 skill，并生成 GitHub URL 和可复制提示词。
2. 新增 GitHub 安装参考文档。
3. 更新根 README、`health` landing 和两个 health skill README，把 GitHub 直装入口写成公开契约。
4. 把测试计划和状态文档同步到这套安装模型。

## 结果

- 每个 skill 都具备统一的 GitHub 直装模板
- 维护者可以在 release 前批量生成安装地址
- 安装入口和 skill 级隔离保持一致，不会把整个 `health/` 混成一个安装单元

## 后续

- 绑定真实 `owner/repo` 和第一个稳定 tag
- 从真实 GitHub 地址出发跑一次安装验收
