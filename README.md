# Research

Build the claim from evidence, keep the limits, and make the work inspectable.

People and agents doing evidence synthesis, experiments, or scientific writing. Use when a decision needs sources, an empirical claim needs a study, or a paper needs an auditable evidence chain.

## Install the portable method

```sh
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

Keep the complete `skills/research` folder together. Installation copies only that method, references, and license; it starts no service and installs no runtime. Use a different skills-parent path for your host.

## Choose the mode

- **Investigate** — A question needs a bounded multi-source answer. A source and claim map, contradictions, applicability, and open gaps.
- **Experiment** — A hypothesis has executable measurements and a justified budget. A frozen protocol, retained trials, integrity checks, and cautious inference.
- **Write** — Evidence is ready for a paper, brief, or technical report. A claim-linked manuscript with real citations, figures, methods, and limitations.

## What was consolidated

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

## Build the local site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

Open `_site/index.html` or serve `_site` with a local static server. The downloadable ZIP is built from canonical method bytes. The fictional before/after example illustrates intended judgment; it is not a measured improvement. Nothing has been published or renamed remotely.
