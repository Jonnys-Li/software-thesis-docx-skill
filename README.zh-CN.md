# software-thesis-docx

从真实软件项目仓库出发，构建和修订毕业论文 `DOCX` 工作流。

English documentation: [README.md](README.md)

## 30 秒安装

### Codex 原生安装

```text
$skill-installer install https://github.com/Jonnys-Li/software-thesis-docx-skill/tree/main/skills/software-thesis-docx
```

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/Jonnys-Li/software-thesis-docx-skill/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/Jonnys-Li/software-thesis-docx-skill/main/install.ps1 | iex
```

安装后重启 Codex，新的 skill 才会被加载。

## 快速试用

```text
Use $software-thesis-docx to turn my software project repo into a structured thesis manifest and generate a DOCX.
Use $software-thesis-docx to replace thesis figures by caption without changing Word layout.
Use $software-thesis-docx to normalize in-text citations and terminology in an existing DOCX.
```

## 兼容性

- Codex：当前已适配
- OpenCode：计划中
- Claude Code：计划中

## 这个仓库包含什么

- 根目录分发文件：`README`、版本说明、一键安装脚本
- 真实可复用的 skill：`skills/software-thesis-docx/`
- 3 个参数化 DOCX 工具：生成、按图注换图、精确段落改写
- 公开示例与方法论文档，便于迁移到其他论文项目

## 仓库结构

```text
.
├── install.py
├── install.sh
├── install.ps1
├── docs/
└── skills/software-thesis-docx/
```

## 官方安装目标

Codex 官方推荐安装入口是：

```text
https://github.com/Jonnys-Li/software-thesis-docx-skill/tree/main/skills/software-thesis-docx
```

这个目录里包含：

- `SKILL.md`
- `agents/openai.yaml`
- `assets/examples/`
- `references/`
- `scripts/`
- `requirements.txt`

## 文档

- [Codex 快速上手](docs/codex-quickstart.zh-CN.md)
- [v0.2.0 版本说明](docs/releases/v0.2.0.md)
- [v0.1.0 版本说明](docs/releases/v0.1.0.md)

## 方法原则

- 先基于代码仓库事实，再组织论文内容
- 把内容放进结构化输入，而不是把正文硬编码进 Python
- 图片替换优先按图注定位，不按“第几张图”这种脆弱逻辑
- 文本改写优先整段精确匹配，减少对 Word 格式的破坏
- 每次重要 DOCX 变更后都做一次可视化校验

## 使用边界

- 段落改写脚本只适合“整段全文精确命中”的场景
- 多 `run`、混合格式、修订痕迹较多的段落需要先人工检查
- 学校格式要求如果更特殊，通常需要扩展 manifest 或样式逻辑

## 下一步

- 增加 OpenCode 兼容的打包与安装方式
- 增加 Claude Code 的接入方式与提示词约定
- 增加跨运行时 smoke test，覆盖 Codex、OpenCode、Claude Code

## 许可证

[MIT](LICENSE)
