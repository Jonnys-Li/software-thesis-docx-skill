# Source Conventions

## Recommended Workspace Layout

Use a workspace layout like this when preparing inputs for the skill:

```text
workspace/
├── chapters/
│   ├── 01_abstract_cn.md
│   ├── 02_abstract_en.md
│   ├── 03_chapter1.md
│   └── ...
├── figures/
│   ├── 01_system_overview.png
│   ├── 02_backend_architecture.png
│   └── ...
├── screenshots/
│   ├── agent-chat.png
│   ├── diet-week-view.png
│   └── ...
├── manifest/
│   └── thesis_manifest.json
└── output/
    └── thesis.docx
```

## Naming Rules

- Use stable, sortable numeric prefixes for figures and chapters when order matters.
- Keep figure filenames separate from figure captions. Filenames are implementation details; captions are public document text.
- Prefer one manifest per output document.

## Manifest Ownership

Use the manifest to own:

- document metadata
- content ordering
- figure block properties
- table rows
- references

Do not put long-form thesis prose into Python source files when it can live in the manifest or upstream text sources.

## Image Mapping Ownership

Use an image map file to own:

- target caption
- replacement image path
- fit mode

Do not encode replacement intent inside the script.

## Rewrite File Ownership

Use a rewrite file to own:

- exact paragraph text to match
- exact paragraph text to replace with

Do not rely on fuzzy substring replacement when format preservation matters.

## Path Resolution

Recommended resolution order for relative paths:

1. relative to the config file that mentions the path
2. if provided, relative to `--workspace`
3. absolute path only when the caller explicitly passes one

## What Not To Open Source By Default

Unless the user explicitly wants it public, keep these outside the reusable skill:

- the real thesis `.docx`
- the real chapter prose
- institution-specific templates with unclear redistribution rights
- private screenshots or non-public project documentation
