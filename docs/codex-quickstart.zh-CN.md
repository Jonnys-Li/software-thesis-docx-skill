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
- `scripts/`
- `references/`
- `assets/examples/`
- `requirements.txt`

关键点是 `SKILL.md` 必须位于安装后的 skill 根目录。

## 3. 在 Codex 中使用

可以直接这样发起：

```text
Use $software-thesis-docx to generate a thesis-ready DOCX workflow from my software project repository.
```

常见提示词示例：

- `Use $software-thesis-docx to turn my project repo into a structured thesis manifest and generate a DOCX.`
- `Use $software-thesis-docx to replace thesis figures by caption without changing Word layout.`
- `Use $software-thesis-docx to normalize in-text citations and terminology in an existing DOCX.`

## 4. 可选依赖安装

如果当前 Python 环境里还没有所需依赖，可以执行：

```bash
python3 -m pip install -r "$HOME/.codex/skills/software-thesis-docx/requirements.txt"
```

如果你设置了自定义 `CODEX_HOME`，把路径替换成对应目录即可。

## 5. 直接运行脚本

根据 manifest 构建论文：

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/build_docx_from_manifest.py" \
  --manifest "$HOME/.codex/skills/software-thesis-docx/assets/examples/thesis_manifest.example.json" \
  --output /tmp/example-thesis.docx
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

## 6. 当前范围

这个仓库当前只提供了 Codex 兼容的 skill 布局。

下一步计划：

- 增加 OpenCode 的打包与安装说明
- 增加 Claude Code 的接入方式与提示词约定
- 增加跨运行时 smoke test

## 排错建议

- 如果 Codex 没识别到 skill，先确认安装路径是否正确，以及 `SKILL.md` 是否在根目录。
- 如果图片替换失败，先确认图注文字与 DOCX 中的图注完全一致。
- 如果段落改写失败，先确认目标段落是单 `run` 且全文完全匹配。
