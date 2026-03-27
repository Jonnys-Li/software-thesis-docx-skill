# Intake Options

## When To Collect Options

Use the full option intake for complex tasks:

- `repo -> thesis`
- whole-chapter drafting or rewriting
- full-document academic tone cleanup
- citation and argument restructuring across multiple sections

For small or surgical tasks, skip the full intake unless the user explicitly asks for advanced features.

## Collection Order

Ask in this order:

1. formatting mode
2. Mermaid generation
3. subagent rigorous-writing mode
4. AIGC checking or AIGC checking plus auto-reduction

If the runtime supports structured prompts such as `request_user_input`, use them.
If not, fall back to the same questions in plain conversation.

## Defaults

- `formatting.mode = default_preset`
- `mermaid.enabled = false`
- `subagents.enabled = false`
- `aigc.enabled = false`

## Unified Options Contract

The top-level options object should contain:

- `formatting`
- `mermaid`
- `subagents`
- `aigc`

See [assets/examples/thesis_workflow_options.example.json](../assets/examples/thesis_workflow_options.example.json).

## Notes On Subagents

- Default is off.
- Only enable when the user explicitly asks for stricter academic drafting and the runtime supports delegation.
- Keep the default split narrow:
  - `explorer` for repository evidence and source grounding
  - `default` for chapter drafting and argument organization
  - `default` for tone consistency and citation-opportunity review

If delegation is not available, fall back to single-agent execution and say so briefly.
