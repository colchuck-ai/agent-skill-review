# agent-skill-review Architecture

The skill is a `SKILL.md` orchestrator that drives a five-lens review funnel, with detail pushed down to two reference documents and one validator script. The orchestrator sequences the review and owns the severity scale and report format; the references carry the judgment criteria; the script carries the mechanical, deterministic checks. Subjective judgment (the premise gate) is deliberately held in its own file so it never mixes with the spec-grounded criteria, and every normative claim links out to the authoritative Agent Skills documentation rather than restating it.

## Principles

- Progressive disclosure: `SKILL.md` is the orchestrator; the review criteria and the validator live in `references/` and `scripts/` and are loaded only when their lens runs.
- Wall subjectivity off from objectivity: the adversarial premise judgment lives in its own reference file, separate from the doc-grounded rubric, so opinion is never presented as a spec violation.
- Ground claims, do not restate them: normative rules link to the authoritative Agent Skills docs so the review stays correct as the spec evolves.
- Script the mechanical, prose the judgmental: deterministic spec checks are a tested script; everything requiring judgment is guided prose.

## Constraints

- The skill must conform to the very spec it reviews (it is dogfooded against its own validator): `SKILL.md` body under ~500 lines, `description` ≤ 1024 characters, references one level deep.
- The validator must run correctly without a preinstalled environment; it declares its dependency inline (PEP 723) so `uv run` resolves PyYAML, and warns that a bare `python3` run may silently degrade.
- Distribution is out of the review runtime: the skill is copied into an agent's skills directory by `install.sh` (`cursor`, `claude`, or `agents` targets), which is packaging tooling, not a review component.

## Technology Choices

- Agent Skills format (Markdown `SKILL.md` plus `references/`): the open standard the skill both targets and conforms to.
- Python 3.8+ validator with PyYAML pinned via an inline PEP 723 dependency block: emits JSON on stdout, diagnostics on stderr, and meaningful exit codes so its output folds into the report without hand-parsing.
- Bash installer: single-file, dependency-light distribution across known agent skill directories.

## Components

### C001 - Review Orchestrator

Defines the five-lens funnel, its sequencing, the severity levels, and the report format; routes each lens to the premise gate, the rubric, or the validator, and instructs the safe validator invocation.

**Relationships**

- **C002 - Premise & Design Gate**: loads it for Lens 1 before the doc-grounded lenses run.
- **C003 - Review Rubric**: loads it for the pass/fail criteria of Lenses 2–5.
- **C004 - Conformance Validator**: invokes it for Lens 2 and folds its JSON output into the report.

### C002 - Premise & Design Gate

Carries the adversarial Lens 1 gate — reason-to-exist, steelman-then-attack, scope/architecture, and blast radius — walled off from the spec-grounded lenses so its verdicts are labeled as judgment, never as spec violations.

**Relationships**

- **C001 - Review Orchestrator**: invoked by it as the first lens; returns a judgment verdict, not a spec finding.

### C003 - Review Rubric

Holds the pass/fail criteria for Conformance, Activation, Instructional Craft, and Outcome, each check linked to its authoritative source and mapped to a severity.

**Relationships**

- **C001 - Review Orchestrator**: invoked by it for Lenses 2–5 criteria and severity mapping.

### C004 - Conformance Validator

Validates a skill directory against hard spec rules (frontmatter presence, `name` format and directory match, `description`/`compatibility` length limits) and best-practice warnings (body length, unresolved references, undocumented scripts); emits a JSON report and exits non-zero on any spec violation.

**Relationships**

- **C001 - Review Orchestrator**: invoked by it for Lens 2; the orchestrator instructs `uv run` so PyYAML resolves and the parser does not silently degrade.

## Requirement-Component Map

- **O001-R001 - Multi-method review**: C001 - Review Orchestrator
- **O001-R002 - Read everything first**: C001 - Review Orchestrator
- **O001-R003 - Continue past early failure**: C001 - Review Orchestrator, C002 - Premise & Design Gate
- **O001-R004 - Trustworthy validation**: C004 - Conformance Validator, C001 - Review Orchestrator
- **O002-R001 - Separate judgment from spec**: C002 - Premise & Design Gate, C001 - Review Orchestrator
- **O003-R001 - Mechanical checks by tool**: C004 - Conformance Validator
- **O003-R002 - Funnel ordering**: C001 - Review Orchestrator
- **O004-R001 - Actionable findings**: C001 - Review Orchestrator, C003 - Review Rubric
- **O004-R002 - Cite the source**: C001 - Review Orchestrator, C002 - Premise & Design Gate, C003 - Review Rubric
