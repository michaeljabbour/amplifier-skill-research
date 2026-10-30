# Structure

`skills/research/SKILL.md` is the canonical portable entry. `skills/research/references/` contains original autonomous-experiment discipline, research roles, and attributed paper-authoring source references. Native `modules/`, `scripts/experiment-loop/`, `templates/`, `agents/`, `modes/`, and `recipes/` retain their original execution roles. `scripts/capability.py`, `site/capability/`, and `capability.json` own portable packaging and local site generation. `_site/` and `.venv-capability/` are ignored generated/local verification output.

`pin_intervention.sh` snapshots the committed iteration revision in worktree-private Git metadata before measurement; `decide.sh` validates and consumes that pin for keep/revert. `tests/test_decision_guards.py` and its shell wrapper cover destructive-failure boundaries offline.
