# AIGC Risk

## Purpose

Use AIGC risk checks when the user wants a local, heuristic pass over thesis prose before submission or before manual polishing.

This is a local risk score, not a claim that it matches any institution's external detector.

The skill now supports two rewrite profiles:

- `academic_safe`: default; keep academic tone and only absorb low-risk anti-template rewrites
- `explicit_low_aigc`: only for users who explicitly ask to lower AIGC; allows stronger sentence expansion and naturalization

## Checker Script

```bash
python3 scripts/check_aigc_risk.py \
  --input thesis.docx \
  --output report.json
```

The report includes:

- paragraph index
- excerpt
- risk score
- triggered signals
- rewrite recipe
- typography flags
- whether rewrite is recommended

## Rewrite Script

```bash
python3 scripts/rewrite_low_aigc_docx.py \
  --input thesis.docx \
  --report report.json \
  --output thesis-low-aigc.docx \
  --pending-output aigc-pending-review.json \
  --profile academic_safe \
  --normalize-typography
```

## Current Signals

- frequent transition cliches
- low-information summary phrases
- compressed academic enumerations
- colon/semicolon-driven template paragraphs
- dense operation chains
- term stacks without enough explanation
- claims without concrete evidence markers
- typography issues in Chinese thesis paragraphs

## Recommended Workflow

1. Run the checker and inspect high-risk paragraphs first.
2. Only rewrite paragraphs the user has authorized.
3. Use `academic_safe` unless the user explicitly asked to lower AIGC.
4. Prefer concrete, evidence-linked rewrites over cosmetic synonym swaps.
5. Normalize punctuation and spacing while rewriting.
6. If a paragraph is a single run, `rewrite_low_aigc_docx.py` can auto-apply the rewrite.
7. If a paragraph has mixed formatting or multiple runs, stop and review the pending JSON output before manual confirmation.

See [low-aigc-playbook.md](low-aigc-playbook.md) for the sample-driven methodology.

## Safe Defaults

- `enabled`: false
- `check_only`: true
- `auto_reduce`: false
- `target_scope`: generated content or user-selected paragraphs only
- `rewrite_profile`: `academic_safe`
- `normalize_typography`: true

## What Not To Do

- Do not silently rewrite an entire thesis.
- Do not imply guaranteed compliance with any third-party AIGC score.
- Do not treat the risk report as a substitute for human academic review.
- Do not reduce citation density, weaken facts, or replace technical terms inaccurately just to chase a lower score.
