#!/usr/bin/env bash
# Pin the committed intervention before measurement; decide only on that revision.
set -uo pipefail
decision="${1:?usage: decide.sh <keep|revert>}"
case "$decision" in keep|revert) ;; *) echo "decide: invalid decision '$decision' (want keep|revert)" >&2; exit 2;; esac
fail() { printf 'decide: %s\n' "$*" >&2; exit 1; }
root=$(git rev-parse --show-toplevel) || fail 'not in a work tree'
[ "$root" = "$(pwd -P)" ] || fail 'run from the intended repository root'
head=$(git rev-parse --verify HEAD) || fail 'no committed intervention'
meta=$(git rev-parse --absolute-git-dir) || fail 'cannot locate repository metadata'
state="$meta/experiment-loop-decision"
git diff --quiet --ignore-submodules=none -- || fail 'tracked work tree has changes'
git diff --cached --quiet --ignore-submodules=none -- || fail 'index has changes'
[ -f "$state" ] && [ ! -L "$state" ] || fail 'missing decision pin; run pin_intervention.sh after committing the intervention'
{
    IFS= read -r expected_root && IFS= read -r expected_head && ! IFS= read -r extra
} < "$state" || fail 'invalid decision pin'
[ "$root" = "$expected_root" ] || fail 'decision pin belongs to a different repository'
[ "$head" = "$expected_head" ] || fail 'HEAD changed since the intervention was pinned'
if [ "$decision" = keep ]; then
    rm -f "$state" || fail 'cannot consume decision pin'
    echo 'decide: keep (intervention retained)'
    exit 0
fi
parent=$(git rev-parse --verify "$head^1") || fail 'intervention has no parent'
# reset --hard may overwrite untracked/ignored paths which obstruct parent files.
# Preserve unrelated untracked metric/ledger rows used by the documented loop.
python3 - "$parent" <<'PY' || fail 'untracked paths obstruct the baseline'
import subprocess, sys
parent = sys.argv[1]
tracked = subprocess.check_output(['git', 'ls-tree', '-r', '-z', '--name-only', parent]).split(b'\0')
untracked = subprocess.check_output(['git', 'ls-files', '--others', '-z']).split(b'\0')
for raw in untracked:
    path = raw.rstrip(b'/')
    if path and any(t and (path == t or path.startswith(t + b'/') or t.startswith(path + b'/')) for t in tracked):
        print('decide: untracked content would be overwritten', file=sys.stderr)
        raise SystemExit(1)
PY
git reset --hard "$parent" || fail 'reset failed; intervention was not reverted'
[ "$(git rev-parse --verify HEAD)" = "$parent" ] || fail 'reset did not reach the pinned parent'
rm -f "$state" || fail 'cannot consume decision pin'
echo 'decide: revert (intervention commit dropped)'
