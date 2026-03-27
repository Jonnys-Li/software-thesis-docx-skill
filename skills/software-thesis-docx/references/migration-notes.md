# Migration Notes

## Goal

These notes explain how to convert one-off thesis tooling into reusable open-source automation.

## What To Keep From A Private Thesis Pipeline

Reusable parts:

- paragraph, heading, caption, table, and page-number formatting helpers
- semantic style extraction from an existing `.docx` template
- image-fit logic based on page width or existing image box
- caption-based figure replacement
- exact paragraph rewrite logic for single-run paragraphs
- local heuristic review passes such as AIGC risk scanning
- structural validation and preview checks

## What To Strip Out

Do not carry these into the open-source skill:

- hardcoded project names
- hardcoded thesis prose inside scripts
- absolute machine-specific paths
- private screenshots and final thesis outputs
- repository-specific assumptions unless surfaced as parameters or examples

## Key Refactor: Builder Script

If a private builder script mixes formatting and final thesis text in one Python file, split it conceptually into two layers:

- formatting engine
- external manifest content
- optional style preset extraction

The open-source build script should keep the formatting helpers but move all real thesis text out to a manifest.

## Key Refactor: Formatting Templates

If a private thesis workflow depends on a hand-adjusted Word file, extract semantic formatting into a reusable preset instead of publishing the original thesis.

The open-source version should:

- keep the preset JSON
- keep the extraction script
- avoid shipping the real thesis template unless redistribution is clearly allowed

## Key Refactor: Image Replacement

The figure replacement algorithm can stay mostly intact if it already:

- locates images by caption
- rewrites image blobs
- optionally resizes by original box or page width

The open-source version must parameterize:

- input/output docx paths
- mapping file path
- image paths
- fit mode per mapping item

## Key Refactor: Paragraph Rewrites

The paragraph rewrite algorithm is reusable when it:

- matches full paragraph text exactly
- edits only single-run paragraphs
- preserves paragraph formatting by rewriting run text in place

The open-source version must not embed any project-specific wording changes.

## Recommended Public Surface

Expose the smallest stable set of user-facing scripts that covers repeated tasks:

- build from manifest
- extract style preset from template docx
- replace images by caption
- rewrite exact paragraphs
- check AIGC risk

Keep higher-level behaviors such as Mermaid authoring and subagent orchestration in the skill instructions and example configs unless repeated usage proves a dedicated script is necessary.
