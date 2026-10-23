---
name: create-pr
description: Use when the user asks to file, open, or create a PR.
disable-model-invocation: true
---

# Create PR

Before filing, check whether a PR for this branch already exists. Review the diff locally against the intended PR base (the parent branch for a stack, normally `origin/main` otherwise) to make sure its contents match the goal.

This skill owns PR titles, descriptions and publication for pstack's [Opening a PR](../poteto-mode/playbooks/opening-a-pr.md) workflow. Use existing [verify-change](../verify-change/SKILL.md) evidence; UI checks require the user's explicit request. Write the body and supporting artifacts under a task directory in `~/.pstack/outputs`.

## PR title

- If a Linear ticket ID was mentioned in the conversation, prefix the PR title with `<ticket_id>:` followed by a space (for example, `ABC-1234:`).
- Prefer a concise, human-readable title that explains why the change matters.

BAD

> ❌ negotiate permessage-deflate on the websocket

GOOD

> ✅ ABC-1234: cut websocket frame size by 70%+ with gzipping

## PR description

- Open the description with a simple explanation of the problem based on the user's original prompt, then briefly explain the solution. Do not lead with an implementation inventory. Then, have in bold `Changes:` and then a list of bullet points that describe the changes made in the PR on a high level (dont mention the files or lines that were changed, nor that tests were added or modified).
- After Changes, add **Tradeoffs:** for rejected alternatives a reviewer would reasonably ask about, with a brief reason for the choice. Omit it when there was no meaningful choice.
- Then add **Blast radius:** in one to three sentences explaining who or what is affected and why the change is safe or risky. Omit it when it adds nothing beyond the opening explanation.
- Add **Validation:** with brief live UI/API checks and outcomes, followed by `**Before:**` / `**After:**` evidence: uploaded images/videos, or a short fenced API/server log proving the behavior. Use `None` for missing checks or evidence. Tests/lint do not count as evidence.
- Add a blurb to the end of the PR description about what model is making the changes.
- Use bold labels for PR description sections, including optional sections; keep Markdown headings for skill documentation only.

### Example

Save the description as `body.md` under the task output directory. Use matching absolute media paths in the body and `--attach`; `gh` replaces them with hosted URLs. Verify the published body contains hosted evidence URLs, or report the upload failure.

````md
Refreshing a thread hid its running indicator. The list now preserves live status after refresh.

**Changes:**
- Include the current running state in thread summaries

**Tradeoffs:**
Use the server's running state rather than infer it from cached messages, which can be stale after refresh.

**Blast radius:**
Thread summaries and the list indicator are affected. Message content and task execution are unchanged.

**Validation:**
- UI: refreshed a running thread; indicator stayed visible.
- API: fetched thread summaries; running state was present.

**Before:** None

**After:**

[Attach the reviewed video here.]

```text
GET /threads → 200
{"id":"thread-123","sidebarIndicator":"running"}
```

Made with <model>.
````

### Create/Edit a PR

From the repository checkout, create a PR using the task's absolute body and attachment paths:

```bash
gh pr create --title "Preserve running status after refresh" --base "<base>" --head "<branch>" --body-file "~/.pstack/outputs/<task>/body.md" --attach "~/.pstack/outputs/<task>/refresh.mp4"
gh pr view "<PR URL>" --json body --jq .body
```

For an existing PR, use `gh pr edit "<PR URL>" --body-file "<task-output-dir>/body.md" --attach "<task-output-dir>/refresh.mp4"` with its updated body and absolute paths.

Open a real PR rather than a draft so review bots run. In T3, register existing PRs when starting work and new PRs immediately after creation with `link_pull_request` using the full URL. If the user also asked to babysit it, continue with the bundled [babysit](../babysit/SKILL.md) policy and the workflow's stack timing.
