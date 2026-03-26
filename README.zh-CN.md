# software-thesis-docx

一个面向软件类毕业论文场景的开源 Codex skill 与脚本仓库，用来把“项目代码仓库里的真实事实”整理成可复用的 `docx` 工作流。

这个仓库主要覆盖两条高频路径：

- `代码仓库 -> 论文结构化素材 -> manifest -> 格式化 docx`
- `现有 docx -> 定向后处理 -> 视觉校验`

English documentation: [README.md](README.md)

## 兼容性

- Codex：当前已适配
- OpenCode：计划中
- Claude Code：计划中

Codex 快速上手见：[docs/codex-quickstart.zh-CN.md](docs/codex-quickstart.zh-CN.md)

## 仓库内容

- `SKILL.md`：可直接复用的技能入口
- `agents/openai.yaml`：技能元数据
- `scripts/build_docx_from_manifest.py`：根据 manifest 构建论文 DOCX
- `scripts/replace_images_by_caption.py`：按图注替换内嵌图片
- `scripts/rewrite_paragraphs.py`：精确改写段落且尽量不破坏 Word 格式
- `references/`：方法论、目录约定、迁移说明
- `assets/examples/`：公开的最小示例输入

## 适用场景

- 根据真实软件项目仓库整理毕业论文并导出 Word
- 在不重排版的前提下替换论文图片
- 规范文内引用、统一术语或去项目名标识
- 把一次性的论文脚本整理成可复用、可开源的自动化能力

## 安装

### Python 依赖

```bash
python3 -m pip install -r requirements.txt
```

### 作为 Codex skill 使用

将本仓库根目录作为 skill 安装源，或者把整个目录复制到本地技能目录中，并保持 `SKILL.md` 位于安装后的技能根目录。

如果你想直接照着操作安装和触发，可以看 [docs/codex-quickstart.zh-CN.md](docs/codex-quickstart.zh-CN.md)。

## 脚本用法

根据 manifest 构建新的论文 DOCX：

```bash
python3 scripts/build_docx_from_manifest.py \
  --manifest assets/examples/thesis_manifest.example.json \
  --output /tmp/example-thesis.docx
```

按图注替换已有 DOCX 中的图片：

```bash
python3 scripts/replace_images_by_caption.py \
  --input thesis.docx \
  --output thesis-images-updated.docx \
  --mapping assets/examples/image_map.example.json
```

精确改写已有 DOCX 中的段落：

```bash
python3 scripts/rewrite_paragraphs.py \
  --input thesis.docx \
  --output thesis-rewritten.docx \
  --replacements assets/examples/rewrites.example.json
```

## 公共契约

`assets/examples/thesis_manifest.example.json`

- 包含标题、摘要、关键词等文档元数据
- 内容块支持：`chapter`、`section`、`subsection`、`paragraph`、`figure`、`table`、`page_break`、`references`
- `figure` 块使用 `caption`、`path`、`max_width_cm`、`max_height_cm`

`assets/examples/image_map.example.json`

- 数组项格式：`{"caption": "...", "image_path": "...", "fit_mode": "original_box|page_width"}`

`assets/examples/rewrites.example.json`

- 数组项格式：`{"match_text": "...", "replace_text": "..."}`

## 目录结构

```text
.
├── SKILL.md
├── agents/
├── assets/examples/
├── references/
└── scripts/
```

## 方法原则

- 先以仓库事实为依据，再组织论文章节
- 把内容放进结构化输入，而不是硬编码在 Python 脚本里
- 图片替换优先按图注定位，不按“第几张图”这种脆弱逻辑
- 文本改写优先整段精确匹配，减少对 Word 格式的破坏
- 每次重要变更后都做一次文档可视化校验

## 使用边界

- 段落改写脚本只适合“整段全文精确命中”的场景
- 多 `run`、混合格式、修订痕迹较多的段落需要先人工检查
- 学校格式要求如果更特殊，通常需要扩展 manifest 或样式逻辑

## 下一步

- 补 OpenCode 兼容的 skill 打包方式和安装说明
- 补 Claude Code 兼容的提示词约定与仓库接入方式
- 增加跨运行时 smoke test，保证同一套示例在 Codex、OpenCode、Claude Code 上都可验证

## 许可证

[MIT](LICENSE)
