---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

On Codex, read the [platform mapping](../poteto-mode/references/codex-tools.md), including its per-skill notes, before following this skill.

In T3 Code or the claudep profile, read the [profile routing](../poteto-mode/references/claudep-routing.md) before dispatching any role; it overrides native dispatch examples below.

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

In T3, obtain the selected thread ID from the current context or `orchestrator_capabilities.parentThreadId`. Read that thread through `t3_thread_read` with `view: "activity"`, paging with `nextPosition` and recovering truncated items with `itemId` and `nextTextOffset`. Save complete evidence in the task report directory and pass its absolute path to reviewers. Record any unavailable activity as a coverage gap. Do not substitute another profile's native transcript.

Outside T3, the parent finds its own transcript file before fanning out. The system prompt names Claude Code's per-project transcripts directory at `~/.pstack/claude/projects/<encoded-cwd>/`. Use that path. Do not glob across `~/.pstack/claude/projects/`. That crosses workspace boundaries and reads private chats from unrelated projects.

Run the finder at `skills/reflect/scripts/find-transcript.mjs` under the installed plugin with the projects directory and a fragment of the conversation's opening user prompt:

```bash
node <plugin>/skills/reflect/scripts/find-transcript.mjs ~/.pstack/claude/projects/<encoded-cwd> "<opening prompt fragment>"
```

It covers the three layouts (flat `<id>.jsonl`, nested `<id>/<id>.jsonl`, subagent `<parent>/subagents/<child>.jsonl`), newest first, and prints the first path whose opening typed prompt carries the fragment. Do not reimplement the scan by hand: the first line of a transcript is session metadata, not a message, a session that starts with `/clear` or a `!` shell command records that command's wrapper and output as `user` records before the prompt, and files run to several megabytes, so the finder streams each candidate and stops at its first typed `user` record. If complete evidence is unavailable, supply a factual digest in turn order: prompts, corrections, tool calls, results and files touched. State coverage gaps; keep diagnosis, verdict and causes for the reviewers to determine.

## 2. Spawn three reviewers in parallel

One message, three `Agent` calls, `subagent_type: "general-purpose"`, with `model` set as below. Reviewers use [Evidence sources](../why/references/source-playbook.md) for referenced GitHub, Linear, Slack, Axiom, or Langfuse context. Keep CLI tool access and route Slack, Axiom, and Langfuse lookups through Codex. The prompt forbids file writes. The parent applies edits.

Each reviewer and the synthesizer name a role line in `pstack-models.md` and a default in [Models](#models). Set `model` to that line's value, or to the default if the sheet or the line is missing. Leave `model` unset when the value is `auto` or `inherit-parent`. If the `Agent` tool rejects a slug, use the default and say so. If it rejects the default, use the closest valid slug of the same family from its error message.

| Lens | Role line | Prompt template |
|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or factual digest where marked. Add no parent diagnosis, verdict or focus note; include only the operational scope, authorization and routing needed to read the evidence. Reviewers return findings in the `Agent` response body.

## 3. Synthesize

One `Agent` call, `subagent_type: "general-purpose"`, with `model` from the `reflect judgment, divergent, synthesizer` line (default in [Models](#models)). Keep the configured CLI/plugin access. The synthesizer spot-verifies citations using [Evidence sources](../why/references/source-playbook.md), with Slack, Axiom, and Langfuse lookups delegated through Codex. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Return Backlog items in the report; file tickets through the configured Linear CLI only when ticket creation is authorized by the user.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the **plugin-dev:skill-development** skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `plugin-dev:skill-development` and run its description-optimization loop.
- `new skill via plugin-dev:skill-development: <kebab-name>`: hand creation to `plugin-dev:skill-development`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog proposed or, when authorized, filed through Linear CLI: `<issue title>`. One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.

## Models

Role defaults. A matching role line in the `pstack-models.md` override sheet overrides each at runtime; `/setup-pstack` writes it and lists its path per runtime.

- reflect tooling: `opus`
- reflect judgment, divergent, synthesizer: `opus`

## Reasoning effort

A role value in the override sheet may name a reasoning effort after its model, as in `opus @xhigh`. Levels on Claude Code: `low`, `medium`, `high`, `xhigh`, `max`. Which ones apply depends on the model. A value without `@` takes the sheet's `default effort` line, a level or `session`, and `session` when the sheet has no such line. `session` sets no effort, so the dispatch is the usual one. Strip the suffix before reading the model: `inherit-parent` or `auto` still omits `model` at every level, and a model name is passed as `model`. On Claude Code, a level picks the effort agent from the `subagent_type` you would otherwise use. `poteto-agent` becomes `subagent_type: "poteto-agent-<level>"`. `general-purpose`, or no `subagent_type`, becomes `subagent_type: "effort-<level>"`. The effort agents set only `effort`, so the model you pass still decides the model. On Codex, pass the level as `spawn_agent`'s `reasoning_effort` and keep the usual instructions.
