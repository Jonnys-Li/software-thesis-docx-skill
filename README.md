# software-thesis-docx

An open-source Codex skill and script bundle for turning a software project repository into a thesis-ready DOCX workflow.

This repository focuses on two practical paths:

- `repository -> structured thesis sources -> manifest -> formatted docx`
- `existing docx -> safe post-processing -> visual QA`

Chinese documentation: [README.zh-CN.md](README.zh-CN.md)

## What It Includes

- `SKILL.md`: the reusable Codex skill entrypoint
- `agents/openai.yaml`: skill metadata
- `scripts/build_docx_from_manifest.py`: build a thesis DOCX from a manifest
- `scripts/replace_images_by_caption.py`: replace inline figures by matching captions
- `scripts/rewrite_paragraphs.py`: rewrite exact-match paragraphs without breaking Word formatting
- `references/`: methodology, workspace conventions, and migration guidance
- `assets/examples/`: public example contracts for manifests, image maps, and paragraph rewrites

## Use Cases

- Generate a graduation-thesis DOCX from a real software repository
- Replace thesis figures without manually reformatting Word
- Normalize in-text citations or terminology while preserving paragraph styles
- Extract one-off thesis automation into reusable, parameterized tooling

## Installation

### Python dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Use as a Codex skill

Point Codex skill installation to this repository root, or copy this directory into your local skills directory so that `SKILL.md` remains at the root of the installed skill.

## Scripts

Build a new DOCX from a manifest:

```bash
python3 scripts/build_docx_from_manifest.py \
  --manifest assets/examples/thesis_manifest.example.json \
  --output /tmp/example-thesis.docx
```

Replace images in an existing DOCX by caption:

```bash
python3 scripts/replace_images_by_caption.py \
  --input thesis.docx \
  --output thesis-images-updated.docx \
  --mapping assets/examples/image_map.example.json
```

Rewrite exact-match paragraphs in an existing DOCX:

```bash
python3 scripts/rewrite_paragraphs.py \
  --input thesis.docx \
  --output thesis-rewritten.docx \
  --replacements assets/examples/rewrites.example.json
```

## Public Contracts

`assets/examples/thesis_manifest.example.json`

- metadata for titles, abstracts, and keywords
- ordered content blocks: `chapter`, `section`, `subsection`, `paragraph`, `figure`, `table`, `page_break`, `references`
- figure blocks with `caption`, `path`, `max_width_cm`, `max_height_cm`

`assets/examples/image_map.example.json`

- array items shaped like `{"caption": "...", "image_path": "...", "fit_mode": "original_box|page_width"}`

`assets/examples/rewrites.example.json`

- array items shaped like `{"match_text": "...", "replace_text": "..."}`

## Repository Layout

```text
.
├── SKILL.md
├── agents/
├── assets/examples/
├── references/
└── scripts/
```

## Design Principles

- Ground the thesis in facts from the repository before drafting prose
- Keep content in structured inputs instead of hardcoding thesis text in Python
- Prefer caption-based figure replacement over position-based image replacement
- Prefer exact paragraph rewrites when Word layout fidelity matters
- Validate visually after meaningful DOCX mutations

## Limits

- The paragraph rewrite tool only handles exact full-paragraph matches
- Mixed-format, multi-run paragraphs should be inspected before automated edits
- Institution-specific formatting rules may require manifest or style extensions

## License

[MIT](LICENSE)
