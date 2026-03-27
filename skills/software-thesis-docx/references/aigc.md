# AIGC Risk

## Purpose

Use AIGC risk checks when the user wants a local, heuristic pass over thesis prose before submission or before manual polishing.

This is a local risk score, not a claim that it matches any institution's external detector.

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
- whether rewrite is recommended

## Current Signals

- frequent transition cliches
- low-information summary phrases
- overly uniform sentence-length patterns
- repeated tri-grams
- claims without concrete evidence markers
- low lexical diversity

## Recommended Workflow

1. Run the checker and inspect high-risk paragraphs first.
2. Only rewrite paragraphs the user has authorized.
3. Prefer concrete, evidence-linked rewrites over cosmetic synonym swaps.
4. If a paragraph is a single run, reuse `rewrite_paragraphs.py` for deterministic updates.
5. If a paragraph has mixed formatting or multiple runs, stop and ask for manual confirmation before rewriting.

## Safe Defaults

- `enabled`: false
- `check_only`: true
- `auto_reduce`: false
- `target_scope`: generated content or user-selected paragraphs only

## What Not To Do

- Do not silently rewrite an entire thesis.
- Do not imply guaranteed compliance with any third-party AIGC score.
- Do not treat the risk report as a substitute for human academic review.
