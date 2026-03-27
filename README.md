# software-thesis-docx

Build and refine software-thesis DOCX workflows from real project repositories.

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
Use $software-thesis-docx to turn my software project repo into a structured thesis manifest and generate a DOCX.
Use $software-thesis-docx to replace thesis figures by caption without changing Word layout.
Use $software-thesis-docx to normalize in-text citations and terminology in an existing DOCX.
```

## Compatibility

- Codex: supported now
- OpenCode: planned
- Claude Code: planned

## What This Repository Ships

- Root-level distribution files: `README`, release notes, and one-click installers
- The actual reusable skill at `skills/software-thesis-docx/`
- Three parameterized DOCX tools for build, figure replacement, and paragraph rewrites
- Public examples and methodology docs for adapting the workflow to another thesis project

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
- `references/`
- `scripts/`
- `requirements.txt`

## Documentation

- [Codex quick start](docs/codex-quickstart.md)
- [v0.2.0 release notes](docs/releases/v0.2.0.md)
- [v0.1.0 release notes](docs/releases/v0.1.0.md)

## Design Principles

- Ground the thesis in repository facts before drafting prose
- Keep content in structured inputs instead of hardcoding thesis text in Python
- Prefer caption-based figure replacement over position-based image replacement
- Prefer exact paragraph rewrites when Word layout fidelity matters
- Validate visually after meaningful DOCX mutations

## Limits

- The paragraph rewrite tool only handles exact full-paragraph matches
- Mixed-format, multi-run paragraphs should be inspected before automated edits
- Institution-specific formatting rules may require manifest or style extensions

## Roadmap

- Add an OpenCode-compatible packaging and installation path
- Add a Claude Code-compatible prompt and repository layout guide
- Add cross-runtime smoke tests across Codex, OpenCode, and Claude Code

## License

[MIT](LICENSE)
