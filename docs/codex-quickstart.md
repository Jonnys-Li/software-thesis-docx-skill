# Codex Quick Start

This guide shows the fastest way to install and use `software-thesis-docx` inside Codex.

## 1. Clone Into Your Codex Skills Directory

```bash
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/Jonnys-Li/software-thesis-docx-skill.git \
  "$CODEX_HOME/skills/software-thesis-docx"
```

If you already cloned the repository elsewhere, you can also copy or symlink it into `$CODEX_HOME/skills/software-thesis-docx`.

## 2. Install Python Dependencies

```bash
python3 -m pip install -r "$CODEX_HOME/skills/software-thesis-docx/requirements.txt"
```

## 3. Verify The Skill Layout

The installed directory should contain:

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/`
- `references/`
- `assets/examples/`

The important part is that `SKILL.md` stays at the root of the installed skill.

## 4. Use The Skill In Codex

Ask Codex to use the skill explicitly:

```text
Use $software-thesis-docx to generate a thesis-ready DOCX workflow from my software project repository.
```

Typical prompts:

- `Use $software-thesis-docx to turn my project repo into a structured thesis manifest and generate a DOCX.`
- `Use $software-thesis-docx to replace thesis figures by caption without changing Word layout.`
- `Use $software-thesis-docx to normalize in-text citations and terminology in an existing DOCX.`

## 5. Run The Scripts Directly

Build from a manifest:

```bash
python3 "$CODEX_HOME/skills/software-thesis-docx/scripts/build_docx_from_manifest.py" \
  --manifest "$CODEX_HOME/skills/software-thesis-docx/assets/examples/thesis_manifest.example.json" \
  --output /tmp/example-thesis.docx
```

Replace images by caption:

```bash
python3 "$CODEX_HOME/skills/software-thesis-docx/scripts/replace_images_by_caption.py" \
  --input thesis.docx \
  --output thesis-images-updated.docx \
  --mapping "$CODEX_HOME/skills/software-thesis-docx/assets/examples/image_map.example.json"
```

Rewrite exact-match paragraphs:

```bash
python3 "$CODEX_HOME/skills/software-thesis-docx/scripts/rewrite_paragraphs.py" \
  --input thesis.docx \
  --output thesis-rewritten.docx \
  --replacements "$CODEX_HOME/skills/software-thesis-docx/assets/examples/rewrites.example.json"
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
