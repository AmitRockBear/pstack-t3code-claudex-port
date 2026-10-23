# Langfuse AI agent and LLM call traces

Use langfuse-cli's executable `langfuse` for agent execution and model-call evidence. Follow [Evidence sources](../source-playbook.md) for source access, executing-provider restrictions and lookup delegation.

1. Check `command -v langfuse` and inspect help for `langfuse api traces list`, `langfuse api traces get`, and `langfuse api observations list`.
2. Use existing authentication or the task-authorized `--env <absolute-env-file>` before `api`; pass the file path without displaying its contents or credential values.
3. Locate traces with a known session ID or a bounded time range, using supported filters from the installed CLI.

```bash
langfuse api traces list --session-id <session-id> --limit 20 --fields core,metrics --json
langfuse api traces get <trace-id> --fields core,metrics --json
langfuse api observations list --trace-id <trace-id> --limit 100 --fields core,basic,time,model,usage --json
```

4. Inspect generation and tool observations for the requested prompt/output behavior, model, duration, usage/cost, status, and recorded scores. Request input/output fields only when needed by the question.
5. Inspect the CLI response envelope before extracting results and follow pagination when needed; record any result cap or unavailable field.
6. Correlate session, trace, observation, version, and release identifiers with code changes; label inferred causes and missing historical data.

Return project/environment, filters and time range, session/trace/observation IDs, relevant evidence and trace links when available, and the commands actually run. Use list/get operations; leave score creation, prompt changes, datasets, and other writes to separately authorized work.
