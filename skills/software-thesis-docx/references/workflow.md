# Workflow

## Purpose

This workflow is for turning a real software project repository into a thesis-ready document pipeline, then refining the resulting `docx` without manually redoing formatting in Word.

## End-To-End Flow

### 1. Repository Grounding

Start from facts in the repository, not from guesses.

Inspect:

- backend entrypoints, services, data models, and APIs
- frontend pages, interaction flows, and state management
- test files and current pass/fail scope
- deployment notes, security notes, and architectural docs
- diagrams, screenshots, and any thesis drafts already in the repo

Typical output of this step:

- chapter candidates for introduction, technical background, requirements, design, implementation, testing, and conclusion
- a shortlist of code files and diagrams that support each chapter

### 2. Source Material Consolidation

Convert repository facts into thesis source inputs:

- chapter titles and section structure
- paragraph drafts or bullet notes
- figure list and captions
- screenshot inventory
- reference list

Prefer structured files over one-off script constants.

### 3. Manifest Authoring

Create a manifest that describes:

- thesis metadata
- abstracts and keywords
- ordered content blocks
- figure locations and captions
- tables
- references

The build script should consume this manifest directly.

### 4. DOCX Build

Use `build_docx_from_manifest.py` to render:

- cover
- Chinese and English abstracts
- table of contents
- chapters, sections, and subsections
- tables and figures
- references

The builder owns formatting. The manifest owns content.

### 5. Post-Processing Existing DOCX

Use post-processing only when it is safer than rebuilding:

- `replace_images_by_caption.py` for figure swaps
- `rewrite_paragraphs.py` for exact-match paragraph rewrites such as citation normalization or terminology cleanup

Do not use paragraph rewrite automation for arbitrary fuzzy edits. It is meant for deterministic, layout-preserving changes.

### 6. Visual QA

Validate after each meaningful document mutation:

- output opens cleanly in Word-compatible viewers
- paragraph count, table count, and image count are reasonable
- figure captions still align with their images
- rewritten paragraphs still match original styles
- no unexpected page explosions, clipping, or overlap

## Common High-Value Tasks

### Build From Repo

Use when the user says things like:

- “根据我的项目仓库整理毕业论文并输出 Word”
- “帮我把现有章节草稿排成论文格式”
- “从项目代码和图表生成一版 thesis docx”

### Replace Figures

Use when the user says things like:

- “把论文里现有图片替换成新图，不改 Word 格式”
- “按图注匹配替换图 4-1 到图 5-4”

### Normalize Citations Or Wording

Use when the user says things like:

- “规范文内引用，不动参考文献列表格式”
- “把项目名统一替换成该系统，不改段落样式”

## Acceptance Checklist

- Source files and scripts use relative or parameterized paths only.
- The skill does not depend on private thesis assets.
- Build and post-process scripts expose stable CLI arguments.
- Example contracts are present and readable.
- The output `docx` can be re-opened by `python-docx`.
