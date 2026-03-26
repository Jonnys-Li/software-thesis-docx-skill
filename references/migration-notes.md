# Migration Notes

## Goal

These notes explain how to convert one-off thesis tooling into reusable open-source automation.

## What To Keep From A Private Thesis Pipeline

Reusable parts:

- paragraph, heading, caption, table, and page-number formatting helpers
- image-fit logic based on page width or existing image box
- caption-based figure replacement
- exact paragraph rewrite logic for single-run paragraphs
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

The open-source build script should keep the formatting helpers but move all real thesis text out to a manifest.

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

Expose only three user-facing scripts:

- build from manifest
- replace images by caption
- rewrite exact paragraphs

Everything else should stay in documentation or example configs unless repeated usage proves another script is necessary.
