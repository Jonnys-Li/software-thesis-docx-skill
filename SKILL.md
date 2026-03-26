---
name: software-thesis-docx
description: Use when the user wants to turn a software project repository into a thesis-ready document workflow, build a formatted graduation-thesis DOCX from structured inputs, or revise an existing DOCX without breaking layout, including caption-based image replacement, citation normalization, and terminology rewrites.
---

# Software Thesis DOCX

## Overview

Use this skill for software-engineering thesis work that starts from a real code repository and ends in a deliverable `docx`. It is designed for two common paths:

- `repo -> thesis sources -> manifest -> formatted docx`
- `existing docx -> targeted post-processing -> visual QA`

This skill is especially useful when the user needs one or more of the following:

- reorganize repository facts into thesis chapters
- build a thesis `docx` from structured content instead of hand-editing Word
- replace thesis figures by caption while preserving layout
- normalize citations or unify terminology without changing Word styles

## Workflow

### 1. Ground The Repository

Before writing anything, inspect the actual repository:

- project structure, modules, APIs, database models, tests
- existing docs, diagrams, screenshots, deployment notes
- thesis-related source material already present in the repo

Do not ask the user where core facts live until you have searched the repo.

If the user already has a `docx`, inspect its structure before editing:

- number of paragraphs, tables, images
- whether target paragraphs are single-run or multi-run
- whether images are inline and captioned in predictable patterns

### 2. Choose The Path

Use this decision split:

- If the user wants a thesis built from repository materials, create or update a manifest and run `scripts/build_docx_from_manifest.py`.
- If the user already has a Word document and wants figure replacement, use `scripts/replace_images_by_caption.py`.
- If the user already has a Word document and wants citation cleanup, wording cleanup, or project-name removal, use `scripts/rewrite_paragraphs.py`.

### 3. Build Structured Inputs First

Prefer structured intermediate files over hardcoded prose in scripts.

- Thesis source organization and naming conventions: read [references/source-conventions.md](references/source-conventions.md)
- End-to-end methodology: read [references/workflow.md](references/workflow.md)
- Migration rules for adapting one-off thesis scripts into reusable tooling: read [references/migration-notes.md](references/migration-notes.md)

The public contracts for this skill live in:

- [assets/examples/thesis_manifest.example.json](assets/examples/thesis_manifest.example.json)
- [assets/examples/image_map.example.json](assets/examples/image_map.example.json)
- [assets/examples/rewrites.example.json](assets/examples/rewrites.example.json)

### 4. Run The Right Script

Build a new thesis `docx`:

```bash
python3 scripts/build_docx_from_manifest.py \
  --manifest assets/examples/thesis_manifest.example.json \
  --output /tmp/thesis.docx
```

Replace images in an existing `docx` by caption:

```bash
python3 scripts/replace_images_by_caption.py \
  --input thesis.docx \
  --output thesis-images-updated.docx \
  --mapping assets/examples/image_map.example.json
```

Rewrite exact-match paragraphs in an existing `docx`:

```bash
python3 scripts/rewrite_paragraphs.py \
  --input thesis.docx \
  --output thesis-rewritten.docx \
  --replacements assets/examples/rewrites.example.json
```

### 5. Quality Gates

Always enforce these rules:

- Do not hardcode machine-specific paths.
- Do not expose the user’s real thesis assets in the reusable skill unless explicitly requested.
- When editing an existing `docx`, preserve paragraph styles, alignment, spacing, and image layout unless the task explicitly requires changing them.
- Prefer caption-based figure replacement over “nth image in the document” logic.
- Prefer exact full-paragraph rewrites over fragile substring edits when preserving Word formatting matters.

### 6. Visual QA

After meaningful changes, validate the output:

- If LibreOffice works, render `docx -> pdf` and inspect pages.
- Otherwise use QuickLook or another local preview path.
- At minimum, confirm the output can be reopened by `python-docx`.

For detailed QA expectations and a fuller end-to-end checklist, read [references/workflow.md](references/workflow.md).

## When To Be Careful

Stop and inspect before applying automated rewrites if any of the following is true:

- the target paragraph uses multiple runs for mixed formatting
- the document uses tracked changes or comments that must be preserved
- figure captions are missing or inconsistent
- the user asks for institution-specific formatting rules not represented in the manifest yet

## Resources

- [references/workflow.md](references/workflow.md): end-to-end repo-to-thesis methodology
- [references/source-conventions.md](references/source-conventions.md): recommended workspace layout and file contracts
- [references/migration-notes.md](references/migration-notes.md): what to keep and what to strip when converting one-off thesis tooling into reusable automation
- `scripts/`: executable tooling for build and post-processing
- `assets/examples/`: minimal public examples for manifests, image mappings, and paragraph rewrites
