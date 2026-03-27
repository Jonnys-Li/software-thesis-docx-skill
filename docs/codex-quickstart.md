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
- `scripts/`
- `references/`
- `assets/examples/`
- `requirements.txt`

The important part is that `SKILL.md` stays at the root of the installed skill.

## 3. Use The Skill In Codex

Ask Codex to use the skill explicitly:

```text
Use $software-thesis-docx to generate a thesis-ready DOCX workflow from my software project repository.
```

Typical prompts:

- `Use $software-thesis-docx to turn my project repo into a structured thesis manifest and generate a DOCX.`
- `Use $software-thesis-docx to replace thesis figures by caption without changing Word layout.`
- `Use $software-thesis-docx to normalize in-text citations and terminology in an existing DOCX.`

## 4. Optional Dependency Step

If your Python environment does not already include the required libraries:

```bash
python3 -m pip install -r "$HOME/.codex/skills/software-thesis-docx/requirements.txt"
```

If you use a custom `CODEX_HOME`, replace the path accordingly.

## 5. Run The Scripts Directly

Build from a manifest:

```bash
python3 "$HOME/.codex/skills/software-thesis-docx/scripts/build_docx_from_manifest.py" \
  --manifest "$HOME/.codex/skills/software-thesis-docx/assets/examples/thesis_manifest.example.json" \
  --output /tmp/example-thesis.docx
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

## 6. Current Scope

This repository currently ships the Codex-compatible skill layout only.

Planned next steps:

- OpenCode packaging and install instructions
- Claude Code packaging and prompt guidance
- Shared smoke tests across runtimes

## Troubleshooting

- If Codex does not discover the skill, confirm the install path and make sure `SKILL.md` is at the root.
- If image replacement fails, check that each target caption exactly matches the caption text in the DOCX.
- If paragraph rewriting fails, confirm the paragraph is a single-run exact match.
