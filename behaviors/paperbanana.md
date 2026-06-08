---
bundle:
  name: research-paperbanana
  version: 0.5.0
  description: "PaperBanana figure generation as native Amplifier constructs (no packaged tool): a figure-designer agent generates publication figures directly via matplotlib/TikZ, a fresh-eyes figure-critic applies the 8 quality veto rules, and the paperbanana-figure recipe drives plan -> approve -> generate -> critique -> refine."

agents:
  include:
    - research:figure-designer
    - research:figure-critic

context:
  include:
    - research:context/figure-generation/paperbanana-methodology.md
---

# PaperBanana Behavior

PaperBanana-style figure generation (arXiv 2601.23265) rebuilt from native Amplifier
constructs — there is no `tool-paperbanana` module. The capability is delivered by two agents
plus a recipe, so nothing loads (or fails to load) until a figure is actually requested:

- **@figure-designer** — Planner + Visualizer. Writes and runs matplotlib/seaborn/TikZ to
  produce publication-ready figures, following the 8 quality veto rules. Uses bash + the
  filesystem directly; no packaged tool, no heavy module mounted into every session.
- **@figure-critic** — the antagonistic Critic. Spawned fresh to apply the 8 veto rules and
  return a strict JSON verdict, carrying no generation bias.
- **`recipes/paperbanana-figure.yaml`** — orchestrates the full pipeline (plan → human
  approval → generate → critique → conditional refine). The iteration the tool used to run
  internally is now expressed as recipe steps.

## Agent Delegation
Figure requests → @figure-designer (generation), @figure-critic (quality gate). For the full
gated workflow, run `recipes/paperbanana-figure.yaml`.
