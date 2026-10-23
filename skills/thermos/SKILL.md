---
name: thermos
description: "Launch both thermo-nuclear review subagents in parallel, then synthesize their findings. Use for thermos, double thermo review, or combined bug/security and code-quality branch audits."
disable-model-invocation: true
---

# Thermos

In T3 Code or the claudep profile, read the [profile routing](../poteto-mode/references/claudep-routing.md) before dispatching roles; it owns models, effort and task lifecycle. Keep the audit read-only and return findings; apply fixes only when authorized.

On Codex, read the [platform mapping](../poteto-mode/references/codex-tools.md), including its per-skill notes, before following this skill.

Run two independent review tasks in parallel, then synthesize their findings.

## Workflow

1. Determine the review scope from the user request, PR, current branch, or relevant changed files.
2. Gather the diff and any file/context excerpts needed for reviewers to evaluate the change without guessing.
3. Launch two independent read-only tasks together, using the configured `judgment and prose` model and effort from `pstack-models.md` through profile routing:
   - Correctness and security: read [`thermo-nuclear-review`](../thermo-nuclear-review/SKILL.md).
   - Maintainability and structure: read [`thermo-nuclear-code-quality-review`](../thermo-nuclear-code-quality-review/SKILL.md).
   Include each skill's absolute path in its task brief. Use T3 `delegate_task` with `mode: "async"` in T3; outside T3, use the runtime's supported subagent tool. Each task follows its assigned rubric and gathers missing code context before reporting.
4. Pass each subagent the same scoped diff/file context and ask it to return prioritized findings with file references and evidence.
5. After both finish, synthesize the results with findings first, deduplicated across reviewers. Weight overlapping findings more heavily, resolve disagreements with your own judgment, and keep summaries brief.

If individual background summaries are already visible to the user, do not restate them wholesale. Surface the unified verdict, the highest-signal findings, and any remaining uncertainty.
