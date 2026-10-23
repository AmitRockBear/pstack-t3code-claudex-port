### Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.**

1. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, requested PRs merge-ready, pixel-diff zero). Include merged PRs only when the user explicitly approves landing those PRs or that stack. Approval to run autonomously does not authorize merging, auto-merge or merge-queue admission.
2. For T3 PR monitoring, the parent follows [Babysit](babysit.md). For other events, use the harness-owned watcher or scheduled wake mechanism through [profile routing](../references/claudep-routing.md); use a fixed-interval heartbeat only when no event can wake the coordinator. Outside T3, an event watcher subagent may provide the wake and a long heartbeat fallback.
3. Each iteration makes the smallest change the evidence justifies, runs focused development checks against the predicate, commits if it advanced, and discards task-owned changes that did not help. Use [verify-change](../../verify-change/SKILL.md) on Sol 6.1/high for implemented-change verification; reuse unaffected proof with a reason and rerun changed or uncertain behavior. UI checks require the user's explicit request. Belt-and-suspenders that "might help" gets reverted, not left to ride.
   Sequence the work via the **sequence-verifiable-units** principle skill, verifying each unit before the next instead of batching checks at the end.
4. Fix mid-run discoveries only when the requested outcome depends on them. Report unrelated findings as follow-ups and keep working toward the predicate. Resolve routine implementation uncertainty through inspection; involve the user in unresolved product or architecture decisions, irreversible actions outside the grant, or a real dead end. Open a PR only when requested or explicitly required by the active playbook, after implementation, cleanup and required development checks are complete.
5. Checkpoint every iteration via the **show-me-your-work** skill, a row for what changed and whether the predicate moved.
6. Stop when the predicate is met. A plateau is not a stop, so keep going and pivot your approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory.

**Reply:** the exit condition, iterations run, what landed, what was discarded, final predicate state.
