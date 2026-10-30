#!/usr/bin/env bash
# Pin the committed intervention before measurement; decide only on that revision.
set -uo pipefail
fail() { printf 'decide: %s\n' "$*" >&2; exit 1; }
root=$(git rev-parse --show-toplevel) || fail 'not in a work tree'
[ "$root" = "$(pwd -P)" ] || fail 'run from the intended repository root'
head=$(git rev-parse --verify HEAD) || fail 'no committed intervention'
meta=$(git rev-parse --absolute-git-dir) || fail 'cannot locate repository metadata'
state="$meta/experiment-loop-decision"
git diff --quiet --ignore-submodules=none -- || fail 'tracked work tree has changes'
git diff --cached --quiet --ignore-submodules=none -- || fail 'index has changes'
    # A file in this worktree's private Git metadata cannot follow a changed cwd.
    tmp=$(mktemp "$state.XXXXXX") || fail 'cannot create decision pin'
    trap 'rm -f "$tmp"' EXIT
    printf '%s\n%s\n' "$root" "$head" > "$tmp" || fail 'cannot write decision pin'
    mv -f "$tmp" "$state" || fail 'cannot save decision pin'
    printf 'decide: pinned %s\n' "$head"
    exit 0
