# Codex Quick Start

This guide shows the fastest way to install and use `software-thesis-docx` inside Codex.

## 1. Install The Skill

### Official Codex installer

```text
$skill-installer install https://github.com/Jonnys-Li/software-thesis-docx-skill/tree/main/skills/software-thesis-docx
```

### One-click installer for macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/Jonnys-Li/software-thesis-docx-skill/main/install.sh | bash
```

### One-click installer for Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/Jonnys-Li/software-thesis-docx-skill/main/install.ps1 | iex
```

Restart Codex after installation.

## 2. Installed Layout

The installed skill directory should contain:

- `SKILL.md`
- `agents/openai.yaml`
- `assets/examples/`
- `assets/presets/`
- `references/`
- `scripts/`
- `requirements.txt`

The important part is that `SKILL.md` stays at the root of the installed skill.

## 3. What The Skill Now Supports

- manifest-driven thesis DOCX generation
- caption-based image replacement
- exact paragraph rewrites for layout-safe terminology or citation cleanup
- built-in academic style preset
- custom style preset extraction from `.docx` templates
- Mermaid planning contracts
- optional subagent rigorous-writing mode
- optional AIGC risk checking and conservative reduction workflow

## 4. Use The Skill In Codex

Ask Codex to use the skill explicitly:

```text
Use $software-thesis-docx to build my thesis DOCX workflow from my software repository and ask me whether to use the default preset, Mermaid generation, subagents, and AIGC checks.
```

Typical prompts:

- `Use $software-thesis-docx to turn my project repo into a structured thesis manifest and generate a DOCX with the built-in preset.`
- `Use $software-thesis-docx to read my Word template, extract a style preset, and build the thesis in that format.`
- `Use $software-thesis-docx to generate Mermaid flowchart and sequenceDiagram code for my thesis based on the repo architecture.`
- `Use $software-thesis-docx to run an AIGC risk review on my thesis DOCX and only rewrite the flagged single-run paragraphs after showing me the report.`

## 5. Optional Dependency Step

If your Python environment does not already include the required libraries:

```bash
python3 -m pip install -r "$HOME/.codex/skills/software-thesis-docx/requirements.txt"
```

If you use a custom `CODEX_HOME`, replace the path accordingly.

## 6. Run The Scripts Directly

Build from the bundled example manifest:

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/build_docx_from_manifest.py" \
  --manifest "$HOME/.codex/skills/software-thesis-docx/assets/examples/thesis_manifest.example.json" \
  --output /tmp/example-thesis.docx
```

Extract a preset from a school template:

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/extract_docx_style_preset.py" \
  --input school-template.docx \
  --output /tmp/style-preset.json
```

Build with that preset:

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/build_docx_from_manifest.py" \
  --manifest thesis_manifest.json \
  --style-preset /tmp/style-preset.json \
  --output /tmp/custom-thesis.docx
```

Run the AIGC risk checker:

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/check_aigc_risk.py" \
  --input thesis.docx \
  --output /tmp/aigc-risk-report.json
```

Replace images by caption:

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/replace_images_by_caption.py" \
  --input thesis.docx \
  --output thesis-images-updated.docx \
  --mapping "$HOME/.codex/skills/software-thesis-docx/assets/examples/image_map.example.json"
```

Rewrite exact-match paragraphs:

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/rewrite_paragraphs.py" \
  --input thesis.docx \
  --output thesis-rewritten.docx \
  --replacements "$HOME/.codex/skills/software-thesis-docx/assets/examples/rewrites.example.json"
```

## 7. Advanced Config Contracts

Bundled examples:

- `assets/examples/thesis_manifest.example.json`
- `assets/examples/thesis_workflow_options.example.json`
- `assets/examples/mermaid_requests.example.json`
- `assets/examples/image_map.example.json`
- `assets/examples/rewrites.example.json`

## 8. Current Scope

This repository currently ships the Codex-compatible skill layout only.

Planned next steps:

- OpenCode packaging and install instructions
- Claude Code packaging and prompt guidance
- Shared smoke tests across runtimes

## Troubleshooting

- If Codex does not discover the skill, confirm the install path and make sure `SKILL.md` is at the root.
- If the builder output looks wrong, check whether the manifest is using the right `formatting.mode`.
- If preset extraction is weak, confirm the source `.docx` actually contains the semantic roles you expect.
- If image replacement fails, check that each target caption exactly matches the caption text in the DOCX.
- If paragraph rewriting fails, confirm the paragraph is a single-run exact match.
