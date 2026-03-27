# Low AIGC Playbook

## Purpose

This document captures a sample-driven methodology for lowering AIGC-style writing risk in thesis prose without blindly copying the source samples.

The playbook is based on a real before/after thesis pair:

- the high-risk version was structurally sound but relied heavily on compressed academic templates
- the low-risk version reduced those templates through sentence expansion, explicit reasoning links, and typography cleanup

## Four Reusable Rule Groups

### 1. Expand Compressed Sentences

Typical high-risk form:

- dense technical lists
- one sentence carrying background, mechanism, and conclusion at the same time
- repeated use of `通过 / 实现 / 提升 / 优化 / 构建`

Preferred rewrite:

- split one dense sentence into two or three shorter sentences
- keep facts and citations intact
- expose the relationship between mechanism and outcome more explicitly

### 2. De-Template Enumerations

Typical high-risk form:

- `一是 / 二是 / 三是`
- `第一，...；第二，...；第三，...`
- colon plus semicolon lists that read like an outline pasted into prose

Preferred rewrite:

- convert the outline-like block into full sentences
- keep the same number of items
- vary clause shapes so the paragraph reads like prose rather than a template

### 3. Make Reasoning Links Explicit

Typical high-risk form:

- facts are correct but the sentence jumps directly from premise to conclusion
- technical terms are stacked without enough connective explanation

Preferred rewrite:

- add neutral framing such as `在系统实现层面` or `在该场景下`
- clarify what the listed mechanism does before stating the result
- add explanation, not new facts

### 4. Normalize Punctuation And Spacing

Typical high-risk form:

- mixed halfwidth and fullwidth punctuation in Chinese paragraphs
- spaces between Chinese and English tokens in inconsistent positions
- citations detached from the preceding clause

Preferred rewrite:

- keep Chinese paragraphs on consistent Chinese punctuation
- normalize Chinese-English spacing consistently
- keep citations attached to the sentence they support

## Dual Rewrite Profiles

### `academic_safe`

Use by default.

- preserve academic tone
- absorb only low-risk anti-template moves
- avoid noticeable colloquial drift

### `explicit_low_aigc`

Use only when the user explicitly says to lower AIGC.

- allow stronger sentence expansion
- allow more naturalized clause flow
- still preserve facts, citations, figure numbers, and technical terminology

## Patterns To Exclude

Do not generalize these sample artifacts into the public skill:

- lowering citation density just to reduce detector pressure
- replacing accurate terms with less precise wording
- overusing colloquial fillers such as `这个 / 这样 / 当中`
- weakening claims by making them vague
- changing English abstract prose into casual English
