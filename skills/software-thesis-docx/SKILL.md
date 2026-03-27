---
name: software-thesis-docx
description: Use when the user wants to turn a software project repository into a thesis-ready document workflow, build a formatted graduation-thesis DOCX from structured inputs, or revise an existing DOCX without breaking layout, including style preset extraction, caption-based image replacement, citation normalization, Mermaid planning, and optional AIGC risk checks.
---

# Software Thesis DOCX

## Overview

Use this skill for software-engineering thesis work that starts from a real repository and ends in a deliverable `docx`.

Supported paths:

- `repo -> thesis sources -> manifest -> formatted docx`
- `existing docx -> targeted post-processing -> visual QA`

This skill is especially useful when the user needs one or more of the following:

- repository-grounded chapter planning and thesis drafting
- a built-in academic formatting preset or a custom Word-template-derived preset
- Mermaid code for architecture, flow, sequence, ER, state, schedule, or mind-map diagrams
- caption-based figure replacement without breaking Word layout
- citation cleanup or terminology cleanup in an existing `docx`
- optional AIGC risk review or low-AIGC rewrite before final delivery

## 1. Ground The Repository Or The DOCX

Before drafting, inspect the actual repository:

- project structure, modules, APIs, schemas, tests
- existing docs, diagrams, screenshots, deployment notes
- thesis-related source material already present in the repo

If the user already has a `docx`, inspect its structure before editing:

- paragraph, table, and image counts
- whether target paragraphs are single-run or multi-run
- whether images are inline and captioned predictably

Do not ask the user where core facts live until you have searched the repo.

## 2. Decide Whether The Task Is Complex

Use the full option intake for complex tasks only:

- `repo -> thesis`
- whole-chapter drafting or rewriting
- full-document academic tone cleanup
- citation and argument restructuring across multiple sections

For small or surgical tasks, skip the full intake unless the user explicitly asks for advanced features.

## 3. Collect Workflow Options

For complex tasks, collect options in this order:

1. formatting mode
2. Mermaid generation
3. subagent rigorous-writing mode
4. AIGC check or AIGC check plus auto-reduction

Default values:

- `formatting.mode = default_preset`
- `mermaid.enabled = false`
- `subagents.enabled = false`
- `aigc.enabled = false`

For AIGC:

- keep `rewrite_profile = academic_safe` by default
- only switch to `explicit_low_aigc` when the user explicitly asks to lower AIGC

If the runtime supports structured input collection such as `request_user_input`, use it.
If not, ask the same questions in plain conversation.

The user may also provide a JSON options object directly instead of answering interactively.

Read [references/intake-options.md](references/intake-options.md) when you need the exact contract.

## 4. Choose The Formatting Path

Formatting options:

- `default_preset`: use the built-in preset in `assets/presets/default_style_preset.json`
- `custom_style_preset`: load a JSON preset extracted earlier
- `custom_template_docx`: extract a preset from a user-provided `.docx` template at runtime

Use these tools:

- `scripts/extract_docx_style_preset.py` to extract a preset from a `.docx`
- `scripts/build_docx_from_manifest.py` to build the thesis from a manifest

Read [references/style-presets.md](references/style-presets.md) for role coverage, limits, and examples.

## 5. Build Structured Inputs First

Prefer structured intermediate files over hardcoded prose in scripts.

Primary public contracts:

- [assets/examples/thesis_manifest.example.json](assets/examples/thesis_manifest.example.json)
- [assets/examples/image_map.example.json](assets/examples/image_map.example.json)
- [assets/examples/rewrites.example.json](assets/examples/rewrites.example.json)
- [assets/examples/mermaid_requests.example.json](assets/examples/mermaid_requests.example.json)
- [assets/examples/thesis_workflow_options.example.json](assets/examples/thesis_workflow_options.example.json)

Supporting references:

- [references/workflow.md](references/workflow.md)
- [references/source-conventions.md](references/source-conventions.md)
- [references/migration-notes.md](references/migration-notes.md)
- [references/low-aigc-playbook.md](references/low-aigc-playbook.md)

## 6. Run The Right Script

Build a new thesis `docx`:

```bash
python3 scripts/build_docx_from_manifest.py \
  --manifest assets/examples/thesis_manifest.example.json \
  --output /tmp/thesis.docx
```

Build with an extracted preset:

```bash
python3 scripts/build_docx_from_manifest.py \
  --manifest thesis_manifest.json \
  --style-preset style-preset.json \
  --output thesis.docx
```

Extract a preset from a Word template:

```bash
python3 scripts/extract_docx_style_preset.py \
  --input template.docx \
  --output style-preset.json
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

Run a local AIGC risk scan:

```bash
python3 scripts/check_aigc_risk.py \
  --input thesis.docx \
  --output /tmp/aigc-risk-report.json
```

Rewrite authorized paragraphs for lower AIGC risk:

```bash
python3 scripts/rewrite_low_aigc_docx.py \
  --input thesis.docx \
  --report /tmp/aigc-risk-report.json \
  --output thesis-low-aigc.docx \
  --pending-output /tmp/aigc-pending-review.json \
  --profile academic_safe \
  --normalize-typography
```

## 7. Mermaid Rules

Mermaid generation is an orchestration capability, not a required rendering pipeline.

Supported diagram types:

- `flowchart`
- `sequenceDiagram`
- `erDiagram`
- `stateDiagram-v2`
- `classDiagram`
- `gantt`
- `mindmap`

Default output is inline code in the response.
Only write `.mmd` files under `output/diagrams/` when the user explicitly asks for file output.

Read [references/mermaid.md](references/mermaid.md) before generating multiple diagrams or file outputs.

## 8. Subagent Rules

Subagent rigorous-writing mode is default off.

Do not delegate unless all of the following are true:

- the task is complex
- the user explicitly enabled subagents
- the runtime supports delegation

Default split when enabled:

- `explorer` for repository evidence and source grounding
- `default` for chapter drafting and argument organization
- `default` for academic tone consistency and citation-opportunity review

If delegation is unavailable, fall back to single-agent execution and say so briefly.

## 9. AIGC Rules

Use AIGC checks as a local heuristic review pass, not as a guarantee of any external detector score.

Safe behavior:

- scan first
- rewrite only authorized paragraphs
- keep `academic_safe` as the default rewrite profile
- use `explicit_low_aigc` only when the user explicitly asks to lower AIGC
- prefer more concrete, evidence-linked language
- use `rewrite_low_aigc_docx.py` for authorized single-run paragraphs
- stop for manual confirmation on multi-run or mixed-format paragraphs and inspect the pending JSON output

Read [references/aigc.md](references/aigc.md) and [references/low-aigc-playbook.md](references/low-aigc-playbook.md) when the user asks for detection or low-AIGC rewriting.

## 10. Quality Gates

Always enforce these rules:

- Do not hardcode machine-specific paths.
- Do not expose the user’s real thesis assets in the reusable skill unless explicitly requested.
- When editing an existing `docx`, preserve paragraph styles, alignment, spacing, and image layout unless the task explicitly requires changing them.
- Prefer caption-based figure replacement over “nth image in the document” logic.
- Prefer exact full-paragraph rewrites over fragile substring edits when Word formatting fidelity matters.

## 11. Visual QA

After meaningful changes, validate the output:

- If LibreOffice works, render `docx -> pdf` and inspect pages.
- Otherwise use QuickLook or another local preview path.
- At minimum, confirm the output can be reopened by `python-docx`.

Read [references/workflow.md](references/workflow.md) for the fuller QA checklist.

## 12. When To Be Careful

Stop and inspect before applying automated rewrites if any of the following is true:

- the target paragraph uses multiple runs for mixed formatting
- the document uses tracked changes or comments that must be preserved
- figure captions are missing or inconsistent
- the user asks for institution-specific formatting rules not represented in the manifest yet
- the user asks for aggressive whole-document AIGC rewriting
