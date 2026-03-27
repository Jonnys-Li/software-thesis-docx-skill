# Mermaid

## Purpose

Use Mermaid generation when the user wants architecture, flow, sequence, entity, state, schedule, or concept diagrams derived from repository facts.

This skill treats Mermaid as a generation contract, not as a mandatory local rendering pipeline.

## Supported Diagram Types

- `flowchart`
- `sequenceDiagram`
- `erDiagram`
- `stateDiagram-v2`
- `classDiagram`
- `gantt`
- `mindmap`

## Request Contract

Store Mermaid requests in a JSON object with:

- `enabled`
- `output_mode`
- `requests`

Each request should include:

- `name`
- `diagram_type`
- `topic`
- `source_scope`
- `constraints`

See [assets/examples/mermaid_requests.example.json](../assets/examples/mermaid_requests.example.json).

## Output Modes

- `inline`: return Mermaid code in the response only
- `files`: write `.mmd` files under `output/diagrams/<slug>.mmd` when the user explicitly wants files

## Generation Rules

- Ground node names and relationships in repository facts or user-supplied chapter material.
- Prefer thesis-ready labels over product-marketing labels.
- Keep diagrams intentionally scoped. Do not dump every module into one chart.
- If the user asks for multiple diagrams, keep each one focused on a single question.

## Typical Uses

- `flowchart`: system overview, request pipeline, recommendation pipeline
- `sequenceDiagram`: multi-agent turn flow, retrieval and response flow
- `erDiagram`: database or knowledge schema summary
- `stateDiagram-v2`: task state transitions or conversation states
- `classDiagram`: domain model or service boundary summary
- `gantt`: thesis schedule or project implementation plan
- `mindmap`: background, literature review, or requirements decomposition
