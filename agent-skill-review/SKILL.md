---
name: agent-skill-review
description: Review Agent Skills (SKILL.md files and their bundled scripts/references/assets) through five lenses — premise & design, spec conformance, activation/triggering, instructional craft, and measured outcome. Use when asked to review, audit, critique, red-team, or improve an Agent Skill, a SKILL.md file, or a skill directory; to judge whether a skill is well-scoped, well-architected, or worth building at all; to diagnose why a skill isn't triggering or activating; or to check spec compliance. Reviews existing skills; it does not author or create new ones — for authoring, use a skill-creation skill.
license: MIT
metadata:
  author: max.dunn
  version: "2.0"
---

# Reviewing Agent Skills

Review an Agent Skill through five lenses, each catching a class of failure the others structurally cannot. The Agent Skills format is an open standard documented at [agentskills.io](https://agentskills.io/home); this skill turns that documentation into a repeatable, multi-lens review.

Always cite the authoritative docs in your findings so the review stays correct as the spec evolves. Link to the relevant section rather than restating rules from memory.

## The five lenses

A skill must clear a funnel: **deserve to exist → be valid → get discovered → guide execution → actually help.** Each lens evaluates one stage with a different method. Review in funnel order because an early failure signals that later polish may be wasted effort — don't over-invest in refining a skill that shouldn't exist. An early failure is a warning, not a hard stop: continue surfacing later findings the author may still want.

| # | Lens | Question it answers | Mode | Deep criteria |
|---|------|---------------------|------|---------------|
| 1 | Premise & Design | Should it exist, and is it shaped right? | Adversarial, by reading | [premise-and-design.md](references/premise-and-design.md) |
| 2 | Conformance | Is it a valid skill that will load and validate? | Objective, scripted | [rubric § Conformance](references/review-rubric.md) |
| 3 | Activation | Will it trigger when it should, stay quiet when it shouldn't? | Semi-empirical (the description) | [rubric § Activation](references/review-rubric.md) |
| 4 | Instructional Craft | Once triggered, will an agent execute well from it? | Quality, by reading | [rubric § Craft](references/review-rubric.md) |
| 5 | Outcome | Does it measurably beat no-skill? | Empirical, by running | [rubric § Outcome](references/review-rubric.md) |

Two concerns cut **across** lenses rather than forming their own, so evaluate them inside the lenses noted:

- **Safety / blast radius** — within Lens 1 (misactivation harm, conflicts with sibling skills) and Lens 4 (script hygiene, destructive-op guards).
- **Maintainability & human legibility** — within Lens 2 (no time-sensitive info), Lens 4 (links to authoritative docs vs. restating rules; whether a human can read, trust, and safely change the skill), and Lens 1 (structural legibility). A skill can pass every lens and still be write-only; you can't maintain what you can't read.

## Review workflow

Copy this checklist and track progress:

```
Review Progress:
- [ ] Step 0: Locate the skill and read every file
- [ ] Lens 1: Premise & Design (funnel gate — a Reject means later polish may be wasted)
- [ ] Lens 2: Conformance (run the validator)
- [ ] Lens 3: Activation (description quality)
- [ ] Lens 4: Instructional Craft (body + scripts)
- [ ] Lens 5: Outcome (on-demand — only if depth warranted)
- [ ] Write the review report
```

### Step 0 — Locate and read

Find `SKILL.md` and read it fully, plus every bundled file in `scripts/`, `references/`, and `assets/`. A review that reads only `SKILL.md` misses broken references, undocumented scripts, and stale content — and cannot judge premise or craft honestly.

### Lens 1 — Premise & Design (first; funnel gate)

Load [references/premise-and-design.md](references/premise-and-design.md) and work its gate. This lens is adversarial and subjective, kept walled off from the doc-grounded lenses so opinion never masquerades as a spec violation. It runs first because if the skill shouldn't exist or is mis-architected, later polish may be wasted effort. If the reason-to-exist gate fails, say so plainly and recommend deletion or a rethink — then continue at your discretion, still surfacing conformance and craft findings the author may want even after a Reject.

### Lens 2 — Conformance (validator)

Run the bundled validator to catch mechanical spec violations before spending judgment:

```bash
uv run scripts/validate_skill.py <path-to-skill-directory>
```

`python3 scripts/validate_skill.py <path>` also works but is a fallback only — see the Gotchas entry below for why `uv run` is the safer default.

It emits JSON (errors, warnings) and exits non-zero on any hard spec violation. Fold its output into the report; do not re-derive limits by hand. Criteria: [rubric § Conformance](references/review-rubric.md).

### Lens 3 — Activation (triggering)

The `description` carries the entire burden of activation ([optimizing-descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)). Judge it against [rubric § Activation](references/review-rubric.md). If triggering is the primary concern, recommend the labeled eval-query method — see [rubric § Activation](references/review-rubric.md) for the method rather than restating the recipe here.

### Lens 4 — Instructional Craft

Given it triggers and should exist, judge whether the body and scripts make an agent perform well: leanness, calibration (freedom vs. prescription), defaults-not-menus, gotchas, templates, script hygiene. Criteria: [rubric § Craft](references/review-rubric.md).

### Lens 5 — Outcome (on-demand)

Structural review can't confirm the skill improves outputs. When the user wants that assurance, run eval-driven testing per [evaluating-skills](https://agentskills.io/skill-creation/evaluating-skills). Criteria: [rubric § Outcome](references/review-rubric.md). Skip for lightweight reviews and say the review was structural only.

### Write the report

Use the [Report format](#report-format). Every finding must be actionable (what's wrong and what to change) and, where it reflects a spec or best-practice rule, link to the authoritative section.

## Severity levels

- **Reject (judgment call)** — Lens 1 verdict: the skill doesn't justify existing, or is fundamentally mis-architected. Subjective and adversarial by design — never conflate with a spec violation. Recommend deletion or rethink, note it prominently, then continue the remaining lenses at your discretion.
- **Blocker (spec violation)** — Violates a hard spec rule (Lens 2). Objective; may fail to load or validate.
- **Major** — Will likely mis-trigger, waste context, or produce wrong output. Fix before use.
- **Minor** — Quality or clarity improvement; safe to defer.

## Report format

Use this template, adapting to what you found. Omit the Lens 5 section if you didn't run evals.

```markdown
# Skill Review: <skill-name>

## Verdict
<One line: ship / fix blockers first / rework / reject — plus the headline reason.>

## Lens 1 — Premise & Design
<Reason-to-exist call; strongest case against; scope & architecture assessment.
 If rejected, note it prominently; continuing to later lenses is optional.>

## Lens 2 — Conformance
<Validator summary: pass/fail, key errors and warnings.>

## Lens 3 — Activation
<Does the description trigger reliably? Suggested rewrite if weak (<1024 chars).>

## Lens 4 — Instructional Craft
<Execution-quality findings for the body and scripts.>

## Lens 5 — Outcome (if run)
<Eval results vs. baseline, or "not evaluated — structural review only".>

## Findings by severity
### Reject (judgment call)
- **<title>** — <why the premise/architecture fails, what a rethink would look like>.
### Blockers (spec violations)
- **<title>** — <what's wrong, why it matters, exact fix>. ([link])
### Major
- **<title>** — <what's wrong, why, fix>. ([link])
### Minor
- **<title>** — <suggestion>.
- e.g. **Bundled helper script has no `--help` output** — an agent invoking it blind has to read the source to learn its flags; add an argparse `--help`.

## Strengths
- <What the skill does well — call this out; it guides what not to change.>
```

## Review principles

- **Keep the lenses honest.** Lenses 2–5 are graded against the docs — tie each finding to a rule or authoritative section. Lens 1 is explicitly subjective; label it as judgment, never as a spec violation.
- **Run the funnel in order.** An early-stage failure signals that later polish may be wasted, so weigh how much effort downstream lenses deserve — but it's not a hard stop. Don't over-refine execution details of a skill that fails its premise, while still surfacing findings the author may want.
- **Reward leanness.** More instructions are not better. Flag content the agent already knows as cuttable, not as missing detail to expand ([best-practices](https://agentskills.io/skill-creation/best-practices)).
- **Verify claims, don't assume.** Open referenced files to confirm links resolve and scripts exist. Note undocumented scripts and dead references.
- **Preserve intent.** Suggest improvements; do not rewrite the author's domain content unless asked.

## Available scripts

- **`scripts/validate_skill.py`** — Lens 2 engine. Validates a skill directory against hard spec rules (frontmatter presence, `name` format and directory match, `description`/`compatibility` length limits) and emits best-practice warnings (SKILL.md length, unresolved file references, undocumented scripts). Run `uv run scripts/validate_skill.py <path>` (resolves PyYAML automatically via the script's PEP 723 dependency block); `python3 scripts/validate_skill.py <path>` is a fallback only — see Gotchas. Use `--help` for options and exit codes.

## Gotchas

- **A clean Lens 2 result does not prove the frontmatter is valid.** `scripts/validate_skill.py` prefers PyYAML but silently falls back to a minimal hand-rolled YAML parser when PyYAML isn't installed. That fallback only understands simple frontmatter — top-level scalars, block scalars, and one level of mapping. On exotic or non-trivial frontmatter (YAML anchors, flow mappings like `{a: 1}`, multi-line list values, and similar) it can quietly mis-parse, so a passing validator run is **not** a guarantee of correctness. For any skill with non-trivial frontmatter, run it with PyYAML available before trusting the result, and say so in the report. The script carries an inline [PEP 723](https://agentskills.io/skill-creation/using-scripts) dependency block, so `uv run scripts/validate_skill.py <path>` resolves PyYAML automatically; a bare `python3` run instead requires PyYAML already installed in the environment (else it silently uses the fallback). Gotchas like this belong in `SKILL.md` so the reviewer reads them before hitting the situation ([best-practices](https://agentskills.io/skill-creation/best-practices)).
