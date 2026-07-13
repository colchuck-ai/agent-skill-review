# Plan: Address agent-skill-review Findings

Source: self-review of `agent-skill-review/` conducted 2026-07-13. Four findings, two Major and two Minor. All changes are confined to `agent-skill-review/SKILL.md` except where noted.

## Major

### 1. Point the Lens 2 instructions at the safe validator invocation
- **File:** `agent-skill-review/SKILL.md`, Lens 2 section (`### Lens 2 — Conformance (validator)`)
- **Problem:** the code block tells the reviewer to run `python3 scripts/validate_skill.py <path>`, but the Gotchas section (further down the same file) reveals that a bare `python3` run can silently fall back to a hand-rolled YAML parser that mis-parses exotic frontmatter — `uv run scripts/validate_skill.py <path>` avoids this via the script's own PEP 723 dependency block. The riskier command is the one shown at the point of use.
- **Fix:** change the fenced command from
  ```bash
  python3 scripts/validate_skill.py <path-to-skill-directory>
  ```
  to
  ```bash
  uv run scripts/validate_skill.py <path-to-skill-directory>
  ```
  and add a one-line note that `python3` is a fallback only if `uv` is unavailable, pointing to the Gotchas entry for why.
- **Also touch:** `## Available scripts` bullet — update the example invocation there too so it stays consistent with Lens 2.

### 2. Separate the subjective "Reject" bucket from objective "Blockers" in the report template
- **File:** `agent-skill-review/SKILL.md`, `## Report format` section
- **Problem:** the template's `### Reject / Blockers` header conflates Lens 1's subjective, adversarial verdict with Lens 2's objective spec violations — directly against the skill's own stated principle that Lens 1 findings must be labeled as judgment, never as spec violations.
- **Fix:** split the header into two:
  ```markdown
  ### Reject (judgment call)
  - **<title>** — <why the premise/architecture fails, what a rethink would look like>.
  ### Blockers (spec violations)
  - **<title>** — <what's wrong, why it matters, exact fix>. ([link])
  ```
- **Also touch:** `## Severity levels` section — reword the "Reject" bullet if needed so its definition and the template header stay in sync.

## Minor

### 3. Add one worked example finding to the report template
- **File:** `agent-skill-review/SKILL.md`, `## Report format` section
- **Fix:** under the `Findings by severity` template, add a single short concrete example (real-sounding title, one-sentence failure scenario, exact fix) for one severity tier, so reviewers calibrate specificity from an instance rather than only from bracketed placeholders. Keep it to 2-3 lines — this is a craft aid, not a new section.

### 4. Decide how to handle the missing `evals/evals.json`
- **Context:** applying the skill's own Lens 5 rubric to itself shows it has no eval harness — expected, since Lens 5 is on-demand, but worth a deliberate decision rather than silence.
- **Options (pick one):**
  - (a) Do nothing — Lens 5 is explicitly on-demand per the skill's own design; no action required.
  - (b) Add a minimal `evals/evals.json` with a handful of real review tasks (e.g., reviewing a deliberately broken sample skill) so the skill can eventually be graded against its own rubric.
- **Recommendation:** (a) for now — revisit only if/when outcome assurance for this skill specifically becomes a priority.

## Sequencing
1. Fix #1 and #2 together (both are single, localized edits to `SKILL.md`).
2. Fix #3 in the same pass (same section as #2).
3. Decide #4 (likely just recording the decision, no code change).
4. Re-run `python3 agent-skill-review/scripts/validate_skill.py agent-skill-review` (or `uv run`) after edits to confirm the skill still validates cleanly.
