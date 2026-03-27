# software-thesis-docx

Build and refine thesis-ready `DOCX` workflows from real software project repositories.

Chinese documentation: [README.zh-CN.md](README.zh-CN.md)

## Install In 30 Seconds

### Codex native

```text
$skill-installer install https://github.com/Jonnys-Li/software-thesis-docx-skill/tree/main/skills/software-thesis-docx
```

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/Jonnys-Li/software-thesis-docx-skill/main/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/Jonnys-Li/software-thesis-docx-skill/main/install.ps1 | iex
```

After installing, restart Codex to pick up new skills.

## Try It

```text
Use $software-thesis-docx to turn my project repo into a structured thesis manifest and generate a DOCX with the built-in academic preset.
Use $software-thesis-docx to read my school Word template, extract a custom style preset, and build the thesis in that format.
Use $software-thesis-docx to generate Mermaid architecture and sequence diagrams for my thesis from the repository structure.
Use $software-thesis-docx to run an AIGC risk check on my thesis DOCX and only rewrite the flagged single-run paragraphs if I approve it.
Use $software-thesis-docx to lower AIGC for my thesis and switch to explicit_low_aigc mode only for the paragraphs I authorize.
```

## What It Adds

- A built-in academic formatting preset derived from a real thesis layout sample, without shipping the original private document
- Runtime extraction of custom style presets from uploaded or provided `.docx` templates
- Manifest-driven DOCX build with optional `formatting` config
- Mermaid request contracts for architecture, sequence, ER, state, gantt, class, and mind-map diagrams
- Optional rigorous-writing subagent mode for complex thesis tasks, default off
- Sample-driven AIGC risk checking and dual-profile paragraph-level reduction workflow, default off and defaulting to `academic_safe`

## Compatibility

- Codex: supported now
- OpenCode: planned
- Claude Code: planned

## What This Repository Ships

- Root-level distribution files: `README`, release notes, and one-click installers
- The actual reusable skill at `skills/software-thesis-docx/`
- Six user-facing scripts and one shared helper:
  - `build_docx_from_manifest.py`
  - `extract_docx_style_preset.py`
  - `replace_images_by_caption.py`
  - `rewrite_paragraphs.py`
  - `check_aigc_risk.py`
  - `rewrite_low_aigc_docx.py`
  - `aigc_utils.py`
- Public examples for manifests, workflow options, Mermaid requests, image maps, and paragraph rewrites
- Reference docs for formatting presets, Mermaid planning, option intake, AIGC review, a low-AIGC playbook, and repo-to-thesis workflow

## Repository Layout

```text
.
├── install.py
├── install.sh
├── install.ps1
├── docs/
└── skills/software-thesis-docx/
```

## Core Skill Path

The official Codex install target is:

```text
https://github.com/Jonnys-Li/software-thesis-docx-skill/tree/main/skills/software-thesis-docx
```

Inside that folder you will find:

- `SKILL.md`
- `agents/openai.yaml`
- `assets/examples/`
- `assets/presets/`
- `references/`
- `scripts/`
- `requirements.txt`

## Documentation

- [Codex quick start](docs/codex-quickstart.md)
- [v0.4.0 release notes](docs/releases/v0.4.0.md)
- [v0.3.0 release notes](docs/releases/v0.3.0.md)
- [v0.2.0 release notes](docs/releases/v0.2.0.md)
- [v0.1.0 release notes](docs/releases/v0.1.0.md)

## Design Principles

- Ground the thesis in repository facts before drafting prose
- Keep content in structured inputs instead of hardcoding thesis text in Python
- Separate formatting from content through built-in or extracted style presets
- Prefer caption-based figure replacement over position-based image replacement
- Prefer exact paragraph rewrites when Word layout fidelity matters
- Keep Mermaid generation and AIGC review opt-in, not forced defaults
- Keep `explicit_low_aigc` behind an explicit user request; otherwise stay in `academic_safe`

## Limits

- Mermaid support currently generates code and file outputs, not rendered images or automatic DOCX insertion
- The paragraph rewrite tool only handles exact full-paragraph matches
- Mixed-format, multi-run paragraphs should be inspected before automated edits
- The AIGC checker is a sample-driven local heuristic pass, not a guarantee of any third-party score
- Institution-specific formatting rules may still require manifest or preset extensions

## Roadmap

- Add OpenCode-compatible packaging and installation paths
- Add Claude Code-compatible prompt and repository layout guidance
- Add shared smoke tests across Codex, OpenCode, and Claude Code
- Expand style extraction for more complex school templates with richer front matter

## License

[MIT](LICENSE)
