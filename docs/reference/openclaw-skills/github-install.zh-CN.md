[English](github-install.md) | [中文](github-install.zh-CN.md)

# GitHub 安装指引

这份文档定义这个工作区对外发布后的标准安装入口。

## 目标

让用户不需要理解仓库结构，只要把整套 `health` 或单个 skill 的 GitHub 地址粘到 OpenClaw 对话框里即可安装。

## 推荐安装格式

正式发布优先固定到 tag：

```text
安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.1/health
安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.1/health/health-archive
安装技能：https://github.com/redcreen/openclaw-skills/tree/v0.2.1/health/private-doctor
```

开发调试时可以临时指向 `main`：

```text
安装技能：https://github.com/redcreen/openclaw-skills/tree/main/health
```

## 维护者发布步骤

1. 把仓库发布到 GitHub。
2. 为对外可安装版本打 tag，例如 `v0.2.1`。
3. 运行生成器：

```bash
python3 scripts/generate_skill_install_manifest.py --repo redcreen/openclaw-skills --ref v0.2.1 --domain health --format markdown
```

4. 把生成出来的 GitHub URL 或 `安装技能：...` 提示词贴到 release note、README 或交付文档里。

## 为什么优先用 Tag

- `main` 会继续变化，不适合对外承诺稳定安装结果
- `tree/<tag>/<skill-path>` 可以把安装内容固定在一个版本上
- `tree/<tag>/health` 让整套能力有一个稳定入口，同时保留子 skill 的独立安装能力

## 当前约束

- 当前绑定仓库是 `redcreen/openclaw-skills`
- `health/` 目录现在可以作为整套安装入口，因为其中同时有 `SKILL.md` 和 `SKILLSET.json`
- 支持 suite manifest 的宿主可以直接展开多个子 skill；只支持单目录安装的宿主也可以直接安装 `health/` umbrella skill
