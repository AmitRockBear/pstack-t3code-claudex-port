#!/usr/bin/env bash
# Rebase a stack bottom-up onto a new base and stop at the first failure.
# Usage: restack.sh --onto <new-base> --old-base <old-parent-of-first> --record <file> <branch>...
# Each branch is rebased onto the previous branch's new head, using the previous
# branch's old head as the boundary. Old heads are saved as refs/restack-backup/<stamp>/<branch>
# and in the record file before any rewrite. Nothing is pushed.
set -euo pipefail

onto="" old_base="" record=""
while [ $# -gt 0 ]; do
  case "$1" in
    --onto) onto="$2"; shift 2 ;;
    --old-base) old_base="$2"; shift 2 ;;
    --record) record="$2"; shift 2 ;;
    --) shift; break ;;
    -*) echo "restack: unknown option $1" >&2; exit 2 ;;
    *) break ;;
  esac
done
[ -n "$onto" ] && [ -n "$old_base" ] && [ -n "$record" ] && [ $# -gt 0 ] || {
  echo "usage: restack.sh --onto <new-base> --old-base <old-parent-of-first> --record <file> <branch>..." >&2
  exit 2
}
[ -z "$(git status --porcelain)" ] || { echo "restack: worktree is not clean" >&2; exit 2; }

stamp="$(date +%Y%m%dT%H%M%S)"
new_parent="$(git rev-parse --verify "$onto^{commit}")"
old_parent="$(git rev-parse --verify "$old_base^{commit}")"
start_ref="$(git symbolic-ref --quiet --short HEAD || git rev-parse HEAD)"

: > "$record"
for branch in "$@"; do
  head="$(git rev-parse --verify "refs/heads/$branch")"
  git update-ref "refs/restack-backup/$stamp/$branch" "$head"
  printf '%s %s\n' "$branch" "$head" >> "$record"
done

for branch in "$@"; do
  old_head="$(git rev-parse "refs/restack-backup/$stamp/$branch")"
  if ! git merge-base --is-ancestor "$old_parent" "$old_head"; then
    echo "restack: $old_parent is not an ancestor of $branch; stopped before $branch" >&2
    exit 1
  fi
  if ! git rebase --onto "$new_parent" "$old_parent" "$branch" >&2; then
    git rebase --abort
    git checkout --quiet "$start_ref"
    echo "restack: rebase of $branch failed; stopped. Later branches are untouched. Backups: refs/restack-backup/$stamp" >&2
    exit 1
  fi
  echo "restacked $branch $(git rev-parse HEAD)"
  old_parent="$old_head"
  new_parent="$(git rev-parse HEAD)"
done
git checkout --quiet "$start_ref"
