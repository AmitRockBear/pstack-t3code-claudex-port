# T3 profile routing

## Explicit activation

- Use original pstack as the workflow baseline; retain necessary runtime adaptations, agreed user customizations and correctness protections. Discuss further workflow changes with the user.

- Enter pstack only after the user invokes `/poteto-mode`; resume that authorized task across turns and include its activation in every delegated pstack brief.
- On claudep, keep unconditional pstack model/routing includes out of the profile instructions. Keep `disable-model-invocation: true` on every bundled skill except `html-communication`, which stays model-invocable for general HTML deliverables.
- Within the activated workflow, read helper skills directly from the installed skills tree and follow them as workflow references. Interpret pstack's skill-invocation instructions as those file reads; preserve each helper's model, scope and behavior.

Read `~/.pstack/pstack-models.md` for every configured role. These rules override native Agent, model-family substitution, effort-agent and dispatch examples throughout pstack when running inside T3 Code.

## Models and dispatch

- Call `orchestrator_capabilities` before selecting a provider, model or option; use its live catalog, including custom models, availability and constraints.
- For `inherit-parent` or `auto`, omit target provider/model; for `session` effort, omit the effort override.
- Preserve the configured role, effort and panel count; treat `hardest tasks` as `strongest judgment`.
- Resolve model-family entries against `orchestrator_capabilities`, preferring the profile's `claudep` (Claude) and `codexp` (Codex) provider instances; Agent delegation aliases in the active profile instructions take precedence when present. Match the provider to its live instance and preserve the exact model ID. Use an explicit `<providerInstanceId>/<modelId>` sheet entry for a role-specific override.
- Store an ambiguous model choice as `<providerInstanceId>/<modelId> @<effort>` in the sheet and validate both against the live catalog.
- Use T3 `delegate_task` for owners whose workflow requires nested T3 delegation; discovering T3 tools does not give a native subagent an active T3 provider session.
- Use T3 `delegate_task` for Claude and Sol roles with explicit effort, including helpers delegated by owners; pass the configured role's model and effort as target options.
- Prefer native subagent tools for remaining same-provider tasks that can finish through native tools and support the selected model and options. Use T3 `delegate_task` for cross-provider tasks, unsupported native selections and explicitly T3-owned tasks; it runs the selected worker directly.
- Set `target.providerInstanceId`, `target.model` and the catalog's model-specific option ID/value. Codex currently uses `reasoningEffort`, Claude uses `effort`, and Cursor varies by model; discover each instead of assuming a common key.
- For configured Opus 5.5 high, set `target.model: "claude-opus-5-5"` and `target.options: {"effort":"high"}`; for Sol high, set `target.model: "gpt-6.1-sol"` and `target.options: {"reasoningEffort":"high"}`; for Haiku 5.5 high, set `target.providerInstanceId: "claudeAgent_claudep"`, `target.model: "claude-haiku-5-5"` and `target.options: {"effort":"high"}`. Resolve the provider instance from the model sheet and live catalog; agent names and frontmatter are not effort receipts.
- After each explicit-effort T3 dispatch, call `t3_thread_configuration` with `threadId` set to the returned `childThreadId` and compare `modelSelection`'s provider instance, model and effort with the requested target. Report missing or mismatched settings as unverified before dependent work; a matching readback confirms configuration, not provider-effective effort.
- Steer a child only while its turn runs. Check `task_status` first, and start a new `delegate_task` round for a finished child.
- On `thread_not_sendable`, retain the amendment, recheck task status, and use a fresh round once the assignment finishes.
- Use `title: "<model>(<effort>):<actual assignment>"`; task names must describe the worker's assignment.
- Give every child a self-contained goal, acceptance criteria, absolute repository/skill paths, edit scope, constraints, authorization, verification and expected output. Quote the user's applicable approval and limits; carry it forward for the same work. T3 children receive only the supplied prompt, not parent conversation history or MCP sessions.
- Keep accepted decisions in one `accepted-decisions.md` in the task outputs folder; link it in every brief and reject a brief that contradicts it.
- Before `delegate_task`, reconcile the prompt and referenced brief: scope each exclusion to its inputs and phases, and allow required intermediate outputs into later steps.
- Include the [Babysit review-comment rubric](../../babysit/SKILL.md) in bot-triage, audit, design-review and verifier briefs; assess findings against the current code, accepted scope and agreed behavior.
- For code-writing tasks, point the child at poteto-mode and the applicable workflow/agent instructions; the T3 tool has no `subagent_type` parameter.
- Preserve inherited runtime and interaction modes unless the task requires an authorized override; a read-only prompt defines edit scope independently of permissions.
- Use one worker per configured panel entry and aggregate all terminal reports before judging. Arena and architect have two candidates, interrogate has two reviewers (Sol and Haiku), and the cross-judge pool selects one Opus judge.

## UI design decisions

- When the user explicitly asks to approve UI, layout or copy before implementation, read `~/.pstack/skills/html-communication/SKILL.md`, present distinct static mocks with their file paths, and wait for approval.
- Otherwise, use the original Prototype flow when a UI decision needs evidence: test alternatives, choose from the observations, and continue within the authorized scope. Choose reference directions without adding an approval checkpoint; ask about genuine unresolved preferences that observation cannot settle.
- Prototype interaction checks and screenshots are part of the authorized UI-design experiment. Implemented-change UI verification still requires the user's explicit request.

## Verification

- For implemented-change or PR verification, use the configured Sol verifier at high effort through [verify-change](../../verify-change/SKILL.md); preserve the assigned scenario and independent-review requirements for verification lanes.
- Use [verify-change](../../verify-change/SKILL.md) for verifier brief fields, phase timing, evidence reuse and revision tracking.
- Implemented-change UI verification requires the user's explicit request, even when a generic playbook demands live UI lanes.

## Ownership and completion

- Use `mode: "async"` for long work, retain every returned `taskId`, and continue independent work. Completion notifies and wakes the parent; yield the turn when only children remain instead of polling or starting watchers.
- Use `task_status` when a result is needed during the turn. `mode: "wait"` with a bounded `timeoutMs` is suitable for short checks; `waitTimedOut` ends the wait, not the child. Retain that taskId and inspect its status rather than launching a duplicate.
- Read `task_status` and watch state in the same turn before you call owned work running or watched.
- Record a delivered message as sent until the child acknowledges it; confirm completion from the requested result.
- After each `task_status` read, call `t3_pending_request_list` with the returned `childThreadId` as `threadId`; read each returned `requestId` with `t3_pending_request_read` using the same `threadId`.
- Resolve brief or tool ambiguities within accepted scope as coordinator decisions; relay unresolved user decisions once through the `ask-question` tool, then call `t3_pending_request_respond` with the child's `threadId`, the original `requestId` and `answers` keyed by the original question IDs.
- Report pending questions on terminal tasks as stale and keep those tasks finished.
- Treat `workState: "waiting_for_children"` as unfinished; consume the terminal status and summary when `workState: "result_available"`. Check `hasPendingChildRuns` and later terminal results before cleanup or handoff.
- Use stable `clientRequestId` values for retries and `task_cancel` only for owned tasks that need stopping; confirm cancellation before replacing a writer.
- Start new assignments and returned-owner fix rounds with a fresh `delegate_task` containing the original brief, accepted directives, prior report, branch and exact revision; give each round a distinct `clientRequestId`, stable across transport retries. Reuse an active child only for its existing assignment or costly owned state; check `task_status`, pending questions and nested children before an ownership transfer.
- Start each T3 delegated review round with a fresh `delegate_task` call containing the original brief, prior findings, responses and unresolved objections; retain its returned `taskId` and use a distinct `clientRequestId` per round, stable across retries. Use `t3_thread_send` on an active child only for in-flight updates to its existing assignment.
- Audit owned children with `t3_thread_read` using their returned `childThreadId`, `view: "activity"`, pagination and text offsets; inspect tool actions as well as summaries and report missing activity as an evidence gap.
- Delegated children inherit the calling workspace. Give concurrent writers separate isolated worktrees and explicit file paths; `delegate_task` has no workspace override and a child changing directory does not change T3's thread binding.
- Create ordinary threads with `t3_thread_launch` only when the user requests a separate top-level conversation; choose its workspace in that launch. A delegated childThreadId is backing storage, not a new top-level conversation.

## Program supervision

- When the user explicitly asks for recurring supervision, create one parent-owned hourly `schedule_task` with `schedule: {"type":"interval","everyMs":3600000}`, `bindToCurrentThread: true` and a stable `clientRequestId`; retain its `scheduledTaskId` and report `nextRunAt`.
- Each wake rereads the playbook, objective and accepted amendments, checks owned tasks and pending questions, and measures progress from commits, pushes, checks and decision trails. Deduplicate against in-flight assignments before delegating.
- Pause the owned schedule with `update_scheduled_task` using its `scheduledTaskId` and `enabled: false` on completion, hold or cancellation; use `list_scheduled_tasks` to recover its ID after an interruption before creating another.
- PR events remain parent-owned `watch_pull_request` watches under Babysit; `unwatch_pull_request` releases them at handoff. Program supervision and PR monitoring have separate completion conditions.

## Evidence and profile boundaries

- Follow [Evidence sources](../../why/references/source-playbook.md) for source availability, permitted executing providers, lookup delegation and coverage reporting.

- Keep automatic memory disabled and learned preferences/lessons in the current conversation; durable instruction or skill edits require an explicit user request.
- Keep profile configuration under `~/.pstack`, implementation worktrees under `~/.pstack/worktrees`, and reports/drafts under `~/.pstack/outputs`.
- If T3 tools are missing from a lazy catalog, make one bounded direct call to `orchestrator_capabilities`. For ACP runtimes with `T3_ACP_MCP_NODE`, use the supported `acp-mcp-call` transport below. Report a concrete unavailable provider/tool failure before changing the requested model.
- Outside T3, use native same-provider delegation where supported and report cross-provider roles as unavailable; this profile no longer supplies shell model-launch skills or a Sonnet transport layer.

## ACP transport

Use only when the ACP runtime does not expose T3's injected MCP tools. Retain the same request IDs, taskIds and ownership rules.

```bash
ELECTRON_RUN_AS_NODE=1 "$T3_ACP_MCP_NODE" ${T3_ACP_MCP_ENTRYPOINT:+"$T3_ACP_MCP_ENTRYPOINT"} acp-mcp-call orchestrator_capabilities '{}'
```

Call `delegate_task`, `task_status` or `task_cancel` through the same transport with a structured JSON argument matching the tool schema; this calls T3 orchestration rather than launching a provider CLI.
