# t3-pstack-claudex

An opinionated pstack profile that runs Claude Code and Codex side by side inside T3 Code.

pstack is a set of agent skills, playbooks, and engineering principles written by Lauren Tan (poteto) for Cursor. Michael Denyer ported it to Claude Code as [pstack-claude](https://github.com/michael-denyer/pstack-claude). This repository is a fork of that port. It keeps the pstack workflow and adapts it to one setup: T3 Code as the host, with an isolated Claude Code profile and an isolated Codex profile that delegate work to each other.

## Lineage

| Layer | Source | What it adds |
| --- | --- | --- |
| pstack | [cursor/plugins/pstack](https://github.com/cursor/plugins/tree/e46364b8be46000b7df0f260550cd712afbb8d36/pstack) by Lauren Tan | The skills, playbooks, principles, and the `/poteto-mode` workflow. |
| Cursor team kit and thermos | [cursor/plugins](https://github.com/cursor/plugins) by Cursor | `deslop`, `fix-ci`, `fix-merge-conflicts`, `get-pr-comments`, `make-pr-easy-to-review`, `what-did-i-get-done`, `thermo-nuclear-code-quality-review`, `thermos`, and `thermo-nuclear-review`. |
| pstack-claude | [michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude) by Michael Denyer | Claude Code tool names, model defaults, and runtime adaptations. |
| Personal skills | [AmitRockBear/skills](https://github.com/AmitRockBear/skills) | Additional skills and workflow adaptations, including `html-communication`. |
| t3-pstack-claudex | This repository | T3 Code routing, mixed Claude and Codex model roles, isolated profiles, and guard hooks. |

[`skills/poteto-mode/references/licenses/NOTICE.md`](skills/poteto-mode/references/licenses/NOTICE.md) records the full provenance and the upstream licenses.

## What makes this version opinionated

- **T3 Code does the dispatch.** Subagents start through T3's `delegate_task`, so a Claude session can hand work to Codex and Codex can hand work to Claude. After each dispatch, the agent reads back the child's model and effort and compares them with the request. The rules live in [`skills/poteto-mode/references/claudep-routing.md`](skills/poteto-mode/references/claudep-routing.md).
- **Each role has one model.** Claude Opus 5.5 does the implementation and judgment work. GPT-6.1-Sol does the exploration, investigation, verification, and swarm work. Review panels mix both families. The table in [Models per task](#models-per-task) lists every role.
- **pstack starts only when you ask for it.** Every skill has `disable-model-invocation: true` except `html-communication`. Type `/poteto-mode <task>` to start the workflow. Plain sessions stay plain.
- **The profiles are isolated.** `claudep` and `codexp` keep their own config homes under `~/.pstack`. Your default `~/.claude` and `~/.codex` setups stay unchanged.
- **Hooks block risky git commands.** `git-backup-guard.sh` blocks `reset --hard`, `rebase --abort`, and detached checkouts until a `backup/` branch points at `HEAD`. `draft-and-stash-guard.sh` blocks draft PRs, which review bots skip, and `git stash`, which all worktrees share.
- **The settings favor long autonomous runs.** The profile uses `auto` permission mode at high effort, keeps automatic memory off, and turns on the task tools.

## Layout

The repository mirrors `~/.pstack`. Clone it to that path and use it there.

```text
~/.pstack
├── claudep                 # launcher: Claude Code with this profile's config homes
├── pstack-models.md        # model and effort for each pstack role
├── skills/                 # every skill, shared by both profiles
├── agents/                 # Claude Code subagent definitions
├── claude/                 # CLAUDE_CONFIG_DIR for claudep
│   ├── settings.json
│   ├── hooks/
│   ├── agents -> ../agents
│   ├── skills/<name> -> ../../skills/<name>
│   └── pstack-models.md -> ../pstack-models.md
└── codex/                  # CODEX_HOME for codexp
    ├── config.toml
    └── skills/<name> -> ../../skills/<name>
```

Claude Code and Codex write sessions, credentials, caches, and history into `claude/` and `codex/`. The `.gitignore` keeps all of it out of git.

## Install

You need T3 Code, the [Claude Code](https://code.claude.com) native install, the [Codex CLI](https://developers.openai.com/codex), `jq`, and `gh`.

1. Clone the repository to `~/.pstack`:

   ```bash
   git clone https://github.com/AmitRockBear/pstack-t3code-claudex-port.git ~/.pstack
   ```

2. Sign in to each profile once. Each profile keeps its own credentials:

   ```bash
   ~/.pstack/claudep
   CODEX_HOME=~/.pstack/codex codex login
   ```

3. In T3 Code, add two provider instances. In T3's settings file, the entries look like this, and T3 assigns the instance IDs:

   ```json
   "providerInstances": {
     "claudeAgent_claudep": {
       "driver": "claudeAgent",
       "displayName": "claudep",
       "enabled": true,
       "config": { "homePath": "~/.pstack/claude", "binaryPath": "~/.pstack/claudep" }
     },
     "codexp": {
       "driver": "codex",
       "displayName": "codexp",
       "enabled": true,
       "config": { "setupMode": "existing", "homePath": "~/.pstack/codex" }
     }
   }
   ```

   `pstack-models.md` names the Claude instance as `claudeAgent_claudep` in the `interrogate reviewers` row. If T3 gives your instance another ID, change that row.

4. Start a `claudep` thread in T3 Code and run `/setup-pstack`. The skill checks every role in `pstack-models.md` against the models that T3 reports, and asks you to replace any model that you cannot use.

5. Run `/poteto-help` to see the skills, playbooks, and principles, and to get help choosing one for a task.

### Add your own instructions

Each profile reads its own instructions file: `~/.pstack/claude/CLAUDE.md` for Claude and `~/.pstack/codex/AGENTS.md` for Codex. Git ignores both files, so your preferences stay local. The routing works without them. To give short names to models, add an `Agent delegation` section like the one below:

```markdown
## Agent delegation

- Resolve GPT or Sol to `codexp` / `gpt-6.1-sol` at high effort.
- Resolve Claude or Opus to `claudep` / `claude-opus-5-5` at high effort.
```

The workflows write plans, reports, and evidence under `~/.pstack/outputs`, and create worktrees under `~/.pstack/worktrees`. Git ignores both folders.

## Use it

- `/poteto-mode <task>` matches the task to a playbook (feature, bug fix, refactoring, investigation, babysit, shipping, and others) and runs that playbook with the principles and the model routing.
- `/how`, `/why`, `/architect`, `/arena`, `/swarm`, `/interrogate`, and `/thermos` run alone or as playbook steps.
- `/create-pr`, `/babysit`, `/fix-ci`, and `/get-pr-comments` handle PR work.
- `/unslop`, `/technical-writing`, `/deslop`, and `/no-comments` clean up prose and code.
- `/ketchup`, `/bro`, `/in-your-own-words`, and `/teach` make a session easier to follow.
- `/sharpen` improves a task prompt without carrying out the task.
- `/create-formal-verification-skill` and `/maintain-formal-verification-skill` create and maintain checks for properties that tests rarely reach.
- `/statechart` turns a TLA+ model into a chart of user-visible behavior, or an agreed chart into a model. Model checking needs Java 11 or later and the TLA+ `tla2tools.jar`; set `JAVA` and `TLA2TOOLS` to their locations. Run the bundled script with `--help` for commands and rendering options.

## Models per task

[`pstack-models.md`](pstack-models.md) maps each pstack role to a model and a reasoning effort. Change it with `/setup-pstack`, or edit the file directly.

| Role | Model |
| --- | --- |
| feature, refactoring | Claude Opus 5.5, high |
| bug fix | Claude Opus 5.5, high |
| perf issue | Claude Opus 5.5, high |
| hillclimb | Claude Opus 5.5, high |
| judgment and prose | Claude Opus 5.5, high |
| strongest judgment | Claude Opus 5.5, high |
| `how` explorer and explainer | GPT-6.1-Sol, high |
| `why` investigators and synthesizer | GPT-6.1-Sol, high |
| `reflect` tooling reviewer | GPT-6.1-Sol, high |
| `reflect` judgment, divergent, and synthesizer | Claude Opus 5.5, high |
| `arena` runners | Claude Opus, high, and GPT-6.1-Sol, high |
| `arena` cross-judge pool | Claude Opus 5.5, high |
| `swarm` workers | GPT-6.1-Sol, high |
| `architect` runners | Claude Opus 5.5, high, and GPT-6.1-Sol, high |
| `interrogate` reviewers | GPT-6.1-Sol, high, and Claude Haiku 5.5, high |
| change verification (`verify-change`) | GPT-6.1-Sol, high |

## License

MIT. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).
