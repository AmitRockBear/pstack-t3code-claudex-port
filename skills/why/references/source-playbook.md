# Evidence sources for the claudep profile

Use this source table for why, recall, reflect, and any workflow that fetches external evidence. The configured sources are GitHub, Linear, Slack, Axiom, and Langfuse; repository files and local artifacts remain available as evidence.

| Source | Access | Execution | Playbook |
|---|---|---|---|
| GitHub and git history | `git`, `gh` | Claude or Codex | [Code archaeology](sources/code-archaeology.md) |
| Linear tickets | Linear CLI, executable `linear` | Claude or Codex | [Linear](sources/linear.md) |
| Slack conversations | Slack plugin tools | Codex through T3 delegation | [Slack](sources/slack.md) |
| Application logs and traces | axiom-cli, executable `axiom` | Codex through T3 delegation | [Axiom](sources/axiom.md) |
| AI agent and LLM call traces | langfuse-cli, executable `langfuse` | Codex through T3 delegation | [Langfuse](sources/langfuse.md) |

- Read [profile routing](../../poteto-mode/references/claudep-routing.md) and the model sheet before dispatch; keep the configured role model and effort.
- Check Axiom and Langfuse CLI capabilities inside the executing Codex session; GitHub and Linear capability checks can run on either provider. Use `command -v` and inspect installed help for supported read commands; resolve executables on the worker's own PATH and report concrete missing-command failures.
- Treat an installed CLI or plugin as a capability, not proof of authentication; report authentication or access failures separately from searches with no matches.
- Discover Slack search and thread-read tools inside the executing Codex session; the requesting role delegates a self-contained lookup and waits for its cited report. Plugin registration alone does not prove those tools are callable.
- Route all Slack, Axiom, and Langfuse access, including capability checks, through Codex. A Claude or Cursor role delegates a read-only lookup to the configured why investigators role at high effort and consumes its cited result before completing the step; preserve the requesting role's model. A worker already running in Codex uses its own plugin/CLIs directly.
- Keep investigations read-only: search, list, view, fetch, and query; return findings and citations without modifying external state.
- Bound searches by the target repository, workspace, service, project, time window, or linked IDs; query a production service only when the task authorizes it.
- Use existing CLI authentication or a task-authorized env-file path; keep credentials out of prompts, commands, reports, and displayed help defaults.
- Record a coverage row for each configured source as searched, unavailable with its cause, or irrelevant with its reason; preserve unsuccessful searches as findings.

Cross-cutting: add [Incident and postmortem context](sources/incident-postmortem.md) when the target looks defensive.
