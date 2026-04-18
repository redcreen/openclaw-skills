[English](github-install.md) | [中文](github-install.zh-CN.md)

# GitHub 安装指引

这份文档定义这个工作区对外发布后的标准安装入口。

## 目标

让用户不需要理解仓库结构，只要把单个 skill 的 GitHub 地址粘到 OpenClaw 对话框里即可安装。

## 推荐安装格式

正式发布优先固定到 tag：

```text
安装技能集：https://github.com/redcreen/openclaw-skills/tree/main/health
安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.1.0/health/health-archive
安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.1.0/health/private-doctor
```

开发调试时可以临时指向 `main`：

```text
安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health/health-archive
```

## 维护者发布步骤

1. 把仓库发布到 GitHub。
2. 为对外可安装版本打 tag，例如 `v0.1.0`。
3. 运行生成器：

```bash
python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.1.0 --format markdown
```

4. 把生成出来的 GitHub URL 或 `安装技能：...` 提示词贴到 release note、README 或交付文档里。

## 为什么优先用 Tag

- `main` 会继续变化，不适合对外承诺稳定安装结果
- `tree/<tag>/<skill-path>` 可以把安装内容固定在一个版本上
- 单个 skill 的安装地址天然保持 skill 级隔离，不会把整个 `health/` 误装成一个大 agent

## 当前约束

- 当前绑定仓库是 `redcreen/openclaw-skills`
- `health/` 目录现在可以作为 skill 集安装入口，因为其中有 `SKILLSET.json`，installer 会展开成多个 skill 安装
