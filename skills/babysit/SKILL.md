---
name: babysit
description: Use when the user asks to monitor, watch, subscribe or babysit a PR.
disable-model-invocation: true
---

# Babysit PR

On Codex, read the [platform mapping](../poteto-mode/references/codex-tools.md), including its per-skill notes, before following this skill.

Use this policy both directly and through the [Babysit playbook](../poteto-mode/playbooks/babysit.md). Use `gh` for GitHub and preserve the assigned branch, requested PR/stack scope and existing approvals. In T3, register scoped PR URLs with `link_pull_request` when available.

For required rebases, coordinate with the branch/topology owner and follow [merge and restack safety](../poteto-mode/references/merge-safety.md) around pending merges and descendants. Update a descendant only when its babysitting turn begins.

All the repos we work in have various AI review bots. They're helpful, even if they are not always right.

In T3, use `watch_pull_request` when available. Handle existing scoped comments, call it with each PR's full `url`, and end the turn. On a wake, inspect the current head, checks and review findings; delegate finite fixes with `delegate_task` when needed and keep the parent's watches active while fixes run. Before handing monitoring back to the user, call `unwatch_pull_request` for the scoped watches. On every resume, re-arm each scoped watch; children never unwatch.

T3 parents own PR watches. Delegated children return after finite build or comment-fix work with their head SHA, check results and pending work; the parent handles later CI and review wakes. Keep PR polling, sleep loops and shell watchers outside this T3 path.

Outside T3, use harness monitoring tools when available; otherwise poll for new comments and checks.

Track unresolved findings across pushes and re-read updated review-summary comments. Before you report a PR as ready or green, run `~/.pstack/skills/poteto-mode/scripts/watch-pr/watch-pr --status-only --owner <owner> --repo <repo> --pr <number> --pretty`; it pages unresolved review threads, and a T3 watch does not wake for comments posted under the user's account. Evaluate findings against the current code and check CI/review completion for the latest head. Verify every bot finding against the source before changing code. Fix real findings and CI failures, distinguish repository failures from infrastructure flakes, reply with a written reason for every comment worth addressing or that you decided to dismiss, and resolve the comment.

If a review bot posts a summary comment with a status row per review, keep babysitting until each row shows completed for the current head.

If the PR has conflicts with the base branch, rebase when needed. If an overlapping PR makes this one obsolete, stop monitoring, report it to the user, and ask before closing the PR unless closure was explicitly authorized.

Format comments left on the user's behalf as:

```md
**[MODEL-SLUG] RESPONDING ON BEHALF OF [USER]**
[actual reply]
```

After you post, read the PR comments to confirm the post landed, and retry only when it is missing. Keep the post command's exit status visible.

For each review comment, check:
- Is it valid and necessary for the user's original PR goal, or would addressing it introduce scope creep?
- Does its benefit justify the added complexity?
- Does this protect an agreed behavior through a small, concrete fix?
- Can the scenario actually happen? Dismiss it when existing code already prevents it or it needs a rare combination of conditions, and cite the file:line that prevents it.

Carry forward accepted scope, tradeoffs and reasoned dismissals; reopen decisions when new evidence changes their consequences.

Address worthwhile issues. Dismiss low-value suggestions and edge cases that do not justify their complexity. Resolve routine uncertainty through inspection. Ask about findings requiring a material product or scope decision.

When reviews stop producing worthwhile findings, report diminishing returns (also post as comment in the PR). Consider diminishing returns only when all outstanding review-bot comments are P2 or below.

Babysit stacked PRs one at a time, from the root PR upward. Once a PR meets the completion criteria, update the next PR onto its current parent if needed, then babysit it. Rebase descendants only when their turn begins. If an earlier PR changes again, finish it before continuing upward.

End a wake silently unless it brings a new finding, failure, user decision or finished gate. Run focused checks during fixes. In T3, complete babysitting when required CI and applicable reviews are complete on the current head and scoped findings are handled; yield with watches active while those conditions remain pending. Outside T3, stop after bots and required CI stay green on the latest commit for 15 minutes. Report addressed and dismissed comments by review round, with reasons and examples for complex comments.

Merge only when explicitly authorized by the user; babysitting alone does not authorize merging.

Unless told otherwise, this skill should not run another round of review using @codex review or @codex security review or run a computer use verification.
