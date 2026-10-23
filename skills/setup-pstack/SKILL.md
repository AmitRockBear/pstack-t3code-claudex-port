---
name: setup-pstack
description: Configure which models pstack uses per role. Detects available models and writes the current runtime's override sheet. Use for /setup-pstack, "configure pstack models", or changing pstack's model choices.
disable-model-invocation: true
---

# Setup pstack

On Codex, read the [platform mapping](../poteto-mode/references/codex-tools.md), including its per-skill notes, before following this skill.

In T3 Code or the claudep profile, read the [profile routing](../poteto-mode/references/claudep-routing.md) before dispatching any role; it overrides native dispatch examples below.

On another runtime, read [Other runtimes](#other-runtimes) below for where the sheet lives and how it loads; the steps are the same.

On the claudep profile, edit `<config>/pstack-models.md` directly. Activated pstack workflows read that sheet through profile routing. Preserve explicit-only activation on re-runs: leave pstack includes out of profile startup instructions, and preserve the skills' manual-only frontmatter as described in step 6. For other profiles, use the path in [Other runtimes](#other-runtimes). Each pstack skill names a default model inline; the override sheet adapts those defaults to the models you actually have access to.

Claude Code has no auto-applied "rules" mechanism like Cursor's `.mdc`. The Claude Code config directory is `$CLAUDE_CONFIG_DIR` when that variable is set and `~/.claude` otherwise. This skill calls it `<config>`. Inclusion is explicit: the user adds a line to `<config>/CLAUDE.md` (or their project `CLAUDE.md`) such as:

```text
@<config>/pstack-models.md
```

with `<config>` written as the resolved path, so the file is loaded as context for every session.

The Codex home directory is `$CODEX_HOME` when that variable is set and `~/.codex` otherwise. This skill calls it `<codex-home>`.

## Steps

### 1. Detect available models

In T3, call `orchestrator_capabilities` and validate every selection against its provider's models and model-specific options. Preserve this profile's existing role choices, efforts and panel counts unless the user requests changes. Use the profile routing for dispatch, including explicit `<providerInstanceId>/<modelId>` entries when a model exists on multiple providers. The native family/model instructions below apply outside T3.

Enumerate the model names the `Agent` tool's `model` parameter accepts in this session. That is the dependable source. On Claude Code they are the family names listed in [Models](#models) below, each running that family's current model. For this profile, use the family alias pinned by the profile settings; select effort separately. The default panel is listed there too. The panel is chosen for cross-family diversity. Ask the user to confirm or paste any additional slugs they want available. Never write a real slug you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid even though they are not detected slugs. Both mean the role runs on the parent session's model, which the `Agent` call expresses by omitting `model`.

### 2. Load current state

The default role-to-model mapping is the rule shape shown in the Write the override sheet step below. If the current runtime's sheet already exists, read it and treat its values as the current choices. Otherwise start from those defaults. A line whose role is not in that shape, such as `how critics`, is from a retired role. Drop it. Outside T3, an older sheet may name full Claude model IDs that the native `Agent` tool rejects; replace each with its family name, the word after `claude-`; inside T3, preserve full catalog model IDs and any explicit provider prefix.

### 3. Map and confirm

Show every role with its current model, marking any real slug not in the detected set as needing a choice. Also list each line step 2 dropped or rewrote. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto` as the options. Prefer `AskUserQuestion` over free text. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

Then ask for the default reasoning effort, the `default effort` line. It is `session`, which keeps the parent session's effort, or a level supported by the selected models' live catalog in T3 (the levels in [Models](#models) outside T3). Start from the existing default. Every role value without a suffix runs at it. Then ask whether any role should run at another level. On Claude Code a role value may carry one after its slug, as in `<slug> @xhigh`; panel entries take their own, as in `<slug> @xhigh, <slug> @max`. Inside T3, pass effort through the selected model's catalog option, independently of the parent session; outside T3, use the native effort controls supported by that provider. Leave the suffix off for the default effort.

### 4. Validate

Inside T3, validate provider availability, exact model ID and effort option against `orchestrator_capabilities`; outside T3, validate against the native provider tool. `inherit-parent` and `auto` always pass. Validate each model without its provider prefix or `@<level>` suffix, and validate the effort against that model's live option values in T3 or native effort controls outside T3. The `default effort` must be supported by every affected model, or `session` to preserve inheritance. If a chosen real slug or level is not available, stop and ask again.

### 5. Write the override sheet

For claudep, preserve the current sheet's T3 routing preamble, role choices, efforts and panel counts unless the user requests changes; the block below shows generic standalone defaults, not this profile's replacement contents. Write the current runtime's sheet with the shape below. Overwrite the whole file so re-runs stay idempotent.

```markdown
# pstack model configuration

Per-role model overrides for pstack skills. Each pstack SKILL.md names its defaults in a Models section; the values here override those defaults. Delete a line to fall back to the skill default. A value of `inherit-parent` or `auto` runs that role on the parent session's model (the `Agent` call omits `model`); an alias entry in a panel list still counts toward that panel's fan-out. A model may carry a reasoning effort, as in `opus @xhigh` (levels: low, medium, high, xhigh, max); the role then runs through the pstack effort agent of that level, each entry of a panel list on its own. `default effort` sets the level for a value without one; `session` keeps the parent session's effort.

feature, refactoring: opus
bug-fix: fable
perf-issue: fable
hillclimb: fable
judgment and prose: opus
strongest judgment: fable
how explorer: opus
how explainer: opus
why investigators: opus
why synthesizer: opus
reflect tooling: opus
reflect judgment, divergent, synthesizer: opus
arena runners: opus, fable, sonnet
arena cross-judge pool: opus, fable, sonnet
swarm workers: opus
architect runners: opus, fable, sonnet
interrogate reviewers: opus, fable, sonnet

default effort: session
```

### 6. Wire it in

On claudep, keep one regular model sheet at `<config>/pstack-models.md`, read when pstack is explicitly activated. Preserve the profile's manual activation rule and leave model/routing includes out of startup instructions. Preserve `disable-model-invocation: true` in every bundled skill except `html-communication`. Activated workflows read helpers by file path. On other Claude Code profiles, if `<config>/CLAUDE.md` does not already include `<config>/pstack-models.md`, append an `@` line naming the sheet's resolved path, so model rows load on every session. If the user prefers project scope, add the include to the project's `CLAUDE.md` instead.

For the isolated claudep Codex worker, preserve its explicit activation rule and load the shared sheet only inside activated work. On other Codex profiles, paste the model rows and the `default effort` line into `<codex-home>/AGENTS.md`; Codex has no `@` include.

### 7. Confirm

Tell the user where the override was written, and how its model rows load. Re-running this skill updates the override sheet.

### 8. Offer an app verification skill (optional)

If the project has no driver skill or harness for the real app, offer once to generate one with [create-verification-skill](../create-verification-skill/SKILL.md). On yes, read and follow that skill; on no, continue.

### 9. Offer a formal verification skill (optional)

If the project has no skill that runs a model checker, prover or code-level verifier, offer once to generate one with [create-formal-verification-skill](../create-formal-verification-skill/SKILL.md). On yes, read and follow that skill; on no, continue.

## Other runtimes

The role lines are the same everywhere. What differs is the sheet path, how the runtime loads it, and how you list models. Detect models with the runtime's own tool and never write a slug you have not seen listed. A runtime whose subagent call has no model parameter still gets the sheet, as the record of the user's choice, and applies it where it can.

| Runtime | Sheet | Load | List models | Status |
| --- | --- | --- | --- | --- |
| T3 Code (claudep configuration) | `~/.pstack/pstack-models.md` | read via profile routing from every provider | `orchestrator_capabilities` | verified live |
| Claude Code | `<config>/pstack-models.md` | `@<config>/pstack-models.md` in `<config>/CLAUDE.md` | the `Agent` tool's model parameter | verified live |
| Codex | `<codex-home>/pstack-models.md` | model rows: paste into `<codex-home>/AGENTS.md` | your configured Codex models, see [codex-tools.md](../poteto-mode/references/codex-tools.md#model-names) | discovery verified |
| opencode | `~/.config/opencode/pstack-models.md` | add the path to the `instructions` array in `opencode.json` | the `models` slash command in the session | from published docs, no live session |
| Gemini CLI | `~/.gemini/pstack-models.md` | `@~/.gemini/pstack-models.md` in `~/.gemini/GEMINI.md` | the `model` slash command in the session | from published docs, no live session |
| Prime Agent | no documented sheet path; Prime's configuration chooses models | | | no live session |

## Models


- Available Claude models: `opus`, `fable`, `sonnet`, `haiku`
- Default panel: `opus`, `fable`, `sonnet`
- Reasoning effort levels: `low`, `medium`, `high`, `xhigh`, `max`
- Default reasoning effort: `session`
- Single-role default: `opus`
