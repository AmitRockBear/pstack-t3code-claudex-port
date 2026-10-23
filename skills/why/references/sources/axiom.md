# Axiom application logs and traces

Use axiom-cli's executable `axiom` for application runtime evidence. Follow [Evidence sources](../source-playbook.md) for source access, executing-provider restrictions and lookup delegation.

1. Check `command -v axiom` and inspect `axiom query --help` with credential defaults suppressed before displaying help.
2. Use the task's dataset, service, environment, identifiers, and time window. When dataset discovery is needed and authorized, use `axiom dataset list -f json`.
3. Build a bounded APL query for the relevant error, request, trace, or session identifiers; inspect the available fields before assuming their names.
4. Query with `axiom query <apl-query> -f json --start-time <start> --end-time <end> --no-spinner`.
5. Aggregate counts and timing before fetching detailed events; follow a concrete trace or request ID when the aggregate suggests it is relevant.
6. Compare timestamps with commits or releases and distinguish correlation from evidence of intent.

Return dataset, environment/service, time window, APL query, trace/request IDs, relevant results, and limitations. An empty successful query is a finding; an authentication failure or inaccessible dataset is a gap. Keep ingestion, annotations, and configuration changes outside an investigation's scope.
