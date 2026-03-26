# Codex 快速上手

这份说明用于在 Codex 中最快安装并使用 `software-thesis-docx`。

## 1. 克隆到 Codex Skills 目录

```bash
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/Jonnys-Li/software-thesis-docx-skill.git \
  "$CODEX_HOME/skills/software-thesis-docx"
```

如果你已经在别处克隆过仓库，也可以复制或软链接到 `$CODEX_HOME/skills/software-thesis-docx`。

## 2. 安装 Python 依赖

```bash
python3 -m pip install -r "$CODEX_HOME/skills/software-thesis-docx/requirements.txt"
```

## 3. 检查技能目录结构

安装后的目录至少应包含：

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/`
- `references/`
- `assets/examples/`

关键点是 `SKILL.md` 必须位于安装后的技能根目录。

## 4. 在 Codex 中显式调用

可以直接这样发起：

```text
Use $software-thesis-docx to generate a thesis-ready DOCX workflow from my software project repository.
```

常见提示词示例：

- `Use $software-thesis-docx to turn my project repo into a structured thesis manifest and generate a DOCX.`
- `Use $software-thesis-docx to replace thesis figures by caption without changing Word layout.`
- `Use $software-thesis-docx to normalize in-text citations and terminology in an existing DOCX.`

## 5. 直接运行脚本

根据 manifest 构建论文：

```bash
python3 "$CODEX_HOME/skills/software-thesis-docx/scripts/build_docx_from_manifest.py" \
  --manifest "$CODEX_HOME/skills/software-thesis-docx/assets/examples/thesis_manifest.example.json" \
  --output /tmp/example-thesis.docx
```

按图注替换图片：

```bash
python3 "$CODEX_HOME/skills/software-thesis-docx/scripts/replace_images_by_caption.py" \
  --input thesis.docx \
  --output thesis-images-updated.docx \
  --mapping "$CODEX_HOME/skills/software-thesis-docx/assets/examples/image_map.example.json"
```

精确改写段落：

```bash
python3 "$CODEX_HOME/skills/software-thesis-docx/scripts/rewrite_paragraphs.py" \
  --input thesis.docx \
  --output thesis-rewritten.docx \
  --replacements "$CODEX_HOME/skills/software-thesis-docx/assets/examples/rewrites.example.json"
```

## 6. 当前适配范围

这个仓库当前只提供了 Codex 兼容的 skill 布局。

下一步计划：

- 增加 OpenCode 的打包与安装说明
- 增加 Claude Code 的接入方式与提示词约定
- 增加跨运行时 smoke test

## 排错建议

- 如果 Codex 没识别到技能，先确认安装路径是否正确，以及 `SKILL.md` 是否在根目录。
- 如果图片替换失败，先确认图注文字与 DOCX 中的图注完全一致。
- 如果段落改写失败，先确认目标段落是单 `run` 且全文完全匹配。
