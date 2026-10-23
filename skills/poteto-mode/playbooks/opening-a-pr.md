### Opening a PR

Use when the user requests a PR or the active playbook explicitly calls for one.

Use the bundled [create-pr](../../create-pr/SKILL.md) as the shared policy for PR titles, descriptions, existing-PR detection, evidence attachments and publication.

**Worktree.** Work from a git worktree off main. Subagents inherit it. Multiple `Agent` calls on the same branch each get their own worktree, or `git fetch && git reset --hard origin/<branch>` between them. Dirty branch with unrelated work: patch out, fresh worktree, apply. Snarled worktree: reset from main, redo minimally. Before publication, cleanup or replacing a writer, inspect task-owned writers and pending children through profile routing. Wait for completion or confirm cancellation where stopping is necessary, preserve unrelated processes, then run `git status` and read the tree you are about to ship.

**Commits.** Commit liberally. Rebase into small, ordered commits before opening PRs. Each commit is a future PR: landable, ordered to tell the story. Amend when the fix belongs in a just-made commit. New commit when separable.

**PRs.** Run `/deslop` once over the current diff before commit; reuse that result while the diff is unchanged. Write every PR title, PR description, and commit body in one pass that applies `/technical-writing` and `/unslop` together. Apply every technical-writing layer except Diátaxis. Use one word for each action, keep articles, and avoid `-ing` when a plain verb works.

**Title and body.** Follow [create-pr](../../create-pr/SKILL.md) for the title and description schema. The squash commit body is the PR body; a commit body does not restate its subject.

**Publication.** Follow [create-pr](../../create-pr/SKILL.md) for existing-PR detection, publication and attachment readback. Record partial upload failures against the existing PR before retrying, so a failed attachment does not create a duplicate PR.

**Size and stacks.** Prefer one cohesive, independently verifiable PR; split when useful review boundaries or dependencies justify it. A stack is a base-branch chain. The root PR targets trunk. Each child branch rebases onto its parent's exact tip and its PR targets the parent branch. Create a child with `gh pr create --base <parent-branch>`. Retarget an existing child with `gh pr edit <pr> --base <parent-branch>`. Branch from trunk only for independent work. Rebase on trunk before substantial stack work.

**Readiness.** Open every PR ready, never as a draft. Omit `--draft`; if an existing PR is a draft, run `gh pr ready <number>`. Run `gh pr view <number>` before you refer to PR status.

**Babysit.** If babysitting is part of the request, continue with [Babysit](babysit.md) after the requested PR or stack exists. Opening a PR alone does not start monitoring. Post the URL and keep building when monitoring was not requested. Push back when feedback drifts from intent.

A subagent that opens a PR runs `interrogate`, follows the cleanup and writing rules above, and posts the URL. In T3, every owner returns a finite work receipt to the parent, which owns any requested monitoring under [Babysit](babysit.md). Outside T3, the Autopilot-full and Autopilot-stack owner briefs assign their babysit loops after the code-ready report and determine merge-ready or STACK-READY; other children return without babysitting.
