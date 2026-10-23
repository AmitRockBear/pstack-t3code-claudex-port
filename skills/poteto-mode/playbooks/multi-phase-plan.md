### Multi-phase or multi-PR plan

Resolve the driver skill through [poteto-mode's Non-negotiables](../SKILL.md#non-negotiables).

**You own the plan, not the code. The plan is a checklist an owner runs box by box and the operator audits from the evidence.** The plan is the deliverable. Do not implement.

1. When the change is one or two files with an obvious approach, skip the plan. Say so and stop.
2. Resolve empirical questions through /prototype, ground architectural alternatives through /architect, and reserve user questions for remaining decisions they own. Keep prototype revisions and relevant evidence in Appendix A.
3. Explore in subagents with `subagent_type: "poteto-agent"` and an explicit model per the Subagents section (the **guard-the-context-window** principle skill). Each returns file pointers, conventions, test commands, and entry points. No inlined dumps.
4. Copy the skeleton below into the plan file and fill every placeholder. Resolve the skeleton's verify-change link to the installed skill's absolute path so the plan works outside the plugin. Unless the operator names a path, write the plan under `~/.pstack/outputs/<project>/<task>/`. Keep every heading and every sub-block in the order shown. One section per PR. One PR is one change with its own evidence (the **sequence-verifiable-units** principle skill). Name the execution playbook in **How to read this**. Pick between `playbooks/autopilot-full.md` and `playbooks/autopilot-stack.md` per the rule at the end of `playbooks/autopilot-stack.md`. A standing program takes `playbooks/orchestrate.md`. The execution playbook owns base selection, topology changes, and merge authority. Do not copy its rebase steps into the plan.
5. Write under `/technical-writing` in full, then `/unslop`. The body is one Diátaxis mode, how-to. Appendices hold explanation and reference. Each heading states the task or the finding. No long dashes. No mid-sentence colons.
6. Run `node skills/poteto-mode/scripts/check-plan.mjs <plan.md>` from the installed plugin and fix every line it prints (the **encode-lessons-in-structure** principle skill).
7. Hand back. Post the plan path and the script's output, then stop. Execution starts on the operator's explicit go, under the execution playbook the plan names. When the user reserves execution-mode selection, recommend stack or full autopilot and ask after plan approval, before execution.

**Verification.** A PR is verified only when required checks, change-driven runtime scenarios, applicable performance checks, and independent audits have evidence. Use one independent verifier through [verify-change](../../verify-change/SKILL.md) for routing, scenario coverage, evidence assessment and revision tracking. The verifier did not write the code and may cover multiple scenarios. Reassess rewritten landing context under [Shipping](shipping.md).

**Performance.** Require measurements only for a performance-sensitive path or an agreed budget. Otherwise write `**Verify, perf.** None. <Reason performance is unaffected.>` with no boxes. When required, write `**Verify, perf.** Required. <Reason.>` and name the metric, interleaved base/head probe, baseline and failure threshold. If the baseline lacks the feature, isolate the added work and set absolute budgets instead of comparing unlike scenarios. The verifier runs the performance checks.

**Audits.** Run one independent read-only source audit of correctness, affected callers and the verification receipts. The auditor did not write the code. Declare applicable second-audit cases in each PR's `Verify, audit` block; use `None` with a reason when no case applies. The first auditor checks that declaration against the diff. Correct an incomplete declaration and obtain the required second audit before a clean verdict. Add exactly one second auditor when any of these cases applies, with a distinct focus on all declared risks.

- `authorization`. Authentication, authorization or tenant isolation changes.
- `security`. Sensitive-data exposure, secrets, untrusted input or security-boundary changes.
- `data`. Schema migrations, destructive data operations or persisted-format compatibility changes.
- `concurrency`. Concurrency, retries, idempotency or lifecycle changes with race or duplication risks.
- `shared-contracts`. Shared contracts or infrastructure changes whose affected callers span multiple services or product modes.

Include the [Babysit review-comment rubric](../../babysit/SKILL.md) and relevant accepted decisions in every audit brief. Classify findings against the current source, accepted scope, benefit and complexity, and agreed behavior.

**Review gate.** An explicitly requested UI review uses screenshots and video before merge. Otherwise record `None` with the reason. A UI review request authorizes only its stated scope; merge authority still belongs to the execution playbook.

**Driver skill.** Select it through the Non-negotiables and put the resolved skill path or exact commands in the verifier's boot recipe. Native mobile uses whatever simulator-driving skill the repo has. A PR that touches two surfaces gets scenarios on both. A surface with no driver skill is a risk in Appendix C, and its live block still names how the verifier exercises it.

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, the rule the program enforces, and the PR ids in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs `skills/poteto-mode/playbooks/<execution playbook>.md` from the installed plugin. <Who prepares each PR for landing, and who performs the authorized merge or delivers the verified stack.>

Approval to execute the plan does not authorize landing. Merging, auto-merge and merge-queue admission require the operator's explicit approval for the requested PRs or stack.

Tests alone are not sufficient verification. A PR is verified only when required checks, change-driven runtime scenarios, applicable performance checks, and independent audits have evidence.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the operator, then stop. Start execution only on the operator's explicit go.
- [ ] On the operator's go, write this exact text into the standing orders and restate it in your todolist. "<The plan path, the PR ids in order, the verification rule, who merges, and the done condition.>"
- [ ] Read these from the installed plugin at program start. Re-read them at every tick.
  - [ ] `skills/poteto-mode/playbooks/<execution playbook>.md`
  - [ ] `skills/verify-change/SKILL.md`
  - [ ] `<driver skill path>`
  - [ ] `skills/poteto-mode/playbooks/opening-a-pr.md`
  - [ ] `skills/<each other leaf skill the program uses>/SKILL.md`
- [ ] Arm the hourly audit tick through profile routing's parent-owned T3 schedule, or the supported `/loop 1h` mechanism outside T3. Never leave the cadence to memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from the installed plugin and the standing objective. Audit the operation against both and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then post a short status message to the operator in chat only when the audit found a tracked change that no earlier status message reported, such as a PR opened, a code-ready head, a round launched or closed, a verdict, a merge, a stuck agent and the action taken, a blocker added or cleared, or a decision only the operator can make. Name every such change and nothing else. Do not repeat a table, the merged list, or an unchanged blocker. If the audit found none, end the turn with no reply text. Either way, log this tick's row in your decision trail. The row names the items reported, or none."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the full lifecycle the execution playbook names.
- [ ] Follow this dependency graph. Start dependent work only after its parent merges, or base it on the parent branch when the execution playbook stacks.
  - [ ] <PR id> and <PR id> are independent and first. Both branch from `main`.
  - [ ] <PR id> after <PR id>.
- [ ] Hold the file boundaries. <PR id or class> touches only `<glob>`.
- [ ] Hold the requested UI review gate. <PR ids, or None with a reason.> UI checks require the operator's explicit request.

### PR mechanics, for every PR

- [ ] Resolve the forge once. Default to `gh`; if `command -v origin` succeeds and Origin can resolve the repository, use `origin pr` for every PR operation. Record any fallback to `gh`. Never require `gt`.
- [ ] Open the PR ready, never draft, with `origin pr create --status open --base <base-branch>` or `gh pr create --base <base-branch>` according to the resolved forge. A stack child targets its parent branch.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Apply the shared cleanup rules in [Opening a PR](opening-a-pr.md) before commit and review.
- [ ] Triage every review-bot and security-reviewer comment per `../references/bugbot-triage.md`.
- [ ] Before the code-ready report and babysit, and again after merge prep, record the base and head SHAs prepared by the topology owner under the execution playbook.

### Verdict and merge, for every PR

- [ ] Independently verify and audit the first code-ready head; assess later revisions under verify-change, repeating only invalidated proof, affected audit findings or newly introduced risks; the root reviews receipts before the verdict.
- [ ] Clean only when every required scenario, check and audit passes. Findings go back to the owner, including defects reported as notes. Reassess each new head and reuse unaffected proof under verify-change and `playbooks/shipping.md`; rerun changed or uncertain checks and scenarios.
- [ ] <The merge or append rule from the execution playbook, with the patch-id rule from `playbooks/shipping.md`.>

### Boot recipe, for the verifier

The verifier runs in its own worktree at the recorded base and PR head. Drive through the skill path or exact commands recorded in this boot recipe.

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] <Start the backend and the surface. Wait for ready.>
- [ ] <Deliver input only through the driver skill's commands. Name the read-only diagnostics.>
- [ ] Save scenario evidence and the report under `~/.pstack/outputs/<program>/<pr-id>/` and return the paths. Capture UI evidence only when requested.

## <Task as a verb phrase> (<PR id>)

**Depends on.** <PR id, or None.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.
- [ ] Delete `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify, unit.** Required repository checks and focused behavior tests support runtime proof.

- [ ] Run `<required check commands>` at the recorded head and record the outcomes. Add meaningful behavior tests where the change needs them.

**Verify, live.** One independent verifier follows [verify-change](<absolute-path-to-installed-verify-change-SKILL.md>) at the recorded base and head. Add as many scenarios as affected behavior needs.

- [ ] Scenario 1. Regression against base. Run <inputs and scenario> at base and head. If the base lacks the feature, record that and prove <added behavior>. Evidence `<report or artifact path>`. Pass when <expected outcome>.

**Verify, perf.** None. <Reason performance is unaffected. If required, replace None with Required and state the reason, then add Metric, Probe, Baseline and Rule boxes under the performance policy above.>

**Verify, audit.** Risks. None. <Explain why none of the five second-audit cases applies; otherwise list their exact names separated by commas and add Audit 2 with a distinct focus on those risks.>

- [ ] Audit 1. Review correctness, affected callers, the declared risks and verification receipts at the recorded base and head. Evidence `<audit report path>`. Pass when <no unresolved actionable findings>.

**Review gate.** None. <No UI review was requested. If requested, replace with the authorized scope and add screenshot, video and operator review boxes.>

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Bugbot triage done.
- [ ] Base and verdict are current under the execution playbook and the patch-id rule in `playbooks/shipping.md`.
- [ ] The operator's explicit merge approval covers this PR or a named stack that includes it.
- [ ] <The authorized landing actor merges this PR, or the root delivers the verified stack for the operator to land bottom-up, under the execution playbook.>

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the report the execution playbook names.

## Appendix A. Prototype evidence

<Each open question a prototype answered, with the branch, the SHA, and the artifact links. Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk with the PR it lands in and what the owner watches.>

## Appendix D. Links and reading list

<Docs to read before editing. Which PRs get `skills/how/SKILL.md` and `skills/interrogate/SKILL.md`. The trail per `skills/show-me-your-work/SKILL.md`.>
````

**Reply:** the plan path, the PR ids with their dependencies and the review-gated set, what the prototypes proved and what stays unproven, and the check script's output.
