---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, data-backed thresholds, or finding a named Slack thread by person and date. Investigates GitHub/git, Linear CLI, the Codex Slack plugin, Axiom CLI, and Langfuse CLI in parallel, then returns a cited read on decisions and tradeoffs. Use how for runtime behavior."
disable-model-invocation: true
---

# Why

On Codex, read the [platform mapping](../poteto-mode/references/codex-tools.md), including its per-skill notes, before following this skill.

In T3 Code or the claudep profile, read the [profile routing](../poteto-mode/references/claudep-routing.md) before dispatching any role; it overrides native dispatch examples below.

Investigate the motivation and intent behind code. The companion `how` skill answers what the code does and how it works. `why` answers what forces led to its shape.

Each spawn below names a role line in `pstack-models.md` and a default in [Models](#models). Set `model` to that line's value, or to the default if the sheet or the line is missing. Leave `model` unset when the value is `auto` or `inherit-parent`. If the `Agent` tool rejects a slug, use the default and say so. If it rejects the default, use the closest valid slug of the same family from its error message.

## Operating Posture

Operate as a **careful, cautious, and precise investigator**. Be honest about what you know vs what you're inferring. Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the Target and the Question

The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** is usually a design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a broad history sweep.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from conversation context (open files, recent edits, cursor location, what was just discussed). State your interpretation briefly so the user can redirect if you're off, then proceed.

## Step 2. Establish the Code Anchor

Before spawning investigators, build the seed context inline: file paths and line ranges, key symbols (functions, classes, constants), the last few commits touching the target, PR numbers from merge commits (pattern `(#1234)` in the subject line), and any linked ticket IDs. Run `git blame -L <start>,<end> <file>` for last-touch commits, `git log --follow -p -- <file>` for full history with patches through renames, `git log --oneline -20 -- <file>` for recent commits with PR numbers visible, and `git log -1 --format=%B <commit>` to extract PR numbers. Then pull the PR bodies and discussion for any substantive commit: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`. This anchor goes to every investigator and to the synthesizer.

## Step 3. Spawn Parallel Investigators

**Default to the full parallel investigation.** The goal is a complete coverage map, not a minimal one. Document the null, don't skip the search.

### Discovery

Read [Evidence sources](references/source-playbook.md) and check only its five configured sources: GitHub/git, Linear CLI, Slack through Codex's plugin, Axiom CLI, and Langfuse CLI. Record availability and the intended search scope before dispatch. Check Axiom/Langfuse CLI capabilities and Slack plugin tools inside the Codex session that will execute the lookup; GitHub/Linear capability checks can run on either provider.

Aim for a complete **coverage map**. Report unavailable sources and empty searches separately.

Launch all relevant, available source investigators concurrently, one per source. Follow the profile routing to dispatch the configured provider and model through T3.

Each task uses the `why investigators` model and effort from the model sheet. Give it a read-only prompt, one source playbook, explicit search bounds, and an expected cited report. T3 delegates inherit the parent runtime mode; keep each task's edit scope explicit. Tool access and the read-only task scope are separate from permission mode.

Each investigator gets:
1. The base prompt from `references/investigator-prompt.md`
2. The category playbook `references/sources/<source>.md` for the selected source, using the access method in `references/source-playbook.md`
3. The cross-cutting `references/sources/incident-postmortem.md` **if the target code looks defensive** (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
4. The code anchor from Step 2 (file paths, symbols, commit hashes, PR numbers, ticket IDs)
5. The user's original question

### Investigator roster. One per configured source

1. **GitHub/git investigator.** Trace commits, PR descriptions, reviews, tests, and code comments for implementation-time rationale.
2. **Linear investigator.** Read linked tickets and CLI-visible issue history for product constraints and decisions.
3. **Slack investigator.** Run through Codex's Slack plugin for discussion threads, incident context, and original human rulings. When a keyword search misses a named thread, search by person and date window before you ask the user.
4. **Axiom investigator.** Query application logs and traces for runtime failures, timing, and evidence around the code's introduction.
5. **Langfuse investigator.** Inspect agent/LLM traces for prompts, generations, tool calls, latency, errors, and recorded scores that explain behavior.

### When to skip an investigator

Write the reason in Sources Consulted when a source is unavailable or provably irrelevant. Name a missing executable, missing plugin tool, authentication failure, or inaccessible scope as an evidence gap. An empty successful search is a result, not an unavailable source.

For a trivial question answered completely by the code and linked PR, answer inline after accounting for all five configured sources and explaining why further searches would be redundant.

## Step 4. Synthesize

Spawn one synthesizer subagent:

- `subagent_type`: `general-purpose`
- `model`: the `why synthesizer` line, default in [Models](#models)
- Task scope: read-only; retain the tools needed to spot-check citations through [Evidence sources](references/source-playbook.md). T3 delegates inherit parent runtime mode and follow profile routing. Route Slack, Axiom, and Langfuse lookups through Codex.

The synthesizer gets:
1. The investigator findings, including any null results and any categories skipped with justification
2. The code anchor
3. The user's original question
4. The epistemics framework from `references/epistemics.md`
5. The synthesizer prompt template from `references/synthesizer-prompt.md`

## Step 5. Present

Present the synthesizer's output to the user. You may lightly edit for clarity or add context from the conversation, but **do not rewrite the confidence language**.

## Output Format

The structure is the one in `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Adapt as needed, but keep the confidence separation intact, and keep Sources Consulted as one line per investigator, including the ones that returned nothing or were skipped, with the reason.

After Sources Consulted, if the user's `why` question is a precursor to changing this code, convert the lineage findings into a Preserve / Change / Avoid / Risk constraint set for planning the change.

## Common Failure Modes to Avoid

- **Recency bias**. Assuming the most recent commit is authoritative. The current shape is often the accretion of many earlier decisions. Trace back.

## Reference Files

- `references/epistemics.md`. Confidence tiers and phrasing guide. The synthesizer must follow it.
- `references/investigator-prompt.md`. Base prompt template for investigator subagents.
- `references/source-playbook.md`. Index pointing at the category playbooks below.
- `references/sources/*.md`. One self-contained example playbook per category, plus cross-cutting `incident-postmortem.md`. Give an investigator the single file that matches its category and use its configured CLI or plugin.
- `references/synthesizer-prompt.md`. Prompt template for the synthesizer subagent, including the output format.

## Models

Role defaults. A matching role line in the `pstack-models.md` override sheet overrides each at runtime; `/setup-pstack` writes it and lists its path per runtime.

- why investigators: `opus`
- why synthesizer: `opus`

## Reasoning effort

A role value in the override sheet may name a reasoning effort after its model, as in `opus @xhigh`. Levels on Claude Code: `low`, `medium`, `high`, `xhigh`, `max`. Which ones apply depends on the model. A value without `@` takes the sheet's `default effort` line, a level or `session`, and `session` when the sheet has no such line. `session` sets no effort, so the dispatch is the usual one. Strip the suffix before reading the model: `inherit-parent` or `auto` still omits `model` at every level, and a model name is passed as `model`. On Claude Code, a level picks the effort agent from the `subagent_type` you would otherwise use. `poteto-agent` becomes `subagent_type: "poteto-agent-<level>"`. `general-purpose`, or no `subagent_type`, becomes `subagent_type: "effort-<level>"`. The effort agents set only `effort`, so the model you pass still decides the model. On Codex, pass the level as `spawn_agent`'s `reasoning_effort` and keep the usual instructions.
