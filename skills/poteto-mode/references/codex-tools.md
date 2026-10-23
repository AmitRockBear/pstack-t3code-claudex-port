# Codex tool mapping for pstack

pstack skills are written in Claude Code tool language (the `Skill` tool, the `Agent` tool, `AskUserQuestion`, Claude model names). On Codex the skills are the same files; only the tool names resolve differently. Read this when a pstack skill names a Claude tool, a driver or bundled skill, or a Claude model. This file is Codex-specific. Gemini CLI, opencode, Prime Agent, and other runtimes must use their own concrete tools, model names, and configuration paths.

## T3 Code override

Inside T3 Code, follow [profile routing](claudep-routing.md) for provider/model selection, effort, dispatch and child lifecycle; it takes precedence over the standalone native delegation and model mappings below.

## Tool actions

| pstack / Claude action | Codex equivalent |
|------------------------|------------------|
| Read a file | `shell` (`cat`, `head`, `tail`) |
| Create / edit / delete a file | `apply_patch` |
| Run a shell command | `shell` |
| Search file contents / find files | `shell` (`rg`, `grep`, `find`, `ls`) |
| Fetch a URL | `shell` with `curl` / `wget` |
| Search the web | `web_search` |
| Invoke a skill (the `Skill` tool, `/command`) | Skills load natively. Follow the instructions presented. |
| Dispatch a subagent (the `Agent`/`Task` tool) | `spawn_agent` |
| Dispatch N parallel subagents in one turn | N `spawn_agent` calls in one response |
| Wait for a subagent result | `wait_agent` |
| Free a finished subagent slot | `close_agent` |
| Track tasks (the todolist; `TaskCreate` / `TaskUpdate`, or `TodoWrite` on Claude Code) | `update_plan` |
| Ask the human a fixed-choice question (`AskUserQuestion`) | Use `request_user_input_async` when exposed, or `request_user_input` when the active mode permits it; otherwise ask in chat. |

Subagent dispatch needs `multi_agent` enabled. Add to `$CODEX_HOME/config.toml` (the claudep launcher uses `~/.pstack/codex/config.toml`):

```toml
[features]
multi_agent = true
```

Without it, optional exploration can run sequentially; a required independent review remains pending until a separate reviewer can run. A native thread-limit error is a capacity failure, not an invalid model. After the first rejection, stop native spawning and use T3 `delegate_task` for the configured role when supported; otherwise report the review gate blocked. Free a finished slot only through a close tool the host actually exposes.

## Subagent policy

Outside T3 Code, poteto-mode's Subagents section sets Claude-specific defaults (`subagent_type: "poteto-agent"`, `run_in_background: true`). On standalone Codex:

- There is no `poteto-agent` subagent type. Route an ad-hoc subagent through poteto-mode's style by dispatching a `spawn_agent` whose instructions tell it to read the `poteto-mode` skill in full first.
- `spawn_agent` calls already run concurrently with your turn, so `run_in_background: true` has no separate flag. Issue the dispatch and continue.
- There are no `effort-<level>` or `poteto-agent-<level>` types. When a role value carries `@<level>`, or the `default effort` line names a level, pass that level as `spawn_agent`'s `reasoning_effort` and keep the dispatch otherwise unchanged. `session` passes no `reasoning_effort`.
- There is no `comment-sicko` subagent type either. The **no-comments** skill spawns it on Claude Code; on Codex dispatch a `spawn_agent` whose instructions tell it to read `poteto-mode/references/agents/comment-sicko.md` in full first.
- Claude Code runs every subagent on this machine, so the **swarm** skill's workers and the fan-out playbooks (`orchestrate`, `autopilot-full`, `autopilot-stack`) isolate writers with worktrees. The same holds on Codex.
- Keep the rest of the policy unchanged. Pass file pointers not inlined context, give each worker its own worktree or branch when they write, review every subagent's diff yourself.

## Model names

Outside T3 Code, skills name Claude defaults (a single-role default for code/prose/judgment plus a diverse-model panel for diverse-model panels; each model-consuming skill lists its own in a Models section). These slugs do not resolve on standalone Codex. Substitute your configured Codex models:

- Single-model roles: your primary Codex model (for example `gpt-6-sol`).
- Roles that default to the strongest Claude model (`bug-fix`, `perf-issue`, `hillclimb`, `strongest judgment`): your strongest Codex model (for example `gpt-6-astra`).
- Diverse-model panels (`arena`, `architect`, `interrogate`, `how` critics, `reflect`): the adversarial signal comes from model diversity, so use the distinct Codex models available to you. A good default panel on ChatGPT is `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`. If only one model family is reachable, vary reasoning effort and note in the verdict that diversity was reduced.

`/setup-pstack` writes the configured model list. On Codex, set it to your Codex model slugs.

## Driver and bundled skills pstack references

The [driver policy](../SKILL.md#non-negotiables) selects the app driver. For skills and drivers named by these workflows, use these Codex equivalents:

| Skill or driver named in pstack | On Codex |
|---------------------------------|----------|
| `run` (drive a CLI/TUI to see a change work) | Run the app yourself via `shell` and observe the real output. |
| Project UI driver | Drive the UI with whatever automation you have, or hand the user a concrete manual check. Do not claim done without observing the artifact. |
| `plugin-dev:skill-development` (Claude's SKILL.md authoring guidance) | Follow your platform's skill-authoring guidance; the `writing-skills` skill if present. Keep `name` + `description` frontmatter and progressive disclosure. |
| `loop` (recurring/self-paced re-invocation, used by `babysit`) | For T3 PR monitoring, follow [Babysit](../../babysit/SKILL.md). For authorized T3 program supervision, follow the persistent schedule in profile routing. Outside T3, use the host's supported wake mechanism. |

## Per-skill notes

Affected skill entry points and the optional Codex slash stubs point here. The native dispatch and model substitutions in this table apply to standalone Codex; T3 roles follow [profile routing](claudep-routing.md).

| Skill | On Codex |
|-------|----------|
| `interrogate` | The `subagent_type` and `model` dispatch fields map to `spawn_agent`; express read-only scope in the prompt; substitute your configured Codex models and keep the reviewer panel model-diverse. |
| `setup-pstack` | The skill's Other runtimes table names the Codex sheet path and how it loads; the slugs are your Codex models (see Model names above). The role rows are identical. |
| `no-comments` | There is no `comment-sicko` subagent type; see Subagent policy above. |
| `teach` | Running `how` and `why` in parallel maps to `spawn_agent` fan-out; image generation uses the configured Codex equivalent. |
| `create-verification-skill` | The generated app-specific recipe lands under `.claude/skills/verify-<app>/` on Claude Code; write it to Codex's project-skill location instead. Read its actions through shared verify-change. The app-driving harness is platform-neutral. |
| `maintain-verification-skill` | The parallel per-feature source readers map to `spawn_agent` fan-out; the project-local skill lives under Codex's skills location, not `.claude/skills/`. |
| `babysit` | In T3, follow [Babysit](../../babysit/SKILL.md). Outside T3, `loop` and `AskUserQuestion` resolve through the tables above. |
| `automate-me` | `plugin-dev:skill-development` resolves through the skills table above. |
| `architect` | The runner panel goes through the **arena** skill, so its `spawn_agent` fan-out and model substitution apply here too. |
| `arena` | The parallel candidates and the cross-judge map to `spawn_agent`; substitute your configured Codex models for the runners and the cross-judge pool (see Model names above). |
| `how` | The parallel explorers and the explainer map to `spawn_agent` fan-out; substitute your configured Codex models. |
| `reflect` | In T3, use reflect's `t3_thread_read` activity evidence and configured role dispatch. Outside T3, use native transcript evidence when supported or its factual fallback digest. |
| `swarm` | Each worker is a `spawn_agent` call on your configured Codex model, and those calls already run concurrently; give each writing worker its own worktree or output directory (see Subagent policy above). |
| `why` | The parallel investigators and the synthesizer map to `spawn_agent`; substitute your configured Codex models. Check the five sources in the why skill's source-playbook.md; use the installed CLI commands and discover Slack plugin tools inside the executing Codex session. |

## Vendored scripts

For T3 PR monitoring, follow [Babysit](../../babysit/SKILL.md); retain finite inspection and cancellation commands for merge safety.

`skills/poteto-mode/scripts/` ships the `watch-pr` PR watcher, the `orch` store CLI, and `worktree-audit.mjs`. The `watch-pr/ship-pr` command owns pending-merge inspection and cancellation; `resume.mjs` owns the shared checkpoint locator described in [Resume storage](resume-storage.md). These scripts use bun and Node.js and run the same on Codex; invoke them through `shell`. Install `bun` and `gh` for the commands that use them; install `gt` only when a selected project command requires it. Run `worktree-audit.mjs` with `node` and explicit task-relevant transcript roots, including scoped Codex sessions or archived sessions when applicable. Supplement native evidence with T3 thread and owned-task usage checks before cleanup. It imports the transcript walker from `skills/reflect/scripts/find-transcript.mjs`, so keep the `reflect` skill installed beside `poteto-mode`.

## Instructions file

Where a pstack skill says "your instructions file", on Codex that is `AGENTS.md` (project root, plus `$CODEX_HOME/AGENTS.md` global). On Claude Code it is `CLAUDE.md`.
