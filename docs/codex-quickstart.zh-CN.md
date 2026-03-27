# Codex 快速上手

这份说明用于在 Codex 中最快安装并使用 `software-thesis-docx`。

## 1. 安装 Skill

### Codex 官方安装入口

```text
$skill-installer install https://github.com/Jonnys-Li/software-thesis-docx-skill/tree/main/skills/software-thesis-docx
```

### macOS / Linux 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/Jonnys-Li/software-thesis-docx-skill/main/install.sh | bash
```

### Windows PowerShell 一键安装

```powershell
irm https://raw.githubusercontent.com/Jonnys-Li/software-thesis-docx-skill/main/install.ps1 | iex
```

安装完成后重启 Codex。

## 2. 安装后的目录结构

安装后的 skill 目录应至少包含：

- `SKILL.md`
- `agents/openai.yaml`
- `assets/examples/`
- `assets/presets/`
- `references/`
- `scripts/`
- `requirements.txt`

关键点是 `SKILL.md` 必须位于安装后的 skill 根目录。

## 3. 现在支持什么

- 基于 manifest 的论文 DOCX 生成
- 按图注替换图片
- 面向格式保真的精确段落改写
- 内置学术论文编排 preset
- 从 `.docx` 模板抽取自定义 style preset
- Mermaid 规划契约
- 可选的严谨写作 subagent 模式
- 可选的 AIGC 风险检查与双模式降重流程

## 4. 在 Codex 中使用

可以直接这样发起：

```text
Use $software-thesis-docx to build my thesis DOCX workflow from my software repository and ask me whether to use the default preset, Mermaid generation, subagents, and AIGC checks.
```

常见提示词示例：

- `Use $software-thesis-docx to turn my project repo into a structured thesis manifest and generate a DOCX with the built-in preset.`
- `Use $software-thesis-docx to read my Word template, extract a style preset, and build the thesis in that format.`
- `Use $software-thesis-docx to generate Mermaid flowchart and sequenceDiagram code for my thesis based on the repo architecture.`
- `Use $software-thesis-docx to run an AIGC risk review on my thesis DOCX and only rewrite the flagged single-run paragraphs after showing me the report.`
- `Use $software-thesis-docx to lower AIGC for my thesis, keep academic_safe by default, and only switch to explicit_low_aigc if I explicitly ask for it.`

## 5. 可选依赖安装

如果当前 Python 环境里还没有所需依赖，可以执行：

```bash
python3 -m pip install -r "$HOME/.codex/skills/software-thesis-docx/requirements.txt"
```

如果你设置了自定义 `CODEX_HOME`，把路径替换成对应目录即可。

## 6. 直接运行脚本

根据示例 manifest 构建论文：

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/build_docx_from_manifest.py" \
  --manifest "$HOME/.codex/skills/software-thesis-docx/assets/examples/thesis_manifest.example.json" \
  --output /tmp/example-thesis.docx
```

从学校模板抽取 preset：

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/extract_docx_style_preset.py" \
  --input school-template.docx \
  --output /tmp/style-preset.json
```

用自定义 preset 构建论文：

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/build_docx_from_manifest.py" \
  --manifest thesis_manifest.json \
  --style-preset /tmp/style-preset.json \
  --output /tmp/custom-thesis.docx
```

运行 AIGC 风险检查：

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/check_aigc_risk.py" \
  --input thesis.docx \
  --output /tmp/aigc-risk-report.json
```

按风险报告回写低 AIGC 版本：

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/rewrite_low_aigc_docx.py" \
  --input thesis.docx \
  --report /tmp/aigc-risk-report.json \
  --output /tmp/thesis-low-aigc.docx \
  --pending-output /tmp/aigc-pending-review.json \
  --profile academic_safe \
  --normalize-typography
```

按图注替换图片：

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/replace_images_by_caption.py" \
  --input thesis.docx \
  --output thesis-images-updated.docx \
  --mapping "$HOME/.codex/skills/software-thesis-docx/assets/examples/image_map.example.json"
```

精确改写段落：

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/rewrite_paragraphs.py" \
  --input thesis.docx \
  --output thesis-rewritten.docx \
  --replacements "$HOME/.codex/skills/software-thesis-docx/assets/examples/rewrites.example.json"
```

## 7. 高级配置契约

内置示例包括：

- `assets/examples/thesis_manifest.example.json`
- `assets/examples/thesis_workflow_options.example.json`
- `assets/examples/mermaid_requests.example.json`
- `assets/examples/image_map.example.json`
- `assets/examples/rewrites.example.json`

## 8. 当前范围

这个仓库当前只提供了 Codex 兼容的 skill 布局。

下一步计划：

- 增加 OpenCode 的打包与安装说明
- 增加 Claude Code 的接入方式与提示词约定
- 增加跨运行时 smoke test

## 排错建议

- 如果 Codex 没识别到 skill，先确认安装路径是否正确，以及 `SKILL.md` 是否在根目录。
- 如果 builder 结果不对，先检查 manifest 里 `formatting.mode` 是否正确。
- 如果 preset 抽取效果弱，先确认源 `.docx` 里确实包含你希望复用的语义样式。
- 如果图片替换失败，先确认图注文字与 DOCX 中的图注完全一致。
- 如果段落改写失败，先确认目标段落是单 `run` 且全文完全匹配。
