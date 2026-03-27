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
Use $software-thesis-docx to turn my project repo into a structured thesis manifest and generate a DOCX with the built-in academic preset.
Use $software-thesis-docx to read my school Word template, extract a custom style preset, and build the thesis in that format.
Use $software-thesis-docx to generate Mermaid architecture and sequence diagrams for my thesis from the repository structure.
Use $software-thesis-docx to run an AIGC risk check on my thesis DOCX and only rewrite the flagged single-run paragraphs if I approve it.
Use $software-thesis-docx to lower AIGC for my thesis and switch to explicit_low_aigc mode only for the authorized paragraphs.
```

## 这次新增了什么

- 一个内置的学术论文编排 preset，来源于真实排版样本，但不公开原始私有文档
- 运行时从用户提供的 `.docx` 模板中抽取自定义样式 preset
- 支持 `formatting` 配置的 manifest 驱动 DOCX 构建
- 面向论文插图的 Mermaid 请求契约，支持架构图、时序图、ER 图、状态图、甘特图、类图和脑图
- 可选的严谨写作 subagent 模式，默认关闭
- 基于真实样本抽象出的 AIGC 风险检查与双模式降重流程，默认关闭且默认走 `academic_safe`

## 兼容性

- Codex：当前已适配
- OpenCode：计划中
- Claude Code：计划中

## 这个仓库包含什么

- 根目录分发文件：`README`、版本说明、一键安装脚本
- 真实可复用的 skill：`skills/software-thesis-docx/`
- 6 个用户可直接运行的脚本与 1 个共享 helper：
  - `build_docx_from_manifest.py`
  - `extract_docx_style_preset.py`
  - `replace_images_by_caption.py`
  - `rewrite_paragraphs.py`
  - `check_aigc_risk.py`
  - `rewrite_low_aigc_docx.py`
  - `aigc_utils.py`
- 公开示例：manifest、workflow options、Mermaid 请求、图片映射、段落改写
- 方法论文档：格式 preset、Mermaid、交互 intake、AIGC 评估、低 AIGC playbook、repo-to-thesis 工作流

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
- `assets/presets/`
- `references/`
- `scripts/`
- `requirements.txt`

## 文档

- [Codex 快速上手](docs/codex-quickstart.zh-CN.md)
- [v0.4.0 版本说明](docs/releases/v0.4.0.md)
- [v0.3.0 版本说明](docs/releases/v0.3.0.md)
- [v0.2.0 版本说明](docs/releases/v0.2.0.md)
- [v0.1.0 版本说明](docs/releases/v0.1.0.md)

## 方法原则

- 先基于代码仓库事实，再组织论文内容
- 把内容放进结构化输入，而不是把正文硬编码进 Python
- 通过内置或抽取出的 style preset 把内容和排版分离
- 图片替换优先按图注定位，不按“第几张图”这种脆弱逻辑
- 文本改写优先整段精确匹配，减少对 Word 格式的破坏
- Mermaid 与 AIGC 评估都是显式开关，不默认强制开启
- 默认只做保守 AIGC 检查，只有用户明确提出“降低 AIGC”时才启用 `explicit_low_aigc`

## 使用边界

- Mermaid 当前只负责生成代码或 `.mmd` 文件，不负责自动渲染图片或自动插入 DOCX
- 段落改写脚本只适合“整段全文精确命中”的场景
- 多 `run`、混合格式、修订痕迹较多的段落需要先人工检查
- AIGC 检测是样本驱动的本地启发式评估，不承诺对齐第三方平台分值
- 学校格式要求如果更特殊，通常需要扩展 manifest 或 preset 逻辑

## 下一步

- 增加 OpenCode 兼容的打包与安装方式
- 增加 Claude Code 的接入方式与提示词约定
- 增加跨运行时 smoke test，覆盖 Codex、OpenCode、Claude Code
- 增强复杂学校模板的样式抽取与前置页支持

## 许可证

[MIT](LICENSE)
