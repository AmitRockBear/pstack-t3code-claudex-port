#!/usr/bin/env bash
# PreToolUse(Bash): block draft PRs, which review bots skip, and git stash, which every worktree shares.
cmd="$(jq -r '.tool_input.command // empty')"

if grep -qE 'gh pr create[^;&|]*[[:space:]](--draft|-d)([[:space:]=]|$)' <<<"$cmd"; then
  echo "Blocked draft PR. Open PRs ready for review: drop --draft/-d." >&2
  exit 2
fi
if grep -qE '(^|[;&|(`[:space:]])git([[:space:]]+-[Cc][[:space:]]+[^[:space:]]+)*[[:space:]]+stash([[:space:]]|$)' <<<"$cmd"; then
  echo "Blocked git stash: all worktrees share one stash. Commit to a scratch branch or use a detached worktree instead." >&2
  exit 2
fi
exit 0
