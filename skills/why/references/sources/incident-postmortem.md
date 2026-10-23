# Incident and postmortem context

Use this cross-cutting angle inside each configured source when defensive code suggests an incident-driven origin.

- GitHub/git: trace incident-linked PRs, defensive fixes, reverts, and their review history.
- Linear CLI: read linked incidents, reliability issues, and postmortem action items.
- Codex Slack plugin: read incident threads around the change and preserve original human rulings.
- Axiom CLI: correlate runtime errors and application traces with the incident and release window.
- Langfuse CLI: correlate agent failures, generations, tool calls, latency, or recorded scores with the same session/trace and release window.

Follow linked postmortem text available within these sources or local artifacts. An inaccessible document is a gap. Return incident identifiers, timing, original action-item wording, and the code changes each source supports; keep correlation separate from direct evidence of motivation.
