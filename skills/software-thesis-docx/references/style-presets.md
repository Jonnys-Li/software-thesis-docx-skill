# Style Presets

## Purpose

Use style presets to separate thesis formatting from thesis content.

This skill now supports three formatting modes:

- `default_preset`: use the built-in academic preset shipped in `assets/presets/default_style_preset.json`
- `custom_style_preset`: load a previously extracted JSON preset
- `custom_template_docx`: extract a preset from a user-provided `.docx` template at runtime

## Extraction Script

Extract a reusable preset from a Word template:

```bash
python3 scripts/extract_docx_style_preset.py \
  --input template.docx \
  --output style-preset.json
```

The extractor captures semantic roles instead of copying the original thesis content:

- page margins, header distance, footer distance
- abstract headings and abstract body
- chapter, section, and subsection headings
- body paragraph defaults
- keyword label and keyword text
- figure and table captions when they exist in the template
- reference heading and reference items

## Builder Integration

The builder accepts either a direct CLI override or manifest-driven formatting config.

CLI override:

```bash
python3 scripts/build_docx_from_manifest.py \
  --manifest thesis_manifest.json \
  --style-preset style-preset.json \
  --output thesis.docx
```

Manifest-driven formatting:

```json
{
  "formatting": {
    "mode": "custom_template_docx",
    "template_docx_path": "templates/my-school-template.docx"
  }
}
```

## Recommended Use

- Use `default_preset` when the user does not care about institution-specific formatting.
- Use `custom_template_docx` when the user uploads a school template or a previously typeset thesis sample.
- Use `custom_style_preset` when the same extracted template will be reused across multiple runs.

## Limits

- The preset is semantic, not pixel-perfect cloning of the original template.
- If the source template does not contain figure captions or table captions, those roles fall back to bundled defaults.
- Multi-section templates with radically different front-matter and body styles may still require manual extension.
