# agent-skill-review

An [Agent Skill](https://agentskills.io/home) for reviewing other Agent Skills.

It evaluates a `SKILL.md` file (and its bundled `scripts/`, `references/`, and `assets/`) through five lenses, each catching a class of failure the others structurally cannot. The skill itself lives in [`agent-skill-review/`](agent-skill-review/):

1. **Premise & Design** — should it exist, and is it shaped right?
2. **Conformance** — is it a valid skill that will load and validate?
3. **Activation** — will it trigger when it should, and stay quiet when it shouldn't?
4. **Instructional Craft** — once triggered, will an agent execute well from it?
5. **Outcome** — does it measurably beat no-skill?

## Usage

Ask an agent to review a skill, e.g. "review the skill in `path/to/skill`". The agent reads [`SKILL.md`](agent-skill-review/SKILL.md) and follows its workflow, producing a report with findings by severity.

To run the conformance validator directly:

```bash
uv run agent-skill-review/scripts/validate_skill.py <path-to-skill-directory>
```

Using `uv` ensures PyYAML is available; a bare `python3` run falls back to a minimal YAML parser that can mis-parse non-trivial frontmatter.

## Contents

- `agent-skill-review/SKILL.md` — the skill definition and review workflow
- `agent-skill-review/references/premise-and-design.md` — Lens 1 adversarial gate
- `agent-skill-review/references/review-rubric.md` — criteria for Lenses 2–5
- `agent-skill-review/scripts/validate_skill.py` — spec conformance validator (Lens 2)
- `install.sh` — installer that clones the repo and copies the skill into your agent's skills directory

## License

MIT — see [LICENSE](LICENSE).
