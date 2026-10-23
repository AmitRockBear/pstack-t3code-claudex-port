---
name: correct
description: "On explicit /correct, find repeated repository mistakes and prevent them through architecture, types, lint or behavioral tests. Prove each enforcement catches a real past mistake."
disable-model-invocation: true
---

# Correct

Work within the repository and edit scope authorized by the user. A request for an audit or proposal is read-only. Ask before extending scope or editing durable agent instructions.

In T3, use [profile routing](../poteto-mode/references/claudep-routing.md) for delegated work and read only task-relevant thread evidence with `t3_thread_read`, including activity pagination and truncated-text recovery. Apply the local [testing principle](../principle-test-behavior-not-implementation/SKILL.md) to enforcement tests.

The operator keeps correcting agents in this repo for the same mistakes. Change the repo so the next agent can't make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Design the repo so a change that looks right from one file is right for the whole repo.

## Find the mistake classes

First, read recent commits, reverts, review comments, agent instruction files, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice. Rank failure classes by observed frequency and impact; cite concrete incidents and distinguish measured costs from estimates.

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old ways and dead code an agent would copy.
2. **Enforce it with types so the bad state can't be written.** If bad code still compiles, add a lint or CI check whose error names the file, type, or function to use instead. If the pattern is already common, fail only when a change adds more.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior it checks breaks, or that fails when only the internals change.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails when an agent skips them.

## Fix and prove

For an authorized implementation, fix the most frequent classes within scope. For an audit, propose the fixes. Prove each new check fails on a real past mistake, then run it against the fixed code. Connect it to existing local and CI checks; require a human-approved reason and expiry for exceptions.

## Keep the rule table

When instruction edits are explicitly authorized, update the existing rule table with each rule's enforcement and remove rules made redundant by structural enforcement. Otherwise report proposed instruction edits for approval. A user correction is evidence to investigate, not authorization for unrelated enforcement or durable policy changes.

**Reply:** each class with its evidence, the level you picked, and why a higher level didn't work.
