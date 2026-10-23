#!/usr/bin/env bash
# PreToolUse(Bash): block destructive git commands until a backup ref points at the repo's HEAD.
input="$(cat)"
cmd="$(jq -r '.tool_input.command // empty' <<<"$input")"
cwd="$(jq -r '.cwd // empty' <<<"$input")"

destructive='git( -C [^ ]+)? (reset[^;&|]*--hard|rebase --abort|checkout[^;&|]*--detach|switch[^;&|]*--detach)'
grep -qE "$destructive" <<<"$cmd" || exit 0
grep -qE '(branch|update-ref) (refs/heads/)?backup/' <<<"$cmd" && exit 0

dir="$(sed -nE 's/.*git -C ([^ ]+) (reset|rebase|checkout|switch).*/\1/p' <<<"$cmd" | head -1)"
[ -n "$dir" ] || dir="$(sed -nE 's/^.*cd ([^ ;&|]+) *&&.*$/\1/p' <<<"$cmd" | head -1)"
dir="${dir:-$cwd}"
case "$dir" in "~"*) dir="$HOME${dir#\~}" ;; /*) ;; *) dir="$cwd/$dir" ;; esac

if git -C "$dir" for-each-ref --points-at HEAD --format='%(refname)' refs/heads/backup refs/restack-backup 2>/dev/null | grep -q .; then
  exit 0
fi
echo "Blocked destructive git command. First save the current state: git -C $dir branch backup/<name>-$(date +%Y%m%d%H%M%S) HEAD, then rerun. Undo on a PR branch under review with a revert commit instead." >&2
exit 2
