### Orchestrate

Resolve the driver skill through [poteto-mode's Non-negotiables](../SKILL.md#non-negotiables).

**You own the program, never the code. Author briefs, drain the queue, keep the frontier green, decide.** For a whole project handed to one standing coordinator chat: multi-day, many stacked PRs, dozens to hundreds of subagents, the human checking in twice a day instead of every five minutes. One task driven to a predicate is Autonomous run. One ambitious run needing a bespoke workflow is figure-it-out. Route here when the work outlives any single agent. Work one agent could finish inside the session's budget is not a program.

Ceremony must scale with the program. On cheap near-identical units, collapse it as each section directs. Start implementation only within the user's authorized scope. Merging, direct pushes to the landing branch, auto-merge and merge-queue admission require explicit approval for the requested PRs or stack; a program execution grant alone does not authorize landing.

Three rules carry the rest.

- Completions are queue events, not interrupts.
- Every spawn and every resume carries the standing orders verbatim.
- The brief is the product. A vague brief fails quietly, because a worker cannot ask you a question.

#### Roles and placement

- **Coordinator (this chat).** Frames, authors briefs, drains the inbox, owns the human report, makes judgment calls. It never authors or edits code. Conflicted merges, restacks, and code changes are always tasks. The coordinator may prepare a clean integration locally; publishing to the landing branch requires the explicit landing approval above and the safeguards in [Shipping](shipping.md). Queueing finished work behind an idle stacker is how a deadline harvests nothing. The loop is agentic end to end. Dispatch and manage task-owned agents through [profile routing](../references/claudep-routing.md), using T3 delegation when applicable. State reads and writes go through the `orch` CLI at drain points, one command in and one line out. The CLI never spawns, waits, or wakes anything.
- **Sub-coordinator.** Durable, one per track, and only when the program exceeds what one coordinator's drains can manage. A track the coordinator can drain itself needs no middle layer. Each nested layer re-pays a full orientation preamble, and a blocking sub-coordinator hides its children while the parent idles. Owns its track's units and boards, authors its workers' briefs, spawns its own workers and verifiers where the runtime lets a subagent spawn one. Where it does not, it owns its track's units directly with the same review separation. Rolls up aggregates at wave boundaries. Never forwards raw child reports. Cap in-flight children at what one drain can process, roughly ten, as a rolling window. Never as blocking batches, which cost the slowest child of every batch.
- **Worker / verifier.** Background subagents (`run_in_background: true`). Claude Code has no remote worker environment, so isolation is a separate worktree per concurrent writer, not a separate machine. Runtime verification goes through the driver skill. The brief names its resolved skill path or exact commands. A subagent never sees this chat, so its brief inlines what it needs or points at repo and store paths. Prefer fewer, broader workers. One writer per worktree (principle-separate-before-serializing-shared-state). Use one independent verifier through [verify-change](../../verify-change/SKILL.md); the verifier did not write the code.

Depth stays at coordinator, track, worker. Author the track decomposition per project (build, landing, and verification are common cuts, not a required shape). Hard-coded swarm trees were tried and parked as too rigid.

#### Store layout

Create `~/.pstack/outputs/<project-slug>/orchestrate/<program-slug>/`, outside the repo and outside the session. Pass this path with `--store <path>` on every `orch` command. The store has to outlive this chat: the program runs for days, a session restart is expected (see Liveness and failure), and the store is the postmortem. The session scratchpad is not a candidate, however convenient. It is session-scoped and temporary, so a restart takes the program's only state with it. Every file has exactly one writer. Owners publish facts, readers aggregate at read time. Use `bun skills/poteto-mode/scripts/orch/orch.ts` under the installed plugin for bookkeeping, written below as `orch`, while its canonical plain TSV and JSON stay readable without the CLI.

- `preferences.md` is the standing-orders register: numbered lines, one constraint each (model policy, stack shape and count, verification bar, forbidden paths, escalation policy). For human rulings, retain original wording and attribution per [Claims about human decisions](../../why/references/epistemics.md#claims-about-human-decisions). Label agent interpretations and missing originals. Copies are not new decisions. Paste it verbatim into every spawn and every resume. Directives decay across resumes, and each dropped one costs a human turn. Record accepted task decisions with their original attribution; propose durable instruction or skill changes instead of creating new standing rules from agent interpretations.
- `overview.md` is the durable PR and issue DB. Append. Never rewrite wholesale per event.
- `units.tsv` has one row per unit: id, track, state, branch, PR, head SHA, brief path. Update rows in place.
- `frontier.json` is the computed merge frontier, per Stack safety.
- `ledger.tsv` is the verification ledger, per Verification.
- `inbox/` holds completion pointers. `gates.md` parks human gates (question, options, approval state). Record `pending` as the default when approval is required; silence does not grant approval.
- `decisions.tsv` is the trail via the show-me-your-work skill.
- `status.md` is derived from `units.tsv` and `ledger.tsv` at each drain, never hand-maintained. Regenerate it from the tables instead of narrating events into it.

#### The brief

Your prompts to agents are your only product, and a sloppy brief compounds into slop across the whole tree. Every spawn carries all of it. A field you cannot fill is a unit you have not scoped yet.

```
GOAL         one sentence, the outcome, executable by a stranger with no chat access
SCOPE        paths this unit may write; paths it may not; its exclusive worktree or branch
CONTEXT      relevant files, PRs and upstream findings; preserve exact constraints
             and evidence pointers without copying unrelated report text
ACCEPTANCE   checkable criteria, one per line
VERIFY       exact commands or the resolved driver skill path, plus known gotchas
TIMEBOX      rough cap on runtime; on expiry, return partial findings and stop rather than run on
FORBIDDEN    no topology changes, no landing without approval, no fixes outside scope
REPORT       status, branch, head SHA, PRs, verdict, what you actually ran, deviations,
             suggested follow-ups
STANDING     <preferences.md pasted verbatim>
REVIEW       <review standard from babysit/SKILL.md pasted verbatim, for any unit that handles review comments>
```

Size the brief to the unit. A one-command unit gets the template collapsed to a paragraph that still names goal, scope, the verify command, and the report shape. A 4KB scaffold around a two-line edit costs more to write and obey than the edit. A spawn may reference the standing-orders file by store path. Verbatim paste is for every resume and for any brief that has to stand alone.

A sub-coordinator brief adds its track boundary and unit list, its spawn budget, the drain protocol, and the rollup format (per child: name, status, PR, head SHA, verdict, one line, plus track status and frontier delta).

A dependency is a context relay, not just ordering. Undeclared upstream context makes the worker guess. Missing fields are a refuse-to-spawn condition. Audit one sampled worker brief per sub-coordinator per wave, concurrently with the wave it samples, never as a gate in front of it. A failing brief stops that track and fixes the sub-coordinator's instructions, not just the worker, because brief quality decays late in a run. Never resume-chain a brief. Respawn fresh with consolidated scope.

#### Steps

1. **Frame.** State the done predicate as something countable ("all 126 units independently verified and merge-ready"). Include merged units only within explicit landing authorization. Quantify scope: units, rough effort, expected stacks, and the wall-clock budget. If one agent could finish inside that budget, stop here and run Autonomous run instead. Collapsing must not depend on another document being present. It means do the work directly in this session, plain workers where they help, verification through verify-change, landing only when explicitly authorized, and none of the store, register, or pilot machinery below. Schedule landing against the budget. By roughly 70% of it, stop spawning and finish verification and handoff; land verified work only within explicit approval. Name the tracks per project. A contested decomposition or one-way door goes through the arena skill before the pilot. Present the framing once. Reversible prep proceeds without waiting.
2. **Install the runtime.** Run `orch init`. Open the trail via the show-me-your-work skill, write the standing orders before any spawn, and seed `frontier.json` from the requested bottom-to-top PR list with `orch frontier set --repo <repo-dir> --prs <bottom,...,tip>`. If no PR exists yet, initialize the frontier when the first completed PR opens.
3. **Pilot.** Push one unit through the whole path: brief, worker, verification, stack entry and ledger row, then merge only when explicitly authorized. The pilot exists to falsify the brief template, the verify recipe, and the unit size while that costs one agent instead of fifty. Fix the contract from pilot evidence before any fan-out. Scale the pilot to the unit. On programs of near-identical cheap units, the first unit is the pilot and fan-out starts when it is independently verified and ready. Reuse its applicable setup evidence for later units instead of building a separate pilot bureaucracy.
4. **Scale.** Spawn a rolling window of workers up to the in-flight cap, refilling as children finish. Blocking batches pay the slowest child of every batch. Spawn track sub-coordinators only past the one-drain threshold in Roles. Recompute ready work after each drain. Relay upstream reports into downstream briefs. Keep sibling communication upward only. The sampled brief audit runs alongside the wave it samples and stops the next refill on failure, not the current one.
5. **Drain.** Run the queue discipline below at every drain point.
6. **Prepare and hand off.** Integration starts with the first verified unit and runs alongside the remaining waves. Open PRs only after implementation, cleanup, required pre-push checks and focused development checks are complete. The stacker prepares dependent branches; publish or merge into the landing branch only within explicit approval and [Shipping](shipping.md). Keep verified work merge-ready when approval is absent. Keep the frontier green before upper-stack work. Stack safety governs. Advance `frontier.json` only on merge or reported new head SHAs.
7. **Close.** Drain the final inbox, reconcile every spawned agent to a terminal row (done, abandoned, zombie-reconciled), confirm the predicate on the real artifact, confirm every landed PR has a verdict for its current head SHA, include the decision trail in the existing independent source audit, and retain accepted decisions in the program state. Propose persistent instruction changes separately. Leave the store intact. It is the postmortem.

#### Queue and drain

- On a completion notification, run `orch inbox push <agent> <unit> <status> [--report PATH]` and return to what you were doing. Never deep-review inline. A completion that needs review becomes a verifier unit. Never review a diff inside a drain.
- Drain in batches at four points: the end of a critical section, a track rollup, a frontier watcher wake (arm it through the harness-owned wake mechanism, with a long heartbeat fallback), and before a human report. Begin each batch with `orch inbox drain`. Arrivals during a drain wait for the next one.
- Critical sections you finish first: authoring a brief, a stack operation, a conflict decision, writing a gate, updating ledger or frontier.
- Each drain classifies every pointer (landed, needs-verify, failed, zombie, noise), writes the resulting rows through `orch unit add`, `orch unit set`, and `orch ledger record`, runs `orch status`, then spawns the next wave in one message.
- Account for every spawned child at its track's rollup: arrived, respawned, or its scope explicitly absorbed. Silently redoing a missing child's work hides both the wasted spend and the coverage gap its result existed to close.
- A drain turn ends with the three lines from `orch status`: counts against the states, what changed, gates open. Detail lives in `status.md`. The full reply contract applies at checkpoints and close.

#### Stack safety

- The frontier is a computed object, never narrative. Recompute `frontier.json` with `orch frontier set --repo <repo-dir> --prs <bottom,...,tip>` after each completed stack mutation or confirmed merge. The command reads current PR heads, bases and states through `gh` for that scoped list and rejects invalid order or unavailable state. Do not require Graphite.
- Exactly one topology writer per stack may rewrite or retarget branches, serialized within its stack. Follow [Merge and restack safety](../references/merge-safety.md) before rewriting, including cancellation of pending merges and explicit remote-SHA leases. Record the holder in the standing orders. A restack at this scale is slow and blocks whoever runs it, so give it its own unit and keep the coordinator out of it.
- Workers never change stack topology. Refresh against `origin/main` only for conflicts or a relevant change that must be incorporated; do not rebase on a timer just to stay current. In T3, the coordinator owns each stack's frontier watch under [Babysit](babysit.md), delegates finite fixes, and sends conflicts to the stacker. Outside T3, one babysitter per stack follows `playbooks/babysit.md`, scoped to one immutable frontier generation, and reports conflicts to the stacker.
- PR closes and retargets go through the stacker only. Closing a base PR orphans every chain above it. Merges and stack surgery are units with briefs like any other.
- One retro watcher follows merged PRs for reverts, post-merge CI breaks, and orphaned follow-ups.

#### Verification

Owners run required pre-push checks and focused development checks and hand commands, fixtures, exact revisions and receipts to one independent verifier following [verify-change](../../verify-change/SKILL.md). Run one independent source audit by default and a second only for the five cases in [Multi-phase plan's audit policy](multi-phase-plan.md). Keep one verifier for a small unit; avoid fixed lane counts or extra model-family panels.

Write ledger rows with `orch ledger record`. Check the current PR and head SHA with `orch ledger check`. `ledger.tsv`, one row per verdict, keyed by PR number plus head SHA: `live-ui-verified | unit-test-verified | type-check-only | verifier-blocked | verifier-failed`. CI green is an input to a verdict, not a verdict. Behavioral work needs better than `type-check-only`. `verifier-blocked` is not a pass. Respawn when the environment heals. `verifier-failed` gets a fix unit, not a re-verify. Worker checks are development receipts; the independent verifier owns the final verdict. A new head requires a new recorded assessment, not automatic full verification. Reassess through [verify-change](../../verify-change/SKILL.md) and [Shipping](shipping.md); satisfy required CI and mergeability. The ledger answers "was this verified", not memory and not the transcript.

A unit is not done until its output is externalized the moment it lands, never batched to the end of the run. A worker pushes its branch, a verifier writes its ledger row, receipts land in the store. Work that exists only on one VM when that VM dies was never done.

#### Liveness and failure

- Never resume an agent to check on it. A resume restarts an idle agent. Probe read-only: the ledger, `units.tsv`, `gh`, pushed branches, and the background task list. Transcript mtime is not liveness.
- Before replacing a writer, inspect its pending children and confirm terminal state or cancellation through profile routing.
- A silent death gets a synthetic postmortem row in the inbox (unit, failure mode, last evidence, options). Replan on evidence as it arrives. Never wait for full quiescence.
- Retry by mode: cap-hit or oom, respawn with smaller scope. Network-drop, retry as-is. Tool-error, inspect the failure and correct actionable arguments; preserve the configured model unless the user authorizes another. Unknown, retry once. Two retries, then abandon the unit and replan around it.
- A zombie that returns hours late reconciles against the current frontier and ledger before anything is accepted. Salvage unique findings through a fresh unit, never a blind merge.
- When continued spawning would produce garbage tree-wide (bad upstream output, broken acceptance, dead infra), write a stop line at the top of the standing orders, let in-flight work finish, fix the cause, clear it.
- Bound your own infra retries the same way you bound a child's. After a few consecutive tool aborts, stop retrying. Write a terminal handoff to durable state (what is done, where it lives, the exact command to resume) and end the run.
- After a session restart, inspect task-owned child state through profile routing before deciding that a worker is lost. Pushed branches, open PRs and the store remain recoverable. Re-read the standing orders and `units.tsv`, recompute the frontier, reconcile PRs, branches and recorded task IDs, reattach active task-owned children and replace confirmed lost workers from their stored briefs and current state, using sub-coordinators only when the program still needs them, drain, resume. The dead session's store lock clears itself on the next write. `orch` replaces a lock whose holder pid is gone.

#### Escalation

Reaches the human, batched into the status page rather than per item: irreversible actions (force-push to shared branches, deploys, deletions, closing someone else's PR), genuine product or preference calls no experiment settles, a standing order that contradicts observed reality, a program-level dead end that survived a replan. Park each as a `gates.md` entry before asking, and route work around it.

Resolve routine mechanics within the grant: frontier updates, safe restacks, bounded retries, CI flake triage, review-thread triage and format fixes. Keep unresolved product or architecture decisions and landing approvals with the user; route other work around those gates.

Mid-run discoveries fix only what blocks the frontier. Everything else parks in follow-ups. At this fan-out a small scope leak multiplies into PRs nobody asked for.

**Reply:** at checkpoints and close: the predicate and the count against it from `units.tsv` and `ledger.tsv`, tracks and what each landed, the frontier (PR list plus SHAs), verdicts summary, what was abandoned and why, gates awaiting the human (the only asks), the store path, and the trail path. Numbers from the tables, not narrative. Include PR links.
