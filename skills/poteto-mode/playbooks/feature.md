### Feature

**You own the design. Plan, review, verify.** Delegate implementation. Stay in the lead.

1. `how` over the affected subsystem.
2. `architect` for parallel design exploration.
3. Write the throughput checkpoint as four todo items. A dimension that genuinely does not apply (single file, no fan-out) keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services or layers parallelize in separate worktrees. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (the **separate-before-serializing-shared-state** principle skill). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. Delegate code-writing using the configured feature model, with a clear scope, success criteria and its own isolated worktree. Name the file paths, data shape and organizing structure per **principle-model-the-domain** in the brief before the delegate writes logic. When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), use the **arena** skill with two independent implementation candidates: Claude Opus 5.5/high and GPT Sol 6.1/high, resolved through the profile's model mappings. After both candidates finish, use a separate readonly Claude Opus 5.5/high judge to score them against the rubric; follow Arena's base selection and grafting steps. This arena is mandatory when multiple valid shapes exist; Laziness Protocol does not override it. A subagent forbidden to spawn owns the diff directly with the same review separation. Give every file-writing delegate its own worktree, and do not write files or run a suite in a worktree another writer still holds. Fencing a file in the brief's prose is not a lock (**principle-separate-before-serializing-shared-state**). Comments per **Comments**. Surgical edits, re-ground against the source for upstream-derived files. Port shared-primitive improvements to all consumers and verify each. Commit liberally.
5. Use [verify-change](../../verify-change/SKILL.md) with Sol 6.1/high to verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
6. Rebase into small, ordered commits. Stack follow-ups.
   Use the **sequence-verifiable-units** principle skill, building, verifying, and committing each small unit before the next.
7. If the design is contested, `interrogate` before shipping.
8. Run **Opening a PR**.

Code-coupled work (one feature, one migration) goes to a single owner with the checkpoint inline. That owner fans out internally after the blocking phase, including implementation candidates when step 4 requires Arena. Parent-level fan-out is for slices that produce independent artifacts (audits, cross-subsystem investigations, competing experiments). Rewrite the checkpoint at phase boundaries. Spawn a fresh owner rather than chaining interrupts.

**Reply:** what you built, what you chose and why, the throughput checkpoint, open decisions. Tables for design alternatives.
